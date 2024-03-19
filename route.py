from directory import Directory
from fichier import Fichier
from render_figure import RenderFigure
from user import User
from event import Event

from mypic import Pic
from javascript import Js
from stylesheet import Css
import re
import traceback
import sys

class Route():
    def __init__(self):
        self.Program=Directory("mon petit guide de python")
        self.Program.set_path("./")
        self.mysession={"notice":None,"email":None,"name":None}
        self.dbUsers=User()
        self.dbEvent=Event()
        self.render_figure=RenderFigure(self.Program)
        self.getparams=("id",)
    def set_my_session(self,x):
          print("set session",x)
          self.Program.set_my_session(x)
          self.render_figure.set_session(self.Program.get_session())
    def set_redirect(self,x):
          self.Program.set_redirect(x)
          self.render_figure.set_redirect(self.Program.get_redirect())
    def render_json(self,x,y):
          self.Program.set_json(Fichier(("./"+x),y).lire())
          return self.render_figure.render_my_json(self.Program.get_json())
    def set_json(self,x):
          self.Program.set_json(x)
          self.render_figure.set_json(self.Program.get_json())
    def set_notice(self,x):
          print("set session",x)
          self.Program.set_session_params({"notice":x})
          self.render_figure.set_session(self.Program.get_session())
    def set_session(self,x):
          print("set session",x)
          self.Program.set_session(x)
          self.render_figure.set_session(self.Program.get_session())
    def get_this_route_param(self,x,params):
          print("set session",x)
          return dict(zip(x,params["routeparams"]))
          
    def logout(self,search):
        self.Program.logout()
        self.set_redirect("/")
        return self.render_figure.render_redirect()
    def login(self,s):
        search=self.get_post_data()(params=("email","password"))
        self.user=self.dbUsers.getbyemailpw(search["email"],search["password"])
        print("user trouve", self.user)
        if self.user["email"] != "":
          self.set_session(self.user)
          self.set_json("{\"redirect\":\"/welcome\"}")
        else:
          self.set_json("{\"redirect\":\"/\"}")
        print("session login",self.Program.get_session())
        return self.render_figure.render_json()
    def voirtouscequejaiajoute(self,params={}):
        self.render_figure.set_param("event",Event().getall())
        return self.render_json("./event","voirtout.json")
    def voirtousevent(self,params={}):
        self.render_figure.set_param("event",Event().getall())
        return self.render_figure.render_figure("event/voirtout.html")
    def voirevent(self,params={}):
        getparams=("id",)
        print("get param, action see my new",getparams)
        myparam=self.get_this_route_param(getparams,params)
        self.render_figure.set_param("event",Event().getbyid(myparam["id"]))
        return self.render_figure.render_figure("welcome/voirevent.html")
    def nouveauevent(self,search={}):
        return self.render_figure.render_figure("event/new.html")
    def sauverevent(self,params={}):
        myparams=self.get_post_data()(params=("user_id","lat","lon","title","pic","date",))
        event=self.dbEvent.create(myparams)
        if event["event_id"]:
          self.set_notice(event["notice"])
          self.set_json("{\"redirect\":\"/seemyevent/"+event["event_id"]+"\"}")
        else:
          self.set_json("{\"redirect\":\"/newevent\"}")
        return self.render_figure.render_json()
    def welcome(self,search):
        return self.render_figure.render_figure("welcome/index.html")
    def delete_user(self,params={}):
        getparams=("id",)
        myparam=self.post_data(self.getparams)
        self.render_figure.set_param("user",User().deletebyid(myparam["id"]))
        self.set_redirect("/welcome")
        return self.render_figure.render_redirect()
    def edit_user(self,params={}):
        getparams=("id",)
        myparam=self.post_data(getparams)
        self.render_figure.set_param("user",User().getbyid(myparam["id"]))
        return self.render_figure.render_figure("welcome/edituser.html")
    def seeuser(self,params={}):
        getparams=("id",)
        print("get param, action see my new",getparams)
        myparam=self.get_this_route_param(getparams,params)
        self.render_figure.set_param("user",User().getbyid(myparam["id"]))
        return self.render_figure.render_figure("welcome/showuser.html")
    def myusers(self,params={}):
        self.render_figure.set_param("users",User().getall())
        return self.render_figure.render_figure("welcome/users.html")
    def set_post_data(self,x):
        self.post_data=x
    def get_post_data(self):
        return self.post_data
    def update_user(self,params={}):
        myparam=self.post_data(self.getparams)
        self.user=self.dbUsers.update(params)
        self.set_session(self.user)
        self.set_redirect(("/seeuser/"+params["id"][0]))
        return self.render_figure.render_redirect()
    def save_user(self,params={}):
        #print("My  f unc",self.post_data)
        myparam=self.get_post_data()(params=("businessaddress","gender","profile","metier", "otheremail", "password","zipcode", "email", "mypic","postaladdress","nomcomplet","password_confirmation"))
        #print("My p  a r a m",myparam)
        self.user=self.dbUsers.create(myparam)
        if self.user["email"]:
          self.set_session(self.user)
          self.set_json("{\"redirect\":\"/welcome\"}")
          return self.render_figure.render_json()
        else:
          self.set_json("{\"redirect\":\"/e\"}")
          return self.render_figure.render_json()
    def data_reach(self,search):
        return self.render_figure.render_figure("welcome/datareach.html")
    def run(self,redirect=False,redirect_path=False,path=False,session=False,params={},url=False,post_data=False):
        if post_data:
            self.set_post_data(post_data)
        if url:
            print("url : ",url)
            self.Program.set_url(url)
        self.set_my_session(session)

        if redirect:
            self.redirect=redirect
        if redirect_path:
            self.redirect_path=redirect
        if not self.render_figure.partie_de_mes_mots(balise="section",text=self.Program.get_title()):
            self.render_figure.ajouter_a_mes_mots(balise="section",text=self.Program.get_title())
        if path and path.endswith("jpg"):
            self.Program=Pic(path)
            self.Program.set_path("./")
        elif path and path.endswith("png"):
            self.Program=Pic(path)
            self.Program.set_path("./")
        elif path and path.endswith(".jfif"):
            self.Program=Pic(path)
        elif path and path.endswith(".css"):
            self.Program=Css(path)
        elif path and path.endswith(".js"):
            self.Program=Js(path)
        elif path:
            print("link route ",path)
            ROUTES={
                    "^/seemyevent/([0-9]+)$":self.voirevent,
                    "^/newevent$":self.nouveauevent,
                    "^/sauverevent$":self.sauverevent,
                    "^/voirtouscequejaiajoute$":self.voirtouscequejaiajoute,
                    "^/allevents$":self.voirtousevent,
                    '^/logmeout$':self.logout,
                    '^/save_user$':self.save_user,
                    '^/update_user$':self.update_user,

                    "^/seeuser/([0-9]+)$":self.seeuser,
                    "^/edituser/([0-9]+)$":self.edit_user,
                    "^/deleteuser/([0-9]+)$":self.delete_user,
                    '^/login$':self.login,

                    '^/welcome$':self.myusers,

                    '^/$': self.welcome,
                    }
            REDIRECT={"/save_user": "/welcome"}
            for route in ROUTES:
               print("pattern=",route)
               mycase=ROUTES[route]
               x=(re.match(route,path))
               print(True if x else False)
               if x:
                    params["routeparams"]=x.groups()
                    try:
                        html=mycase(params)
                    except Exception as e:
                        print("erreur"+str(e),traceback.format_exc())
                        html=("<p>une erreur s'est produite dans le code server  "+(traceback.format_exc())+"</p><a href=\"/\">retour à l'accueil</a>").encode("utf-8")
                        print(html)
                    self.Program.set_html(html=html)
                    return self.Program
               else:
                    self.Program.set_html(html="<p>la page n'a pas été trouvée</p><a href=\"/\">retour à l'accueil</a>")
        return self.Program
