from flask import Blueprint, render_template, request, redirect, url_for
from db import get_db
import models.tickets as tickets
import models.estados as estados

tickets_bp = Blueprint('tickets', __name__, url_prefix='/tickets')

# Listar y gestionar tickets (vista interna)
@tickets_bp.route('/', methods=['GET', 'POST'])
def gestionar_tickets():
    # Bloque para guardar ticket cuando se envía el formulario
    if request.method == 'POST':
        id_cliente = request.form['id_cliente']
        id_equipo = request.form['id_equipo']
        numero_ticket = request.form['numero_ticket']

        # Guardar ticket en la base
        tickets.crear_ticket(id_cliente, id_equipo, numero_ticket)

        # Redirigir para evitar reenvío del formulario
        return redirect(url_for('tickets.gestionar_tickets'))

    # Bloque para listar tickets
    db = get_db()
    with db.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT t.id_ticket, t.numero_ticket, t.estado, t.fecha_creacion,
                   c.nombres, c.apellidos,
                   e.marca, e.modelo
            FROM tickets t
            JOIN equipos e ON t.id_equipo = e.id_equipo
            JOIN clientes c ON e.id_cliente = c.id_cliente
            ORDER BY t.fecha_creacion DESC
        """)
        tickets_list = cursor.fetchall()

    with db.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT id_cliente, nombres, apellidos FROM clientes")
        clientes = cursor.fetchall()

        cursor.execute("SELECT id_equipo, marca, modelo FROM equipos")
        equipos = cursor.fetchall()

    return render_template("tickets.html", clientes=clientes, equipos=equipos, tickets=tickets_list)


# Cambiar estado (interno)
@tickets_bp.route('/cambiar_estado', methods=['POST'])
def cambiar_estado():
    id_ticket = request.form['id_ticket']
    nuevo_estado = request.form['estado']

    tickets.actualizar_estado(id_ticket, nuevo_estado)
    estados.registrar_estado(id_ticket, nuevo_estado)

    return redirect(url_for('tickets.gestionar_tickets'))

# Ver historial de estados
@tickets_bp.route('/estados/<int:id_ticket>')
def ver_estados(id_ticket):
    db = get_db()
    with db.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT e.estado, e.fecha
            FROM estados_ticket e
            WHERE e.id_ticket = %s
            ORDER BY e.fecha ASC
        """, (id_ticket,))
        estados_list = cursor.fetchall()

    if not estados_list:
        return f"No se encontró historial para el ticket {id_ticket}"

    return render_template("estados_ticket.html", estados=estados_list, id_ticket=id_ticket)

# Consultar estado por número de ticket
@tickets_bp.route('/estado/<numero_ticket>')
def consultar_estado(numero_ticket):
    db = get_db()
    with db.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT e.estado, e.fecha, t.id_ticket
            FROM tickets t
            JOIN estados_ticket e ON t.id_ticket = e.id_ticket
            WHERE t.numero_ticket = %s
            ORDER BY e.fecha ASC
        """, (numero_ticket,))
        estados_list = cursor.fetchall()

    if not estados_list:
        return f"No se encontró historial para el ticket {numero_ticket}"

    return render_template("estados_ticket.html", estados=estados_list, id_ticket=estados_list[0]["id_ticket"])

# Consulta pública por cédula (externo)
@tickets_bp.route('/consulta', methods=['GET', 'POST'])
def consulta_cliente():
    equipos = []
    cedula = None

    if request.method == "POST":
        cedula = request.form.get("cedula")

        db = get_db()
        with db.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT e.marca, e.modelo, t.numero_ticket, t.estado, t.fecha_creacion
                FROM clientes c
                JOIN equipos e ON c.id_cliente = e.id_cliente
                JOIN tickets t ON e.id_equipo = t.id_equipo
                WHERE c.cedula = %s
                ORDER BY t.fecha_creacion DESC
            """, (cedula,))
            equipos = cursor.fetchall()

    return render_template("consulta_tickets.html", equipos=equipos, cedula=cedula)

# Tickets por equipo (externo)
@tickets_bp.route('/equipo/<int:id_equipo>')
def tickets_por_equipo(id_equipo):
    db = get_db()
    with db.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT t.id_ticket, t.numero_ticket, t.estado, t.fecha_creacion,
                   e.marca, e.modelo, c.nombres, c.apellidos
            FROM tickets t
            JOIN equipos e ON t.id_equipo = e.id_equipo
            JOIN clientes c ON e.id_cliente = c.id_cliente
            WHERE e.id_equipo = %s
            ORDER BY t.fecha_creacion DESC
        """, (id_equipo,))
        tickets_list = cursor.fetchall()

    return render_template("tickets.html", tickets=tickets_list)
