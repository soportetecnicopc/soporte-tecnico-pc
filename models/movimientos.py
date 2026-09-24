from flask import Blueprint, render_template, request, redirect, url_for
from models.productos import actualizar_stock, obtener_productos, agregar_producto, obtener_producto_por_id, actualizar_producto, eliminar_producto
from db import get_db

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

# agregar ruta para obtener movimientos
def agregar_movimiento(id_producto, tipo, motivo, cantidad, observaciones):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO movimientos (id_producto, tipo, motivo, cantidad, fecha, observaciones)
        VALUES (%s, %s, %s, %s, NOW(), %s)
    """, (id_producto, tipo, motivo, cantidad, observaciones))
    db.commit()

    # Actualizar stock automáticamente
    if tipo == "entrada":
        actualizar_stock(id_producto, "entrada", int(cantidad))
    elif tipo == "salida":
        actualizar_stock(id_producto, "salida", int(cantidad))

    cursor.close()
    db.close()


#obtenemos un movimiento por su ID
def obtener_movimiento_por_id(id_movimiento):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT m.id_movimiento, m.id_producto, m.tipo, m.motivo, m.cantidad, m.fecha, m.observaciones,
               p.nombre
        FROM movimientos m
        JOIN productos p ON m.id_producto = p.id_producto
        WHERE m.id_movimiento = %s
    """, (id_movimiento,))
    resultado = cursor.fetchone()
    cursor.close()
    db.close()
    return resultado



# obtener producto.
def obtener_movimientos():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT m.id_movimiento, m.id_producto, m.tipo, m.motivo, m.cantidad, m.fecha, m.observaciones,
               p.nombre
        FROM movimientos m
        JOIN productos p ON m.id_producto = p.id_producto
        ORDER BY m.fecha DESC
    """)
    resultados = cursor.fetchall()
    cursor.close()
    db.close()
    return resultados



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



# obtener movimientos
def obtener_movimientos():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT m.id_movimiento, m.id_producto, m.tipo, m.motivo, m.cantidad, m.fecha, m.observaciones,
               p.nombre AS producto
        FROM movimientos m
        JOIN productos p ON m.id_producto = p.id_producto
        ORDER BY m.fecha DESC
    """)
    resultados = cursor.fetchall()
    cursor.close()
    db.close()
    return resultados

def agregar_movimiento(id_producto, tipo, motivo, cantidad, observaciones):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO movimientos (id_producto, tipo, motivo, cantidad, fecha, observaciones)
        VALUES (%s, %s, %s, %s, NOW(), %s)
    """, (id_producto, tipo, motivo, cantidad, observaciones))
    db.commit()
    cursor.close()
    db.close()

    # 🔥 Actualizamos stock automáticamente
    actualizar_stock(id_producto, tipo, int(cantidad))

def obtener_movimiento_por_id(id_movimiento):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT m.*, p.nombre AS producto
        FROM movimientos m
        JOIN productos p ON m.id_producto = p.id_producto
        WHERE m.id_movimiento = %s
    """, (id_movimiento,))
    resultado = cursor.fetchone()
    cursor.close()
    db.close()
    return resultado

def actualizar_movimiento(id_movimiento, id_producto, tipo, motivo, cantidad, observaciones):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE movimientos
        SET id_producto=%s, tipo=%s, motivo=%s, cantidad=%s, observaciones=%s
        WHERE id_movimiento=%s
    """, (id_producto, tipo, motivo, cantidad, observaciones, id_movimiento))
    db.commit()
    cursor.close()
    db.close()

    # 🔥 Ajustamos stock según el movimiento editado
    actualizar_stock(id_producto, tipo, int(cantidad))


def eliminar_movimiento(id_movimiento):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Obtenemos el movimiento antes de eliminarlo
    cursor.execute("SELECT * FROM movimientos WHERE id_movimiento = %s", (id_movimiento,))
    movimiento = cursor.fetchone()

    if movimiento:
        # Revertimos stock según el tipo
        if movimiento["tipo"] == "entrada":
            actualizar_stock(movimiento["id_producto"], "salida", int(movimiento["cantidad"]))
        elif movimiento["tipo"] == "salida":
            actualizar_stock(movimiento["id_producto"], "entrada", int(movimiento["cantidad"]))

        # Eliminamos el movimiento
        cursor.execute("DELETE FROM movimientos WHERE id_movimiento = %s", (id_movimiento,))
        db.commit()

    cursor.close()
    db.close()



def obtener_kardex_por_producto(id_producto):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT m.fecha, m.tipo, m.motivo, m.cantidad, m.observaciones, p.nombre
        FROM movimientos m
        JOIN productos p ON m.id_producto = p.id_producto
        WHERE m.id_producto = %s
        ORDER BY m.fecha ASC
    """, (id_producto,))
    resultados = cursor.fetchall()
    cursor.close()
    db.close()

    # Calcular saldo acumulado en Python
    saldo = 0
    kardex = []
    for r in resultados:
        if r["tipo"] == "entrada":
            saldo += r["cantidad"]
        elif r["tipo"] == "salida":
            saldo -= r["cantidad"]
        r["saldo"] = saldo
        kardex.append(r)

    return kardex
