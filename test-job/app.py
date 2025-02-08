from flask import Flask, jsonify
import time
import random

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_job():
    # Simulate job execution with a random delay between 1-3 seconds
    time.sleep(random.uniform(1, 3))
    
    # Randomly return success (200) or error (500)
    if random.random() < 0.8:  # 80% success rate
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Random failure'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)
