from flask import Blueprint, render_template, request, redirect, url_for
from models.clientes import obtener_clientes, agregar_cliente, obtener_cliente_por_id, actualizar_cliente, eliminar_cliente
from db import get_db

clientes_bp = Blueprint('clientes', __name__, url_prefix='/clientes')

# 📌 Listar clientes
@clientes_bp.route("/", methods=["GET", "POST"])
def listar_clientes():
    if request.method == "POST":
        # Recibir datos del formulario
        nombres = request.form["nombres"]
        apellidos = request.form["apellidos"]
        cedula = request.form["cedula"]
        telefono_fijo = request.form["telefono_fijo"]
        telefono_celular = request.form["telefono_celular"]
        direccion = request.form["direccion"]
        correo = request.form["correo"]

        try:
            agregar_cliente(nombres, apellidos, cedula, telefono_fijo, telefono_celular, direccion, correo)
        except ValueError as e:
            return render_template("clientes.html", registros=obtener_clientes(), error=str(e))
        
        return redirect(url_for("clientes.listar_clientes"))
    
    registros = obtener_clientes()
    return render_template("clientes.html", registros=registros)


# 📌 Editar cliente
@clientes_bp.route("/clientes/editar/<int:id_cliente>", methods=["GET", "POST"])
def editar_cliente(id_cliente):
    cliente = obtener_cliente_por_id(id_cliente)

    if request.method == "POST":
        nombres = request.form["nombres"]
        apellidos = request.form["apellidos"]
        cedula = request.form["cedula"]
        telefono_fijo = request.form["telefono_fijo"]
        telefono_celular = request.form["telefono_celular"]
        direccion = request.form["direccion"]
        correo = request.form["correo"]

        actualizar_cliente(id_cliente, nombres, apellidos, cedula, telefono_fijo, telefono_celular, direccion, correo)
        return redirect(url_for("clientes.listar_clientes"))

    return render_template("editar_cliente.html", cliente=cliente)

# buscar cliente
@clientes_bp.route('/buscar', methods=['POST'])
def buscar_cliente():
    cedula = request.form.get('cedula')
    cliente = None

    db = get_db()
    with db.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT id_cliente, nombres, apellidos, cedula, telefono_fijo, telefono_celular, direccion, correo
            FROM clientes
            WHERE cedula = %s
        """, (cedula,))
        cliente = cursor.fetchone()
    # Mantiene la lista completa de clientes visible
    registros = obtener_clientes()
    
    return render_template("clientes.html", cliente=cliente, cedula=cedula, registros=obtener_clientes())


# 📌 Eliminar cliente
@clientes_bp.route("/clientes/eliminar/<int:id_cliente>", methods=["POST"])
def eliminar_cliente_route(id_cliente):
    eliminar_cliente(id_cliente)
    return redirect(url_for("clientes.listar_clientes"))
