from flask import Flask

# modules
from api.institucion.main import institucion
from api.proyecto.main import proyecto
from api.usuario.main import usuario

# models
from models import db

app = Flask(__name__)
# config
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kurobnwo:bw0xqio5t6CoPfpftCL9nQ3GbXpUDJxQ@baasu.db.elephantsql.com/kurobnwo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Blueprints
app.register_blueprint(institucion, url_prefix='/institucion')
app.register_blueprint(proyecto, url_prefix='/proyectos')
app.register_blueprint(usuario, url_prefix='/usuarios')

db.init_app(app)

if __name__ == 'main':
    app.run(load_dotenv=True)