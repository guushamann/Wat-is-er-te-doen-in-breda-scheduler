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
        # # Using subprocess.run instead of call to capture output
        # process = await subprocess.create_subprocess_shell(
        #     './deploy.sh',
        #     stdout=subprocess.PIPE,
        #     stderr=subprocess.PIPE
        # )
        # stdout, stderr = await process.communicate()
        
        # if process.returncode == 0:
        #     return jsonify({'status': 'success'}), 200
        # else:
        #     error_message = stderr.decode('utf-8') if stderr else stdout.decode('utf-8') if stdout else 'Unknown error occurred'
        #     print(error_message)
        #     return jsonify({
        #         'status': 'error',
        #         'message': error_message
        #     }), 500
            
    except Exception as e:
        print(e)
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8086)
