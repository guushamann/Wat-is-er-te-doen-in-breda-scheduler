from flask import Flask, jsonify
import subprocess
from start import start
app = Flask(__name__)

@app.route('/execute', methods=['POST'])
async def execute_job():
    try:
        print("start scrape")
        await start()
        print("stop scrape")
        return jsonify({'status': 'success'}), 200
        
            
    except Exception as e:
        print(e)
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
print('scrape server started')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8086)
