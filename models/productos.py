from db import get_db

def obtener_productos():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    resultados = cursor.fetchall()
    cursor.close()
    db.close()
    return resultados

# 📌 Obtener stock actual de un producto
def obtener_stock(id_producto):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT stock FROM productos WHERE id_producto = %s", (id_producto,))
    resultado = cursor.fetchone()
    cursor.close()
    db.close()
    return resultado[0] if resultado else 0

# 📌 Actualizar stock según tipo de movimiento
def actualizar_stock(id_producto, tipo, cantidad):
    db = get_db()
    cursor = db.cursor()

    if tipo == "entrada":
        cursor.execute("UPDATE productos SET stock = stock + %s WHERE id_producto = %s", (cantidad, id_producto))
    elif tipo == "salida":
        cursor.execute("UPDATE productos SET stock = stock - %s WHERE id_producto = %s", (cantidad, id_producto))

    db.commit()
    cursor.close()
    db.close()


def agregar_producto(nombre, descripcion, categoria, precio, stock):
    db = get_db()
    cursor = db.cursor()

    # Insertar producto
    cursor.execute("""
        INSERT INTO productos (nombre, descripcion, categoria, precio, stock)
        VALUES (%s, %s, %s, %s, %s)
    """, (nombre, descripcion, categoria, precio, stock))
    db.commit()

    # Obtener ID del producto recién insertado
    id_producto = cursor.lastrowid

    # Registrar movimiento automático de entrada
    cursor.execute("""
        INSERT INTO movimientos (id_producto, tipo, cantidad, fecha, observaciones)
        VALUES (%s, %s, %s, NOW(), %s)
    """, (id_producto, "entrada", stock, "Stock inicial"))
    db.commit()

    cursor.close()
    db.close()
    
    
def obtener_producto_por_id(id_producto):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
    resultado = cursor.fetchone()
    cursor.close()
    db.close()
    return resultado

def actualizar_producto(id_producto, nombre, descripcion, categoria, precio, stock):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE productos
        SET nombre=%s, descripcion=%s, categoria=%s, precio=%s, stock=%s
        WHERE id_producto=%s
    """, (nombre, descripcion, categoria, precio, stock, id_producto))
    db.commit()
    cursor.close()
    db.close()

def eliminar_producto(id_producto):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
    db.commit()
    cursor.close()
    db.close()


def actualizar_stock(id_producto, tipo, cantidad):
    db = get_db()
    cursor = db.cursor()
    if tipo == "entrada":
        cursor.execute("UPDATE productos SET stock = stock + %s WHERE id_producto = %s", (cantidad, id_producto))
    elif tipo == "salida":
        cursor.execute("UPDATE productos SET stock = stock - %s WHERE id_producto = %s", (cantidad, id_producto))
    db.commit()
    cursor.close()
    db.close()
