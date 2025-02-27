# Declarando nombre de la aplicación e inicializando, crear la aplicación Flask
from app import app
#from route import  route_dropdown


# Importando todos mis Routers (Rutas)
from routers.router_login import *
from routers.router_home import *
from routers.router_page_not_found import *


# Ejecutando el objeto Flask
if __name__ == '__main__':
    #app.run(debug=False, port=5600) para trabajar localmente
    app.run(host='0.0.0.0',port=5600)  #para trabajar desde la red local