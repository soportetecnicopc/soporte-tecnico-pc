from db import get_db

def obtener_clientes():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes")
    resultados = cursor.fetchall()
    cursor.close()
    db.close()
    return resultados

def agregar_cliente(nombres, apellidos, cedula, telefono_fijo, telefono_celular, direccion, correo):
    db = get_db()
    cursor = db.cursor()

    # Verificar si la cédula ya existe
    cursor.execute("SELECT COUNT(*) FROM clientes WHERE cedula = %s", (cedula,))
    existe = cursor.fetchone()[0]

    if existe > 0:
        cursor.close()
        db.close()
        raise ValueError("La cédula ya está registrada")

    cursor.execute("""
        INSERT INTO clientes (nombres, apellidos, cedula, telefono_fijo, telefono_celular, direccion, correo)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (nombres, apellidos, cedula, telefono_fijo, telefono_celular, direccion, correo))
    db.commit()
    cursor.close()
    db.close()
    

def obtener_cliente_por_id(id_cliente):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id_cliente,))
    resultado = cursor.fetchone()
    cursor.close()
    db.close()
    return resultado

def actualizar_cliente(id_cliente, nombres, apellidos, cedula, telefono_fijo, telefono_celular, direccion, correo):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE clientes
        SET nombres=%s, apellidos=%s, cedula=%s, telefono_fijo=%s, telefono_celular=%s, direccion=%s, correo=%s
        WHERE id_cliente=%s
    """, (nombres, apellidos, cedula, telefono_fijo, telefono_celular, direccion, correo, id_cliente))
    db.commit()
    cursor.close()
    db.close()

def eliminar_cliente(id_cliente):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))
    db.commit()
    cursor.close()
    db.close()
