from db import get_db

def obtener_clientes():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes")
    resultados = cursor.fetchall()
    cursor.close()
    db.close()
    return resultados

print(obtener_clientes())
