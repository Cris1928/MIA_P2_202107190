from flask import Flask, jsonify, request
import time
from flask_cors import CORS
#202107190ubuntu
app = Flask(__name__)
CORS(app)

respuesta ={
    'estado': 'OK',
    'mensaje': '[Success] => Disco creado correctamente',
    }

@app.route('/', methods=['GET'])
def obtener_productos():
    return jsonify(respuesta)

@app.route('/execute', methods=['POST'])
def get_first_word():
    data = request.get_json()
    message = data.get('command', '')

    # Dividir el mensaje en palabras
    words = message.split()

    if words:
        message = f'[Success] => comando {words[0]} ejecutado exitosamente'
    else:
        message = "No se encontraron palabras en el mensaje."

    respuesta = {
        'estado': 'OK',
        'mensaje': message,
    }

    # Esperamos 1 segundo, para simular proceso de ejecución
    time.sleep(1)

    return jsonify(respuesta)

if __name__ == '__main__':
    app.run(debug=True)