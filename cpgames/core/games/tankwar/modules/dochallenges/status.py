from flask import Flask, render_template, jsonify
from pymongo import MongoClient


import config

app = Flask(__name__)

client = MongoClient(config.database["host"])
db = client[config.database['db_name']]
players_collection = db[config.database['level_collection']]

if players_collection.count_documents({}) == 0:
    players_collection.insert_one({"player1_level": False, "player2_level": False})

# Route to fetch player data from MongoDB
@app.route('/status', methods=['GET'])
def get_status():
    player_data = players_collection.find_one()
    return jsonify(player_data)

# Route to handle player 1 button click
@app.route('/player_1', methods=['POST'])
def player_1_click():
    players_collection.update_one({}, {'$set': {'player1_level': True}})
    return jsonify({'message': 'Player 1 clicked!'}), 200

# Route to handle player 2 button click
@app.route('/player_2', methods=['POST'])
def player_2_click():
    players_collection.update_one({}, {'$set': {'player2_level': True}})
    return jsonify({'message': 'Player 2 clicked!'}), 200

# Main route to display the interface
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
