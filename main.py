from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import urlfetch

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('index.html', {'titulo':'Serpientes y Aviones'}))

# Manejo de Usuarios
class User_accounts(webapp.RequestHandler):
    def get(self):
        # obtenemos el usuario logueado
        usuario = users.get_current_user()
        if usuario:
            #si el usuario esta logueado, le damos la bienvenida, lo persistimos y mostramos todos los usuarios registrados
            todos_usuarios = db.Query(Usuarios)
            todos_usuarios.filter('email',usuario.email())
            todos_usuarios = todos_usuarios.fetch(limit=1)
            if not todos_usuarios:
                save = Usuarios(nickname=usuario.nickname(),email=usuario.email())
                save.put()
                message = 'Su usuario ha sido registrado'
            else:
                message = 'Sus datos de usuario son:'

            self.response.out.write('<h1>Bienvenido %(nicename)s <a href="%(logout)s" > log out </a></h1> <br> %(mensaje)s <br>' % {'nicename':usuario.nickname(),'logout':users.create_logout_url('/users'),'mensaje':message})
            for p in todos_usuarios:
                self.response.out.write('%(nickname)s - %(email)s <br>' % {'nickname': p.nickname,'email': p.email})
        else:
            # si no esta logueado, le damos la posibilidad de hacerlo
            self.redirect(users.create_login_url('/users'))

class ErrorTest(webapp.RequestHandler):
    def get(self):
        number = self.request.get('number')
        if 0 <= int(number) <= 10 :
            self.response.out.write('El numero ingresado es %s' % number)
        else:
            self.error(404)

class Url_fetch(webapp.RequestHandler):
    def get(self):
        url = "http://www.google.com/"
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            self.response.out.write(result.content)

class Usuarios(db.Model):
    nickname = db.StringProperty(multiline=False)
    email = db.EmailProperty()

app = webapp.WSGIApplication([('/',MainPage),('/users',User_accounts),('/errors',ErrorTest),('/url',Url_fetch)],debug=True)