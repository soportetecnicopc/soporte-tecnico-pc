from flask import Blueprint, render_template
from db import get_db

reportes_bp = Blueprint("reportes", __name__)

@reportes_bp.route("/reportes")
def reporte_movimientos():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Consulta agrupada por tipo y motivo
    cursor.execute("""
        SELECT tipo, motivo, COUNT(*) AS total_movimientos, SUM(cantidad) AS total_cantidad
        FROM movimientos
        GROUP BY tipo, motivo
        ORDER BY tipo, motivo
    """)
    datos = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("reportes.html", datos=datos)
