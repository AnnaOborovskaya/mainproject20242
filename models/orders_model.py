from typing import Union
from models.courier_users import *
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"
    id_order = Column(Integer, primary_key=True)
    name = Column(String)
    district = Column(String)
    status = Column(Integer)
    id_user = Column(Integer, ForeignKey(User.id_user))

class Main_Order_1(BaseModel):
    id_order: Union[int, None] = None

class Main_Order_2(Main_Order_1):
    name: Union[str, None] = None
    district: Union[str, None] = None
    id_user: Union[int, None] = None

class Main_Order_3(Main_Order_1):
    id_user: Union[int, None] = None
    status: Union[int, None] = None

class Main_Order_4(Main_Order_1): #&
    status: Union[int, None] = None

class Main_Order_5(Main_Order_2):
    status: Union[int, None] = None





class Main_Order_5(Main_Order_1):
    name: Union[str, None] = None
    district: Union[str, None] = None
    status: Union[int, None] = None
    id_user: Union[int, None] = None    
