import os
import uuid
from flask import Flask, render_template, request, jsonify, session
from saudi_ecommerce_chatbot import SaudiEcommerceChatbot

app = Flask(__name__)
# Generate a random secret key for sessions
app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(24))

# Initialize the chatbot globally
try:
    chatbot = SaudiEcommerceChatbot()
except Exception as e:
    print(f"Warning: Failed to initialize chatbot: {e}")
    chatbot = None

@app.route('/')
def index():
    # Ensure each user has a unique session ID
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if chatbot is None:
         return jsonify({"error": "Chatbot not initialized. Check server logs."}), 500

    data = request.json
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    user_id = session.get('user_id', 'anonymous')

    try:
        response = chatbot.chat(user_id, user_message)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
