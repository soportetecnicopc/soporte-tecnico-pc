from flask import Blueprint, render_template, request, redirect, url_for
from models.usuarios import obtener_usuarios, agregar_usuario, obtener_usuario_por_id, actualizar_usuario, eliminar_usuario

usuarios_bp = Blueprint("usuarios", __name__)

# 📌 Listar y registrar usuarios
@usuarios_bp.route("/usuarios", methods=["GET", "POST"])
def listar_usuarios():
    if request.method == "POST":
        nombre_usuario = request.form["nombre_usuario"]
        password = request.form["password"]
        rol = request.form["rol"]

        agregar_usuario(nombre_usuario, password, rol)
        return redirect(url_for("usuarios.listar_usuarios"))

    registros = obtener_usuarios()
    return render_template("usuarios.html", registros=registros)


# 📌 Editar usuario
@usuarios_bp.route("/usuarios/editar/<int:id_usuario>", methods=["GET", "POST"])
def editar_usuario(id_usuario):
    usuario = obtener_usuario_por_id(id_usuario)

    if request.method == "POST":
        nombre_usuario = request.form["nombre_usuario"]
        rol = request.form["rol"]
        password = request.form.get("password")  # opcional

        actualizar_usuario(id_usuario, nombre_usuario, rol, password if password else None)
        return redirect(url_for("usuarios.listar_usuarios"))

    return render_template("editar_usuario.html", usuario=usuario)


# 📌 Eliminar usuario
@usuarios_bp.route("/usuarios/eliminar/<int:id_usuario>", methods=["POST"])
def eliminar_usuario_route(id_usuario):
    eliminar_usuario(id_usuario)
    return redirect(url_for("usuarios.listar_usuarios"))
