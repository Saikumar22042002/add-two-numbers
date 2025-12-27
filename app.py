import logging
from flask import Flask, jsonify, request

# Configure structured logging for better parsing in production
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    """Provides a simple health check endpoint."""
    return jsonify({"status": "healthy"}), 200

@app.route('/add', methods=['GET'])
def add_numbers():
    """
    Adds two numbers provided as query parameters 'a' and 'b'.
    Returns a 400 error if parameters are missing or not numeric.
    Example: /add?a=10&b=20
    """
    a_val = request.args.get('a')
    b_val = request.args.get('b')

    if a_val is None or b_val is None:
        logger.warning("Add request failed: Missing 'a' or 'b' parameter.")
        return jsonify({"error": "Missing required query parameters: 'a' and 'b'"}), 400

    try:
        num_a = float(a_val)
        num_b = float(b_val)
    except (ValueError, TypeError):
        logger.error("Add request failed: Invalid number format for a='%s', b='%s'", a_val, b_val)
        return jsonify({"error": f"Invalid number format. 'a' and 'b' must be numbers."}), 400

    result = num_a + num_b
    logger.info("Successfully processed /add request: %s + %s = %s", num_a, num_b, result)
    
    response_data = {
        "inputs": {"a": num_a, "b": num_b},
        "result": {"sum": result}
    }
    return jsonify(response_data), 200

# This block is for local development and is not used by the Gunicorn server.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
