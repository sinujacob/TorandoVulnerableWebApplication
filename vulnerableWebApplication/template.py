import tornado.ioloop
import tornado.web
import cgi
import sqlite3 as lite
import os
import tornado.options

def CreateDB():
    con = lite.connect('db.db')
    with con:
        cur = con.cursor()
        cur.execute("SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name = 'tag'")
        x = cur.fetchone()[0]
        print x
        if x==0:
            cur.execute("CREATE TABLE tag(username varchar(20), password varchar(20))")
            con.commit()
        return x    
     

class LoginXss(tornado.web.RequestHandler):
        def get(self):
                return self.render('index.html')

class HomeHandler(tornado.web.RequestHandler):
   
    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password") 
        con = lite.connect('db.db')
        with con:
            cur = con.cursor()
            cur.execute("SELECT count(*) FROM tag WHERE username= %s and password= %s" %("'"+username+"'","'"+password+"'"))
            x=cur.fetchone()[0]
            if x!=0:
                self.write('<html><body bgcolor="#E6E6FA"><p>Welcome ' + username + '</p>'
                            '<a href="/userlist">List All The Users</a><br><br>'
                            '<a href="/dom">DOMXSS Example</a><br><br>'
                            '<a href="/login">Logout</a><br><br>'
                            '<a href="/search">search</a></body></html>')
            else:
                self.write('<html><body><script>alert("Invalid Useraname or Password..!")</script>'
                            '<a href="/login">BackToLogin</a></body></html>')   

class SearchHandler(tornado.web.RequestHandler):

    def get(self):
        return self.render('search.html')

    def post(self):
        username=self.get_argument("username")
        self.write('<html><body><p>Welcome '+username+ '</p></body></html>')
        

class SignupXss(tornado.web.RequestHandler):
    def get(self):
        return self.render("Signup.html")  
        
    def post(self):
        username=self.get_argument("username")
        password=self.get_argument("password")                
        con = lite.connect('db.db')
        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO tag VALUES(?,?)",(username,password))
            self.write('<html><body><script>alert("UserRegistration sucess..!")</script>'
                       '<a href="/login">BackToLogin</a></body></html>')

class ListuserXss(tornado.web.RequestHandler):
    def get(self):
        con = lite.connect('db.db')
        with con:
            cur = con.cursor()
            x=cur.execute("select username from tag")        
                
            for l1 in x:                        
                    self.write(l1[0]) 

class DOMXss(tornado.web.RequestHandler):
        def get(self):
                return self.render("tag.html") 
class DOM(tornado.web.RequestHandler):
        def get(self):
                return self.render("submit.html")                                              
        
               

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
settings={
            "debug": True,
            "template_path": os.path.join(BASE_DIR, "templates"),
            "static_path": os.path.join(BASE_DIR, "static")
        } 

   
def make_app():
    return tornado.web.Application([
        (r"/login", LoginXss),(r"/home",HomeHandler),(r"/signup", SignupXss),(r"/userlist",ListuserXss),(r"/dom",DOMXss),(r"/dom1",DOM),(r"/search",SearchHandler)],**settings)


if __name__ == "__main__":
    try:
        CreateDB()
        app = make_app()
        app.listen(8004)
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.current().stop()
