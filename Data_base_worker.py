import pandas
import sqlalchemy
from sqlalchemy import Column, Integer, String, Binary, create_engine, exc, orm, engine
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()

Link_len = 255
Name_len = 255
Type_len = 255
Activity_string_len = 255
City_name_len = 255
Country_name_len = 255
Description_len = 255
Date_string_len = 255
Status_len = 255
Post_len = 500
Vec_column = Column(String(1000))


class Groups(Base):
    __tablename__ = "Group"
    base_id = Column(Integer, primary_key=True)
    vk_id = Column(Integer)
    link = Column(String(Link_len))


class Main_group_info(Base):
    __tablename__ = "Main_group_info"
    group_id = Column(Integer, primary_key=True)
    name = Column(String(Name_len))
    screen_name = Column(String(Name_len))
    is_closed = Column(Binary)
    deactivated = Column(Binary)
    group_type = Column(String(Type_len))
    has_photo = Column(Binary)
    photo_50 = Column(String(Link_len))
    photo_100 = Column(String(Link_len))
    photo_200 = Column(String(Link_len))


class Additional_group_info(Base):
    __tablename__ = "Additional_group_info"
    group_id = Column(Integer, primary_key=True)
    activity = Column(String(Activity_string_len))
    age_limits = Column(Integer)
    city = Column(String(City_name_len))
    country = Column(String(Country_name_len))
    description = Column(String(Description_len))
    members_count = Column(Integer)
    public_date_label = Column(String(Date_string_len))
    site = Column(String(Link_len))
    status = Column(String(Status_len))
    verified = Column(Binary)
    wiki_page = Column(String(Link_len))


class Update_date(Base):
    __tablename__ = "Update_date"
    group_id = Column(Integer, primary_key=True)
    date = Column(String(Date_string_len))


class Update_plan(Base):
    __tablename__ = "Update_plan"
    group_id = Column(Integer, primary_key=True)
    take_vk_info = Column(Binary)
    take_vec = Column(Binary)



class Vecs(Base):
    __tablename__ = "Vec"
    group_id = Column(Integer, primary_key=True)
    vec = Vec_column


class Posts(Base):
    __tablename__ = "Posts"
    group_id = Column(Integer, primary_key=True)
    post1 = Column(String(Post_len))
    #x100

class Vecs_Story(Base):
    __tablename__ = "Vec_Story"
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer)
    date = Column(String(Date_string_len))
    vec = Vec_column