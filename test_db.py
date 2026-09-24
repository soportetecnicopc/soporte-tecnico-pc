import mysql.connector

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Admin",
    database="soporte_tecnico",
    port=3306
)

print("Conexión exitosa:", db.is_connected())
