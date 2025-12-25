# app/controllers/chat_controller.py

from app.services.whatsapp_service import WhatsAppService

ws = WhatsAppService()

def process_whatsapp_message(body):
    value = body['entry'][0]['changes'][0]['value']
    
    if 'messages' in value:
        message = value['messages'][0]
        number = message['from']
        
        # Lógica para texto
        if 'text' in message:
            text = message['text']['body'].lower()
            if "hola" in text:
                return ws.send_buttons(number, "¿Cómo puedo ayudarte?", [("id_ventas", "Ventas"), ("id_soporte", "Soporte")])
        
        # Lógica para botones
        elif 'interactive' in message:
            id_button = message['interactive']['button_reply']['id']
            if id_button == "id_ventas":
                return ws.send_text_message(number, "Has elegido Ventas.")
            elif id_button == "id_soporte":
                return ws.send_text_message(number, "Has elegido Soporte.")
                
    return None