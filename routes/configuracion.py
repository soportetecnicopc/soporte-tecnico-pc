from flask import Blueprint, render_template, request, redirect, flash
from models.configuracion import obtener_configuracion, actualizar_configuracion
from db import get_db

# Definir el Blueprint
configuracion_bp = Blueprint('configuracion', __name__)

# Ruta principal para ver y actualizar configuración
@configuracion_bp.route('/configuracion', methods=['GET', 'POST'])
def configuracion():
    if request.method == 'POST':
        iva = request.form['iva_porcentaje']
        ganancia = request.form['ganancia_porcentaje']
        stock = request.form['stock_minimo']
        actualizar_configuracion(iva, ganancia, stock)
        flash('Configuración actualizada correctamente.')
        return redirect('/configuracion')
    
    config = obtener_configuracion()
    return render_template('configuracion.html', config=config)

# Función para calcular precio final de un producto
def calcular_precio_final(precio_base):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM configuracion LIMIT 1")
    config = cursor.fetchone()
    cursor.close()
    db.close()

    iva = float(config["iva_porcentaje"])
    ganancia = float(config["ganancia_porcentaje"])

    precio_con_ganancia = precio_base + (precio_base * ganancia / 100)
    precio_final = precio_con_ganancia + (precio_con_ganancia * iva / 100)

    return round(precio_final, 2)

# Función para inicializar configuración si no existe
def inicializar_configuracion():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM configuracion")
    (count,) = cursor.fetchone()
    if count == 0:
        cursor.execute("""
            INSERT INTO configuracion (iva_porcentaje, ganancia_porcentaje, stock_minimo)
            VALUES (12.00, 20.00, 5)
        """)
        db.commit()
    cursor.close()
    db.close()
