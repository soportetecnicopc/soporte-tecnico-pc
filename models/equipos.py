from db import get_db
from flask import flash

def obtener_equipos():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    # JOIN para traer también datos del cliente
    cursor.execute("""
        SELECT e.id_equipo, e.marca, e.modelo, e.serie, e.observaciones, e.accesorios,
           c.nombres, c.apellidos
        FROM equipos e
        JOIN clientes c ON e.id_cliente = c.id_cliente
        ORDER BY e.id_equipo DESC
    """)
    resultados = cursor.fetchall()
    cursor.close()
    db.close()
    return resultados

def agregar_equipo(id_cliente, marca, modelo, serie, observaciones, accesorios):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO equipos (id_cliente, marca, modelo, serie, observaciones, accesorios)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (id_cliente, marca, modelo, serie, observaciones, accesorios))
    db.commit()
    cursor.close()
    db.close()

def obtener_equipo_por_id(id_equipo):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM equipos WHERE id_equipo = %s", (id_equipo,))
    resultado = cursor.fetchone()
    cursor.close()
    db.close()
    return resultado

def actualizar_equipo(id_equipo, id_cliente, marca, modelo, serie, observaciones, accesorios):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE equipos
        SET id_cliente=%s, marca=%s, modelo=%s, serie=%s, observaciones=%s, accesorios=%s
        WHERE id_equipo=%s
    """, (id_cliente, marca, modelo, serie, observaciones, accesorios, id_equipo))
    db.commit()
    cursor.close()
    db.close()

def eliminar_equipo(id_equipo):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM tickets WHERE id_equipo = %s", (id_equipo,))
    count = cursor.fetchone()[0]
    if count > 0:
        print("⚠️ No se puede eliminar: el equipo tiene tickets asociados.")
        return
    cursor.execute("DELETE FROM equipos WHERE id_equipo = %s", (id_equipo,))
    db.commit()
    cursor.close()
    db.close()

