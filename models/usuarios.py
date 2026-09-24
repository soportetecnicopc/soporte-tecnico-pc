from db import get_db

def obtener_usuarios():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    resultados = cursor.fetchall()
    cursor.close()
    db.close()
    return resultados

def agregar_usuario(nombre_usuario, password, rol):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO usuarios (nombre_usuario, password, rol)
        VALUES (%s, %s, %s)
    """, (nombre_usuario, password, rol))
    db.commit()
    cursor.close()
    db.close()

def obtener_usuario_por_id(id_usuario):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    resultado = cursor.fetchone()
    cursor.close()
    db.close()
    return resultado

def actualizar_usuario(id_usuario, nombre_usuario, rol, password=None):
    db = get_db()
    cursor = db.cursor()
    if password:  # si se envía nueva clave
        cursor.execute("""
            UPDATE usuarios
            SET nombre_usuario=%s, rol=%s, password=%s
            WHERE id_usuario=%s
        """, (nombre_usuario, rol, password, id_usuario))
    else:
        cursor.execute("""
            UPDATE usuarios
            SET nombre_usuario=%s, rol=%s
            WHERE id_usuario=%s
        """, (nombre_usuario, rol, id_usuario))
    db.commit()
    cursor.close()
    db.close()

def eliminar_usuario(id_usuario):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    db.commit()
    cursor.close()
    db.close()
