
# Importar todos los Blueprints
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from flask import Flask, render_template, redirect, url_for, request, session
from db import get_db
import bcrypt

#importacion de modelos
import models.tickets as tickets
import models.estados as estados

# Blueprints
from routes.clientes import clientes_bp
from routes.equipos import equipos_bp
from routes.productos import productos_bp
from routes.movimientos import movimientos_bp
from routes.usuarios import usuarios_bp
from routes.informes import informes_bp
from routes.tickets import tickets_bp
from routes.facturas import facturas_bp
from routes.reportes import reportes_bp
from routes.configuracion import configuracion_bp  # Importar el Blueprint de configuración

app = Flask(__name__)
# 🔹 Clave secreta para manejar sesiones
app.secret_key = "una_clave_unica_y_segura"

# configuracoin de loginmanager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirige a la página de login si no está autenticado  

# Clase Usuario para Flask-Login
class Usuario(UserMixin):
    def __init__(self, id_usuario, nombre_usuario, rol):
        self.id = id_usuario
        self.nombre = nombre_usuario
        self.rol = rol

# Recuperar usuario desde la BD
@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    with db.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario=%s", (user_id,))
        usuario = cursor.fetchone()
        if usuario:
            return Usuario(usuario["id_usuario"], usuario["nombre_usuario"], usuario["rol"])
        return None


# Registrar Blueprints
app.register_blueprint(clientes_bp)
app.register_blueprint(equipos_bp)
app.register_blueprint(productos_bp)
app.register_blueprint(movimientos_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(informes_bp)
app.register_blueprint(tickets_bp) 
app.register_blueprint(facturas_bp)
app.register_blueprint(reportes_bp)
app.register_blueprint(configuracion_bp)  # Registrar el Blueprint de configuración
# 📌 Ruta principal protegida
@app.route("/")
@login_required
def index():
    return render_template("index.html", usuario=current_user.nombre)


# 📌 Ruta de login
@app.route("/login", methods=["GET", "POST"])
def login():
    db = get_db()
    with db.cursor(dictionary=True) as cursor:
        if request.method == "POST":
            nombre_usuario = request.form.get("nombre_usuario")
            password = request.form.get("password")

            cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario=%s", (nombre_usuario,))
            usuario = cursor.fetchone()

            if usuario and bcrypt.checkpw(password.encode("utf-8"), usuario["password"].encode("utf-8")):
                user = Usuario(usuario["id_usuario"], usuario["nombre_usuario"], usuario["rol"])
                login_user(user)
                return redirect(url_for("index"))
            else:
                return render_template("login.html", error="Usuario o contraseña incorrectos")

        return render_template("login.html")

# 📌 Ruta de logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)
