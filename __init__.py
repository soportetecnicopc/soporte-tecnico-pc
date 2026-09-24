from flask import Flask

def create_app():
    app = Flask(__name__)

    # Configuración básica (ejemplo: clave secreta)
    app.config['SECRET_KEY'] = 'tu_clave_secreta'

    # Importar y registrar blueprints de rutas
    from .routes import clientes, tickets
    app.register_blueprint(clientes.bp)
    app.register_blueprint(tickets.bp)

    return app
