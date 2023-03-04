from flask import Flask, render_template

app = Flask(__name__)
app.debug = True  # debug mode is required for templates to be reloaded

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    from livereload import Server
    server = Server(app.wsgi_app)
    server.serve(host = '0.0.0.0',port=5000)