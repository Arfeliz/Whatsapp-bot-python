import os
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import json

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# --- CONFIGURACIÓN ---
# El TOKEN_VERIFICACION es el que tú inventas y pones en el Dashboard de Meta
TOKEN_VERIFICACION = "mi_secreto_123" 
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = "v18.0"

@app.route('/webhook', methods=['GET'])
def verificar_webhook():
    """
    Paso obligatorio para que Meta valide tu servidor.
    """
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode == 'subscribe' and token == TOKEN_VERIFICACION:
        print("WEBHOOK_VERIFICADO CON ÉXITO")
        return challenge, 200
    
    print("ERROR DE VERIFICACIÓN: TOKEN INCORRECTO")
    return 'Error de verificación', 403

@app.route('/webhook', methods=['POST'])
def recibir_mensajes():
    """
    Recibe las notificaciones de mensajes nuevos desde WhatsApp.
    """
    try:
        body = request.get_json()
        
        # Verificamos que sea un mensaje de WhatsApp
        entry = body.get('entry', [{}])[0]
        changes = entry.get('changes', [{}])[0]
        value = changes.get('value', {})
        
        if 'messages' in value:
            # Datos del mensaje
            mensaje_obj = value['messages'][0]
            numero_remitente = mensaje_obj['from']
            texto_usuario = mensaje_obj.get('text', {}).get('body', "").lower()
            
            # Datos del perfil del usuario
            contacto = value.get('contacts', [{}])[0]
            nombre_perfil = contacto.get('profile', {}).get('name', 'amigo/a')

            print(f"Mensaje recibido de {nombre_perfil} ({numero_remitente}): {texto_usuario}")

            # LÓGICA DE RESPUESTA
            if "hola" in texto_usuario:
                respuesta = f"¡Hola, {nombre_perfil}! 👋 Qué gusto saludarte. Soy tu asistente virtual inteligente. ¿En qué puedo ayudarte hoy?"
                enviar_whatsapp(respuesta, numero_remitente)
            elif "cuero" in texto_usuario:
                respuesta = f"¡El cuero es un material fascinante, {nombre_perfil}! ¿Te gustaría saber más sobre sus tipos y cuidados? 🐄✨"
                enviar_whatsapp(respuesta, numero_remitente)
            elif "gracias" in texto_usuario:
                enviar_whatsapp(f"¡De nada, {nombre_perfil}! Estoy para servirte. 😊", numero_remitente)
                
            else:
                respuesta_default = "Recibí tu mensaje. Por ahora solo entiendo saludos, pero pronto tendré más funciones. 🚀"
                enviar_whatsapp(respuesta_default, numero_remitente)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(f"Error procesando el mensaje: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

def enviar_whatsapp(texto, numero):
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    
    # Estructura exacta requerida por Meta
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": numero,
        "type": "text",
        "text": {"body": texto}
    }
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        # Usamos json=payload (Requests lo convierte automáticamente)
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"Enviando a Meta... Status: {response.status_code}")
        print(f"Respuesta de Meta: {response.text}") # Esto nos dirá si funcionó
        
        return response.json()
    except Exception as e:
        print(f"Error de red: {e}")
        return None

if __name__ == '__main__':
    # Ejecuta el servidor en el puerto 5000
    app.run(host='0.0.0.0', port=5000, debug=True)