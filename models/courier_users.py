from typing import Union, Annotated
import datetime
from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Integer, DATETIME, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base
from enum import Enum

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id_user = Column(Integer, primary_key=True)
    name = Column(String)
    avg_order_complete_time = Column(DATETIME)
    avg_day_orders = Column(Integer)
    district = Column(ARRAY(String))
    active_order = Column(JSONB)
    avg_list_time = Column(ARRAY(String))
    time_start = Column(Integer)
    time_end = Column(Integer)
    counter_ord = Column(Integer)
    time_start_work = Column(Integer)

class Main_User_1(BaseModel):
    id_user: Annotated[Union[int, None], Field(default=100, ge=1, lt=288)] = None

class Main_User_2(Main_User_1):
    name: Union[str, None] = None
    district: Union[list, None] = None

class Main_User_3(BaseModel):
    name: Union[str, None] = None
    district: Union[list, None] = None

class Main_User_5(Main_User_1):
    name: Union[str, None] = None
    district: Union[list, None] = None
    active_order: Union[dict, None] = None
    avg_order_complete_time: Union[datetime.time, None] = None
    avg_day_orders: Union[int, None] = None

class Main_User_4(Main_User_1):
    district: Union[list, None] = None
    active_order: Union[dict, None] = None
    avg_order_complete_time: Union[datetime.time, None] = None
    avg_day_orders: Union[int, None] = None
    avg_list_time: Union[list, None] = None
    time_start: Union[int, None] = None
    time_end: Union[int, None] = None
    counter_ord: Union[int, None] = None
    time_start_work: Union[int, None] = None    