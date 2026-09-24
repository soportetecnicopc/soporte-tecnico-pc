from db import get_db


def insertar_factura(id_cliente, total):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO facturas (id_cliente, total) VALUES (%s, %s)", (id_cliente, total))
    id_factura = cursor.lastrowid
    db.commit()
    cursor.close()
    db.close()
    return id_factura

def obtener_factura(id_factura):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM facturas WHERE id_factura = %s", (id_factura,))
    factura = cursor.fetchone()
    cursor.close()
    db.close()
    return factura

def obtener_cliente(id_cliente):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id_cliente,))
    cliente = cursor.fetchone()
    cursor.close()
    db.close()
    return cliente

def obtener_detalle_factura(id_factura):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT d.id_detalle, d.cantidad, d.precio_unitario, d.precio_con_ganancia,
               d.subtotal, d.iva, d.total, p.nombre
        FROM detalle_factura d
        JOIN productos p ON d.id_producto = p.id_producto
        WHERE d.id_factura = %s
    """, (id_factura,))
    detalle = cursor.fetchall()
    cursor.close()
    db.close()
    return detalle