import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("../database/floodsense.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return "FloodSense AI API is running"

@app.route("/predictions", methods=["GET"])
def get_predictions():
    conn = get_db_connection()
    rows = conn.execute("""
        SELECT l.place, l.severity, l.type, p.risk_score, p.risk_level, p.reason, p.timestamp
        FROM predictions p
        JOIN locations l ON p.location_id = l.id
        ORDER BY p.risk_score DESC
    """).fetchall()
    conn.close()

    results = []
    for row in rows:
        results.append({
            "place": row["place"],
            "severity": row["severity"],
            "type": row["type"],
            "risk_score": row["risk_score"],
            "risk_level": row["risk_level"],
            "reason": row["reason"],
            "timestamp": row["timestamp"]
        })

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)