from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from starlette import status
from models.courier_users import *
from models.orders_model import *
from db import SessionLocal
from typing import Union
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_session():
    async with SessionLocal() as session:
        yield session

orders_router = APIRouter(tags = ["order"])

@orders_router.get("/api/order", response_model=Union[list[Main_Order_5]])
async def get_all_orders_db(DB: AsyncSession = Depends(get_session)):
    '''Получение информации о всех заказах системе.'''
    orders = await DB.execute(select(Order))
    orders = orders.scalars().all()
    if orders == []:
        return JSONResponse(status_code=404, content={"message": "Заказы не найдены"})
    else:
        return orders

@orders_router.post("/api/order", response_model=Union[Main_Order_2, Main_User_4], status_code=status.HTTP_201_CREATED)
async def create_order(name: str, district: str, DB: AsyncSession = Depends(get_session)):
    '''Публикация заказа в системе с полями:'''
    try:
        user_id = await DB.execute(select(User.id_user).where(User.active_order == {}))
        user_id = user_id.scalars().all()
        order = Order(name=name, district=district)
        count_id = ''
        for id in user_id:
            user_district = await DB.execute(select(User.district).where(User.id_user == id))
            user_district = user_district.scalars().first()
            if district in user_district:
                count_id = id
                break            
        if count_id == '':
            raise HTTPException(status_code=404, detail="Нет свободного курьера")
        order.id_user = count_id
        order.status = 1
        if order is None:
            raise HTTPException(status_code=404, detail="Объект не определен")   
        user  = await DB.execute(select(User).where(User.id_user == count_id))
        user = user.scalars().first()   
        DB.add(order)
        await DB.commit()
        await DB.refresh(order)

        user.active_order = {"order_id": order.id_order, "order_name": order.name}
        user.time_start = datetime.datetime.today().timestamp()
        try:
            user.time_start_work = user.time_start_work + 1 - 1
        except:
            user.time_start_work = datetime.datetime.today().timestamp()
        DB.add(user)
        await DB.commit()
        await DB.refresh(user)

        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при добавлении объекта. Нет подходящего курьера в данном районе")

@orders_router.get("/api/order/{id}", response_model=Union[Main_Order_3])
async def get_order(id: int, DB: AsyncSession = Depends(get_session)):
    """Получение информации о заказе."""
    order = await DB.execute(select(Order).where(Order.id_order == id))
    order = order.scalars().first()
    if order == None:
        return JSONResponse(status_code=484, content={"message": "Заказ не найден"})
    else:
        return order


@orders_router.post("/api/order{id}", response_model=Union[Main_Order_4, Main_User_4], status_code=status.HTTP_201_CREATED)
async def end_order(id: int, DB: AsyncSession = Depends(get_session)):
    '''Завершить заказ.'''
    order = await DB.execute(select(Order).where(Order.id_order == id))
    order = order.scalars().first()
    if order == None:
        return JSONResponse(status_code=484, content={"message": "Заказ не найден"})
    else:
        if order.status == 2:
            return JSONResponse(status_code=484, content={"message": "Заказ уже завершён"})

        user = await DB.execute(select(User).where(User.active_order == {"order_id": order.id_order, "order_name": order.name}))
        user = user.scalars().first()
        user.active_order = {}
        order.status = 2
        await DB.commit()
        await DB.refresh(order)

        user.time_end = datetime.datetime.today().timestamp()
        try:
            user.counter_ord = user.counter_ord + 1
        except:
            user.counter_ord = 0
            user.counter_ord = user.counter_ord + 1
        if datetime.datetime.today().timestamp() - user.time_start_work > 86400:
            try:
                user.avg_day_orders = (user.avg_day_orders + user.counter_ord) / 2
            except:
                user.avg_day_orders = user.counter_ord
            user.counter_ord = 0
        try:
            user.avg_list_time = [str(round(user.time_end - user.time_start))] + user.avg_list_time
        except:
            user.avg_list_time = [str(round(user.time_end - user.time_start))]

        this_time  = str(datetime.timedelta(seconds=sum(map(int, user.avg_list_time))/len(user.avg_list_time)))
        user.avg_order_complete_time = datetime.datetime.strptime(this_time, '%H:%M:%S')

        await DB.commit()
        await DB.refresh(user)
        return order
