from db import get_db

def registrar_estado(id_ticket, estado):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO estados_ticket (id_ticket, estado)
        VALUES (%s, %s)
    """, (id_ticket, estado))
    db.commit()
    cursor.close()
    db.close()

def obtener_historial(id_ticket):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT estado, fecha
        FROM estados_ticket
        WHERE id_ticket = %s
        ORDER BY fecha DESC
    """, (id_ticket,))
    historial = cursor.fetchall()
    cursor.close()
    db.close()
    return historial
