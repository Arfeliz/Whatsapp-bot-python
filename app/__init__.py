# app/__init__.py

from flask import Flask, request, jsonify
from app.controllers.chat_controller import process_whatsapp_message
import os

def create_app():
    app = Flask(__name__)

    @app.route('/webhook', methods=['GET'])
    def verify():
        token = os.getenv("TOKEN_VERIFICACION", "mi_secreto_123")
        if request.args.get('hub.verify_token') == token:
            return request.args.get('hub.challenge'), 200
        return "Error", 403

    @app.route('/webhook', methods=['POST'])
    def webhook():
        body = request.get_json()
        process_whatsapp_message(body)
        return jsonify({"status": "ok"}), 200

    return app