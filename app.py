from flask import Flask, jsonify, request
from flask_cors import CORS
from database_wrapper import DatabaseWrapper
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

db = DatabaseWrapper(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME'),
    port=os.getenv('DB_PORT')
)

@app.route("/tasks", methods=["GET"])
def get_tasks():
    lista = db.get_tasks()
    return jsonify(lista)

@app.route("/tasks", methods=["POST"])
def add_task():
    dati = request.json
    
    # CONTROLLO VALIDITÀ (Server Side)
    if not dati or 'title' not in dati:
        return jsonify({'error': 'Manca il titolo'}), 400
    
    titolo = dati["title"].strip() # Rimuove spazi vuoti inizio/fine
    
    if not titolo: # Se dopo aver tolto gli spazi è vuoto
        return jsonify({'error': 'Il titolo non può essere vuoto'}), 400

    # Ora add_task ritorna l'ID
    new_id = db.add_task(titolo)
    
    # Restituisco l'oggetto completo così Angular non deve ricaricare tutto
    return jsonify({"id": new_id, "title": titolo, "completed": False}), 201

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    db.delete_task(task_id)
    return jsonify({"msg": "Task eliminato"}), 200

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    dati = request.json
    # Prendo il valore booleano (True/False)
    completed = dati.get("completed") 
    
    db.toggle_task(task_id, completed)
    return jsonify({"msg": "Stato aggiornato"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)