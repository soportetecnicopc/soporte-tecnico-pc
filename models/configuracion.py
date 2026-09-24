from db import get_db


def obtener_configuracion():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM configuracion LIMIT 1")
    config = cursor.fetchone()
    cursor.close()
    db.close()
    return config

def actualizar_configuracion(iva, ganancia, stock):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE configuracion
        SET iva_porcentaje = %s,
            ganancia_porcentaje = %s,
            stock_minimo = %s
        WHERE id_config = 1
    """, (iva, ganancia, stock))
    db.commit()
    cursor.close()
    db.close()
