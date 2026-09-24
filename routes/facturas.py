from flask import Blueprint, render_template, make_response, request, redirect, url_for
from weasyprint import HTML
from db import get_db
from models.facturas import obtener_factura, obtener_cliente, obtener_detalle_factura
from models.configuracion import obtener_configuracion
from decimal import Decimal

# 🔹 Definir el blueprint
facturas_bp = Blueprint("facturas", __name__, url_prefix="/facturas")


# Ruta para mostrar formulario de nueva factura
@facturas_bp.route("/", methods=["GET"])
def mostrar_formulario():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Obtener clientes y productos para el formulario
    cursor.execute("SELECT id_cliente, nombres, apellidos FROM clientes")
    clientes = cursor.fetchall()

    cursor.execute("SELECT id_producto, nombre, precio FROM productos")
    productos = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("factura_form.html", clientes=clientes, productos=productos)


# Ruta para crear factura
@facturas_bp.route("/crear", methods=["POST"])
def crear_factura():
    id_cliente = request.form["id_cliente"]
    id_producto = request.form["id_producto"]
    cantidad = int(request.form["cantidad"])

    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Obtener precio base del producto
    cursor.execute("SELECT precio FROM productos WHERE id_producto = %s", (id_producto,))
    producto = cursor.fetchone()
    precio_unitario = producto["precio"]

    # Obtener configuración (IVA y ganancia)
    config = obtener_configuracion()
    iva = float(config["iva_porcentaje"])
    ganancia = float(config["ganancia_porcentaje"])

    # Calcular valores
    precio_unitario = Decimal(producto["precio"])
    iva = Decimal(config["iva_porcentaje"])
    ganancia = Decimal(config["ganancia_porcentaje"])

    precio_con_ganancia = precio_unitario + (precio_unitario * ganancia / Decimal(100))
    subtotal = precio_con_ganancia * cantidad
    iva_total = subtotal * (iva / Decimal(100))
    total = subtotal + iva_total
    
    # Crear factura
    cursor.execute("INSERT INTO facturas (id_cliente, total) VALUES (%s, %s)", (id_cliente, total))
    id_factura = cursor.lastrowid

    # Insertar detalle con cálculos completos
    cursor.execute("""
        INSERT INTO detalle_factura (id_factura, id_producto, cantidad, precio_unitario, 
                                     precio_con_ganancia, subtotal, iva, total)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (id_factura, id_producto, cantidad, precio_unitario, precio_con_ganancia, subtotal, iva_total, total))

    # Actualizar stock
    cursor.execute("UPDATE productos SET stock = stock - %s WHERE id_producto = %s", (cantidad, id_producto))

    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for("facturas.generar_pdf", id_factura=id_factura))


@facturas_bp.route("/pdf/<int:id_factura>")
def generar_pdf(id_factura):
    factura = obtener_factura(id_factura)
    cliente = obtener_cliente(factura["id_cliente"])
    detalle = obtener_detalle_factura(id_factura)

    # Obtener datos principales
    subtotal_global = sum(item["subtotal"] for item in detalle)
    iva_global = sum(item["iva"] for item in detalle)
    total_global = sum(item["total"] for item in detalle)
    
    # Renderizar HTML con los valores calculados
    html = render_template("factura.html", factura=factura, cliente=cliente, detalle=detalle, subtotal=subtotal_global, iva=iva_global, total=total_global)
    
     # Generar PDF con WeasyPrint
    pdf = HTML(string=html).write_pdf()

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"inline; filename=factura_{id_factura}.pdf"
    return response
