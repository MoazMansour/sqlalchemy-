#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

myFristRestaurant = Restaurant(name = "Pizza Palace")
cheesepizza = MenuItem(name = "Chees Pizza",
                        description = '''Made with all natural
                                        ingredien ts and fresh mozzarella''',
                        course = "Entree", price = "$8.99",
                        restaurant = myFristRestaurant)

session.add(myFristRestaurant)
session.add(cheesepizza)
session.commit()
session.query(Restaurant).all()
session.query(MenuItem).all()
