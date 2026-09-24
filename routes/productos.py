from flask import Blueprint, render_template, request, redirect, url_for
from models.productos import obtener_productos, agregar_producto, obtener_producto_por_id, actualizar_producto, eliminar_producto

productos_bp = Blueprint("productos", __name__)

# 📌 Listar y registrar productos
@productos_bp.route("/productos", methods=["GET", "POST"])
def listar_productos():
    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form.get("descripcion")
        categoria = request.form.get("categoria")
        precio = request.form["precio"]
        stock = request.form["stock"]

        agregar_producto(nombre, descripcion, categoria, precio, stock)
        return redirect(url_for("productos.listar_productos"))

    registros = obtener_productos()
    return render_template("productos.html", registros=registros)


# 📌 Editar producto
@productos_bp.route("/productos/editar/<int:id_producto>", methods=["GET", "POST"])
def editar_producto(id_producto):
    producto = obtener_producto_por_id(id_producto)

    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form.get("descripcion")
        categoria = request.form.get("categoria")
        precio = request.form["precio"]
        stock = request.form["stock"]

        actualizar_producto(id_producto, nombre, descripcion, categoria, precio, stock)
        return redirect(url_for("productos.listar_productos"))

    return render_template("editar_producto.html", producto=producto)


# 📌 Eliminar producto
@productos_bp.route("/productos/eliminar/<int:id_producto>", methods=["POST"])
def eliminar_producto_route(id_producto):
    eliminar_producto(id_producto)
    return redirect(url_for("productos.listar_productos"))
