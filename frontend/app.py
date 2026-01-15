from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from subhunterx.database.manager import SubHunterDB
import sqlite3
import pandas as pd

app = Flask(__name__)
CORS(app)
db = SubHunterDB()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/scans')
def get_scans():
    conn = sqlite3.connect('subhunterx.db')
    df = pd.read_sql_query("SELECT * FROM scans ORDER BY timestamp DESC LIMIT 10", conn)
    return jsonify(df.to_dict('records'))

@app.route('/api/subdomains/<scan_id>')
def get_subdomains(scan_id):
    conn = sqlite3.connect('subhunterx.db')
    query = """
    SELECT * FROM subdomains 
    WHERE scan_id = ? 
    ORDER BY risk_score DESC
    """
    df = pd.read_sql_query(query, conn, params=(scan_id,))
    return jsonify(df.to_dict('records'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)