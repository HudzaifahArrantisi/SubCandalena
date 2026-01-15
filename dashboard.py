from flask import Flask, render_template, jsonify
from subhunterx.database.manager import DBManager

app = Flask(__name__)
db = DBManager()

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/api/data')
def api_data():
    return jsonify(db.get_results())

if __name__ == '__main__':
    app.run(debug=True, port=5000)