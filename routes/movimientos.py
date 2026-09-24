from db import get_db
from flask import Blueprint, render_template, request, redirect, url_for
from models.movimientos import obtener_movimientos, agregar_movimiento, obtener_movimiento_por_id, actualizar_movimiento, eliminar_movimiento
from models.productos import obtener_productos, obtener_stock, actualizar_stock
from models.movimientos import obtener_kardex_por_producto
from datetime import datetime
import pdfkit
from flask import make_response



# 👉 Aquí defines el Blueprint
movimientos_bp = Blueprint("movimientos", __name__)

# 📌 Listar y registrar movimientos
@movimientos_bp.route("/movimientos", methods=["GET", "POST"])
def listar_movimientos():
    if request.method == "POST":
        id_producto = request.form["id_producto"]
        tipo = request.form["tipo"]
        motivo = request.form["motivo"]  # Obtener el motivo del formulario
        cantidad = int(request.form["cantidad"])
        observaciones = request.form.get("observaciones")

        # Validación: no permitir stock negativo en salidas
        if tipo == "salida":
            stock_actual = obtener_stock(id_producto)
            if stock_actual < cantidad:
                flash("❌ No hay suficiente stock disponible para este movimiento", "error")
                return redirect(url_for("movimientos.listar_movimientos"))
            actualizar_stock(id_producto, "salida", cantidad)
        else:
            actualizar_stock(id_producto, "entrada", cantidad)

        agregar_movimiento(id_producto, tipo, motivo, cantidad, observaciones)
        return redirect(url_for("movimientos.listar_movimientos"))

    registros = obtener_movimientos()
    productos = obtener_productos()
    return render_template("movimientos.html", registros=registros, productos=productos)

# 📌 Editar movimiento
@movimientos_bp.route("/movimientos/editar/<int:id_movimiento>", methods=["GET", "POST"])
def editar_movimiento(id_movimiento):
    movimiento = obtener_movimiento_por_id(id_movimiento)
    productos = obtener_productos()

    if request.method == "POST":
        id_producto = request.form["id_producto"]
        tipo = request.form["tipo"]
        motivo = request.form["motivo"]  # Obtener el motivo del formulario
        cantidad = int(request.form["cantidad"])
        observaciones = request.form.get("observaciones")

        # Validación en edición
        if tipo == "salida":
            stock_actual = obtener_stock(id_producto)
            if stock_actual < cantidad:
                flash("❌ No hay suficiente stock disponible para este movimiento", "error")
                return redirect(url_for("movimientos.editar_movimiento", id_movimiento=id_movimiento))
            actualizar_stock(id_producto, "salida", cantidad)
        else:
            actualizar_stock(id_producto, "entrada", cantidad)

        actualizar_movimiento(id_movimiento, id_producto, tipo, motivo, cantidad, observaciones)
        return redirect(url_for("movimientos.listar_movimientos"))

    return render_template("editar_movimiento.html", movimiento=movimiento, productos=productos)

# 📌 Obtener movimientos
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

# 📌 Agregar movimiento
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

# 📌 Obtener movimiento por ID
def obtener_movimiento_por_id(id_movimiento):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM movimientos WHERE id_movimiento = %s", (id_movimiento,))
    resultado = cursor.fetchone()
    cursor.close()
    db.close()
    return resultado

# 📌 Actualizar movimiento
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

# 📌 Eliminar movimiento
@movimientos_bp.route("/movimientos/eliminar/<int:id_movimiento>", methods=["POST"])
def eliminar_movimiento_route(id_movimiento):
    eliminar_movimiento(id_movimiento)
    return redirect(url_for("movimientos.listar_movimientos"))


# Ruta para ver el Kardex en HTML
@movimientos_bp.route("/movimientos/kardex/<int:id_producto>", methods=["GET"])
def kardex_producto(id_producto):
    kardex = obtener_kardex_por_producto(id_producto)
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template("kardex.html", kardex=kardex, fecha_actual=fecha_actual)

# Ruta para exportar el Kardex en PDF
@movimientos_bp.route("/movimientos/kardex/pdf/<int:id_producto>", methods=["GET"])
def kardex_pdf(id_producto):
    kardex = obtener_kardex_por_producto(id_producto)
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = render_template("kardex.html", kardex=kardex, fecha_actual=fecha_actual)
    pdf = pdfkit.from_string(html, False)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=kardex.pdf"
    return response