from db import get_db

def obtener_tickets():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tickets ORDER BY fecha_creacion DESC")
    tickets = cursor.fetchall()
    cursor.close()
    db.close()
    return tickets

def crear_ticket(db, id_equipo, numero_ticket):
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO tickets (id_equipo, numero_ticket, estado)
        VALUES (%s, %s, %s)
    """, (id_equipo, numero_ticket, "Recibido"))
    db.commit()
    cursor.close()



#actualizar estado de tickets

def actualizar_estado(id_ticket, nuevo_estado):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE tickets
        SET estado = %s
        WHERE id_ticket = %s
    """, (nuevo_estado, id_ticket))
    db.commit()
    cursor.close()
    db.close()
