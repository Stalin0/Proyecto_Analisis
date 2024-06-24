from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import psycopg2
import requests

# Configuración de la conexión a la base de datos
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="proyecto",
    user="postgres",
    password="1234"
)

# Configuración de la API de ChatGPT
chatgpt_api_key = "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"  # Reemplaza con tu clave de API de OpenAI
chatgpt_url = "https://api.openai.com/v1/chat/completions"
chatgpt_model = "gpt-3.5-turbo"  # Reemplaza con el modelo de ChatGPT que deseas utilizar

app = Flask(__name__)
CORS(app)

def obtener_respuesta_chatgpt(mensaje):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {chatgpt_api_key}"
    }

    data = {
        "model": chatgpt_model,
        "messages": [
            {"role": "system", "content": "I am a nutrition chatbot. Ask me about food, exercises or diseases related to nutrition, I SHOULD NOT ANSWER TO OTHER SUBJECTS THAT DO NOT DEAL WITH NUTRITION AND ITS DERIVATIVES"},
            {"role": "user", "content": mensaje}
        ]
    }

    response = requests.post(chatgpt_url, json=data, headers=headers)
    response_data = response.json()

    if "choices" in response_data:
        choices = response_data["choices"]
        if len(choices) > 0:
            return choices[0]["message"]["content"]

    return None

@app.route('/mensajes', methods=['POST'])
def crear_mensaje():
    data = request.get_json()
    mensaje = data.get('mensaje')
    if mensaje:
        # Guardar el mensaje en la base de datos
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chatbot (mensaje) VALUES (%s)", (mensaje,))
        conn.commit()
        cursor.close()

        # Obtener la respuesta de ChatGPT
        respuesta_chatgpt = obtener_respuesta_chatgpt(mensaje)

        return jsonify({'mensaje': mensaje, 'respuesta': respuesta_chatgpt})
    else:
        return jsonify({'error': 'Error: El mensaje no puede estar vacío'})

def verify_user(email, contrasenia):
    cursor = conn.cursor()
    query = "SELECT * FROM usuario WHERE email = %s AND contrasenia = %s;"
    cursor.execute(query, (email, contrasenia))
    user_exists = cursor.fetchone() is not None
    cursor.close()
    return user_exists

@app.route('/verificar_usuario', methods=['POST'])
def verificar_usuario():
    data = request.get_json()
    email = data.get('email')
    contrasenia = data.get('contrasenia')
    if email and contrasenia:
        if verify_user(email, contrasenia):
            return jsonify({'mensaje': 'Usuario existente'})
        else:
            return jsonify({'mensaje': 'Usuario no existente'})
    else:
        return jsonify({'error': 'Error: Debes proporcionar el email y la contrasenia'})

    
    
if __name__ == '__main__':
    app.run()
