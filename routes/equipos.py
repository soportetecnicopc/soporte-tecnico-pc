from flask import Blueprint, render_template, request, redirect, url_for
from models.equipos import obtener_equipos, agregar_equipo, obtener_equipo_por_id, actualizar_equipo, eliminar_equipo
from db import get_db
import models.tickets as tickets
import time

equipos_bp = Blueprint('equipos', __name__, url_prefix='/equipos')

@equipos_bp.route('/', methods=['GET', 'POST'])
def listar_equipos():
    db = get_db()
    if request.method == 'POST':
        # 🔹 Capturar datos del formulario
        id_cliente = request.form.get('id_cliente')
        marca = request.form.get('marca')
        modelo = request.form.get('modelo')
        serie = request.form.get('serie')
        observaciones = request.form.get('observaciones')
        accesorios = request.form.get('accesorios')

        # 🔹 Validar que id_cliente no esté vacío
        if not id_cliente or not id_cliente.isdigit():
            print("⚠️ Error: id_cliente vacío o inválido, no se puede crear ticket.")
            return redirect(url_for('equipos.listar_equipos'))

        id_cliente = int(id_cliente)

        # 🔹 Guardar equipo
        cursor = db.cursor()
        cursor.execute("""
                INSERT INTO equipos (id_cliente, marca, modelo, serie, observaciones, accesorios)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (id_cliente, marca, modelo, serie, observaciones, accesorios))
        db.commit()
        id_equipo = cursor.lastrowid  # ID del equipo recién creado
        cursor.close()

        # 🔹 Crear ticket automáticamente
        numero_ticket = f"T-{id_equipo}-{int(time.time())}"  # número único
        tickets.crear_ticket(db, id_equipo, numero_ticket)

        return redirect(url_for('equipos.listar_equipos'))

    # 🔹 Listado de equipos
    with db.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT e.id_equipo, e.marca, e.modelo, e.serie, e.observaciones, e.accesorios,
                   c.id_cliente, c.nombres, c.apellidos
            FROM equipos e
            JOIN clientes c ON e.id_cliente = c.id_cliente
            ORDER BY e.id_equipo DESC
        """)
        registros = cursor.fetchall()

    # 🔹 Clientes para el formulario
    with db.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT id_cliente, nombres, apellidos FROM clientes")
        clientes = cursor.fetchall()

    return render_template("equipos.html", registros=registros, clientes=clientes)


# 📌 Editar equipo
@equipos_bp.route("/equipos/editar/<int:id_equipo>", methods=["GET", "POST"])
def editar_equipo(id_equipo):
    equipo = obtener_equipo_por_id(id_equipo)
    clientes = obtener_clientes()

    if request.method == "POST":
        id_cliente = request.form["id_cliente"]
        marca = request.form["marca"]
        modelo = request.form["modelo"]
        serie = request.form.get("serie")
        observaciones = request.form.get("observaciones")
        accesorios = request.form.get("accesorios")

        actualizar_equipo(id_equipo, id_cliente, marca, modelo, serie, observaciones, accesorios)
        return redirect(url_for("equipos.listar_equipos"))

    return render_template("editar_equipo.html", equipo=equipo, clientes=clientes)


# 📌 Eliminar equipo
@equipos_bp.route("/eliminar/<int:id_equipo>", methods=["POST"])
def eliminar_equipo_route(id_equipo):
    eliminar_equipo(id_equipo)
    return redirect(url_for("equipos.listar_equipos"))
