from flask import Blueprint, render_template, send_file
from models.clientes import obtener_clientes
from models.productos import obtener_productos
from models.movimientos import obtener_movimientos
import pdfkit  # librería para generar PDF
import io  # para manejar archivos en memoria
from flask import send_file

#configuración de pdfkit para usar wkhtmltopdf
path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  # Cambia esta ruta según tu instalación
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)


informes_bp = Blueprint("informes", __name__)

@informes_bp.route("/informes/pdf")
def generar_pdf():
    clientes = obtener_clientes()
    productos = obtener_productos()
    movimientos = obtener_movimientos()
    html = render_template("informes_pdf.html", clientes=clientes, productos=productos, movimientos=movimientos)
    pdf = pdfkit.from_string(html, False, configuration=config)
    return send_file(
        io.BytesIO(pdf),
        as_attachment=True,
        download_name="informe_general.pdf",
        mimetype="application/pdf"
    )

@informes_bp.route("/informes")
def mostrar_informes():
    clientes = obtener_clientes()
    productos = obtener_productos()
    movimientos = obtener_movimientos()

    # Datos para gráficos
    nombres_productos = [p["nombre"] for p in productos]
    stock_productos = [p["stock"] for p in productos]

    # Proyección de ventas (ejemplo simple)
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio"]
    ventas_proyectadas = [sum(m["cantidad"] for m in movimientos if m["tipo"] == "salida") // len(meses)] * len(meses)

    return render_template(
        "informes.html",
        clientes=clientes,
        productos=productos,
        movimientos=movimientos,
        nombres_productos=nombres_productos,
        stock_productos=stock_productos,
        meses=meses,
        ventas_proyectadas=ventas_proyectadas
    )