import pandas
import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, Binary, MetaData, create_engine, exc, orm, engine, ForeignKey, \
    Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, Session
import os
import random

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
Vec_column_len = 1000
metadata = MetaData
"""
Groups_table = Table('Groups', metadata,
                     Column('group_id', Integer, primary_key=True),
                     Column('vk_id', Integer),
                     Column("link", String(Link_len)),
                     Column("name", String(Name_len)),
                     Column("screen_name", String(Name_len)),
                     Column("is_closed", Binary),
                     Column("deactivated", Binary),
                     Column("group_type", String(Type_len)),
                     Column("has_photo", Binary),
                     Column("photo_50", String(Link_len)),
                     Column("photo_100", String(Link_len)),
                     Column("photo_200", String(Link_len)),
                     Column("activity", String(Activity_string_len)),
                     Column("age_limits", Integer),
                     Column("city", String(City_name_len)),
                     Column("country", String(Country_name_len)),
                     Column("description", String(Description_len)),
                     Column("members_count", Integer),
                     Column("public_date_label", String(Date_string_len)),
                     Column("site", String(Link_len)),
                     Column("status", String(Status_len)),
                     Column("verified", Binary),
                     Column("wiki_page", String(Link_len)),
                     Column("update_posts_time", String(Date_string_len)),
                     Column("update_vec_time", String(Date_string_len))
                     )

Posts_table = Table("Posts", metadata,
                    Column('vec_id', Integer, primary_key=True),
                    "..."
                    )
Vecs_story_table = Table("Vec_story", metadata,
                         Column('id', Integer, primary_key=True),
                         Column('group', Integer, ForeignKey('Groups.group_id')),
                         Column("Date_of_info", String(Date_string_len), ForeignKey('Groups.update_posts_time')),
                         Column("n1", Boolean),
                         Column("n1", Boolean),
                         )
"""


def Check_database():
    # engine = create_engine('sqlite:////test.db', convert_unicode=True)
    # db_session = scoped_session(sessionmaker(
    #    autocommit=False, autoflush=False, bind=engine))
    with sqlalchemy.create_engine('sqlite:///test.db').connect() as connection:
        if not os.path.exists("test.db"):
            Create_database(connection)
            Base.metadata.create_all(bind=engine)
            connection.execute("commit")


def Create_database(connection):
    connection.execute('CREATE DATABASE my_database')
    connection.execute("commit")


class Groups(Base):
    __tablename__ = "Group"
    base_id = Column(Integer, primary_key=True)
    vk_id = Column(Integer)
    link = Column(String(Link_len))
    # ____________Main_info_________________
    name = Column(String(Name_len))
    screen_name = Column(String(Name_len))
    is_closed = Column(Binary)
    deactivated = Column(Binary)
    group_type = Column(String(Type_len))
    has_photo = Column(Binary)
    photo_50 = Column(String(Link_len))
    photo_100 = Column(String(Link_len))
    photo_200 = Column(String(Link_len))
    # ___________Add_info____________________
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
    # __________Updates______________________
    wall_update_date = Column(String(Date_string_len))  # ForeignKey(Wall.wall_update_date)
    vec_update_date = Column(String(Date_string_len))  # ForeignKey(Vecs_Story.vec_update_date)

    def __repr__(self):
        return "<Group(%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r)>" \
               % self.base_id, self.vk_id, self.link, self.name, self.screen_name, self.is_closed, self.deactivated, \
               self.group_type, self.has_photo, self.photo_50, self.photo_100, self.photo_200, self.activity, \
               self.age_limits, self.city, self.country, self.description, self.members_count, self.public_date_label, \
               self.site, self.status, self.verified, self.wiki_page, self.wall_update_date, self.vec_update_date


class Posts(Base):  # !!!!!!
    __tablename__ = "Posts"
    post_id = Column(Integer, primary_key=True)
    attr1 = Column(String(Post_len))

    def __repr__(self):
        return "<Post(%r)>" % self.attr1


class Wall(Base):
    __tablename__ = "Wall"
    wall_id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey(Groups.base_id))
    wall_update_date = Column(String(Date_string_len))
    gr_post_id = Column(String(Post_len), ForeignKey(Posts.post_id))
    # x100


class Vecs_Story(Base):
    __tablename__ = "Vec_Story"
    vec_id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey(Groups.base_id))
    vec_update_date = Column(String(Date_string_len))
    v1 = Column(Integer)


if __name__ == "__main__":
    Check_database()
    my_engine = sqlalchemy.create_engine('sqlite:///test.db')
    #Post1= Posts(attr1="ma1")
    #print()
    Base.metadata.create_all(my_engine)
    session=Session(bind=my_engine)
    #session.add(Post1)
    #session.commit()
    print(session.query(Posts).first())
"""
    db_session = scoped_session(sessionmaker(
        autocommit=False, autoflush=False, bind=engine))
    Base.query = db_session.query_property()
    # connection.execute("commit")
    Groups.Add_to_base(1132, "link", connection)
    print()
"""
