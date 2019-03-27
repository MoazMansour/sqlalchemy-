#!/usr/bin/env python3

import sys
from sqlalchemy import Column, ForiegnKey, Integer, String
from sqlalchemy.ext.decalartive import decalartive_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = decalartive_base()

class Restaurant(Base):
    __tablename__ = 'restaurant'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

class MenuItem(Base):
    __tablename__ = 'menu_item'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForiegnKey('restaurant.id'))
    restaurant = relationship(Restaurant)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
