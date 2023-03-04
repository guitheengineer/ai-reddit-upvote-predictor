from livereload import Server
from app import app

flask_app = app()
flask_app.debug = True  # debug mode is required for templates to be reloaded

server = Server(flask_app.wsgi_app)
server.watch(...)
server.serve()