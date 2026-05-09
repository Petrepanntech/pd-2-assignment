from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        'message': 'Welcome to Pandas Assignment API',
        'status': 'running',
        'version': '1.0'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'pandas-assignment'}), 200

@app.route('/api/status')
def status():
    return jsonify({
        'app': 'Pandas Assignment',
        'environment': 'production',
        'deployed': True
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found', 'code': 404}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error', 'code': 500}), 500

if __name__ == '__main__':
    app.run(debug=False)
