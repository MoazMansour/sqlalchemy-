#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import re

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
session.rollback()

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = '''
                        <html>
                        <body>
                        <a href="/restaurants/new">Create a new Restaurant</a></br></br>
                        '''
                list = session.query(Restaurant).all()
                for restaurant in list:
                    output += " %s </br>" % restaurant.name
                    #objective 4 Step 1 - add an id link
                    output += '<a href="/restaurants/%s/edit"> Edit </a></br>' % restaurant.id
                    output += '<a href="/restaurants/%s/delete"> Delete </a></br>' % restaurant.id
                output += "</ul></body></html>"
                self.wfile.write(output)
                return

            # Objective 3 Step 2 - Create /restarants/new page
            elif self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
                output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return

            # Objective 4 Step 2 - Edit Restaurant page
            elif self.path.endswith("/edit"):
                pattern = re.compile("\/\d+")
                m = pattern.search(self.path)
                target = int(self.path[m.start()+1:m.end()])
                trgt = session.query(Restaurant).filter_by(id=target).one()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1> %s </h1>" % trgt.name
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/%s/edit'>" % target
                output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
                output += "<input type='submit' value='Edit'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return

            # Objective 5 Step 2 - Delete Restaurant page
            elif self.path.endswith("/delete"):
                pattern = re.compile("\/\d+")
                m = pattern.search(self.path)
                target = int(self.path[m.start()+1:m.end()])
                trgt = session.query(Restaurant).filter_by(id=target).one()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1> Are you sure you want to delete %s ?</h1>" % trgt.name
                output += "<form method = 'POST' action = '/restaurants/%s/delete'>" % target
                output += "<input type='submit' value='Yes'></form>"
                output += '<a href="/restaurants"><button>No</button></a></br>'
                output += "</form></body></html>"
                self.wfile.write(output)
                return


        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    # Create new Restaurant Object
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            elif self.path.endswith("/edit"):
                pattern = re.compile("\/\d+")
                m = pattern.search(self.path)
                target = int(self.path[m.start()+1:m.end()])
                change = session.query(Restaurant).filter_by(id=target).one()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    # Create new Restaurant Object
                    change.name = messagecontent[0]
                    session.add(change)
                    session.commit()

                    self.send_response(303)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            elif self.path.endswith("/delete"):
                pattern = re.compile("\/\d+")
                m = pattern.search(self.path)
                target = int(self.path[m.start()+1:m.end()])
                change = session.query(Restaurant).filter_by(id=target).one()

                # delete the Restaurant Object
                session.delete(change)
                session.commit()

                self.send_response(303)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print ("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print (" ^C entered, stopping web server....")
        server.socket.close()

if __name__ == '__main__':
    main()
