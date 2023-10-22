from flask import Flask, jsonify, request
from mkdisk import mkdisk, fdisk
import time
from flask_cors import CORS
#202107190ubuntu
app = Flask(__name__)
CORS(app)
@staticmethod
def procesar_comando(comando):
    datos = {} 
    comand=0
    if comando.startswith("mkdisk"):
        comand=1
        partes = comando.split()  # Dividir la cadena en palabras
    # print("abajo")
        #print(partes)
        #print("arriba")
            # Diccionario para almacenar los valores
        parametro_actual = None  # Para mantener el parámetro actual
        for palabra in partes:
            if palabra.startswith("-"):
                parametro_actual = palabra[1:]  # Eliminar el guion (-) del parámetro
            #   print(parametro_actual)
                parametro, valor = parametro_actual.split("=")
                datos[parametro] = valor
        return datos,comand
    elif comando.startswith("rmdisk"):
        comand=2
        partes = comando.split()  # Dividir la cadena en palabras
        parametro_actual = None  # Para mantener el parámetro actual
        for palabra in partes:
            if palabra.startswith("-"):
                parametro_actual = palabra[1:]  # Eliminar el guion (-) del parámetro
                parametro, valor = parametro_actual.split("=")
                datos[parametro] = valor
        return datos,comand
    elif comando.startswith("rep"):
        comand=3
        partes = comando.split()
        parametro_actual = None
        for palabra in partes:
            if palabra.startswith("-"):
                parametro_actual = palabra[1:]
                parametro, valor = parametro_actual.split("=")
                datos[parametro] = valor
        return datos,comand
                
    elif comando.startswith("fdisk"):
        comand=4
        partes = comando.split()
        parametro_actual = None
        for palabra in partes:
            if palabra.startswith("-"):
                parametro_actual = palabra[1:]
                parametro, valor = parametro_actual.split("=")
                datos[parametro] = valor
        #   print(datos)        
        return datos,comand
    #      elif parametro_actual is not None:
    #         datos[parametro_actual] = palabra
        #        print(parametro_actual)
        #       print("arriba")
        #      parametro_actual = None
    
    elif comando.startswith("mount"):
        comand=5
        partes = comando.split()
        parametro_actual = None
        for palabra in partes:
            if palabra.startswith("-"):
                parametro_actual = palabra[1:]
                parametro, valor = parametro_actual.split("=")
                datos[parametro] = valor
        #   print(datos)        
        return datos,comand
    
    elif comando.startswith("unmount"):
        comand=6
        partes = comando.split()
        parametro_actual = None
        for palabra in partes:
            if palabra.startswith("-"):
                parametro_actual = palabra[1:]
                parametro, valor = parametro_actual.split("=")
                datos[parametro] = valor
        #   print(datos)    
        return datos,comand
    
    elif comando.startswith("mosumon"):
        comand=7
        partes = comando.split()
        parametro_actual = None
        for palabra in partes:
            if palabra.startswith("-"):
                parametro_actual = palabra[1:]
                parametro, valor = parametro_actual.split("=")
                datos[parametro] = valor
        #   print(datos)    
        return datos,comand
    elif comando.startswith("mkfs"):
        comand=8
        partes = comando.split()
        parametro_actual = None
        for palabra in partes:
            if palabra.startswith("-"):
                parametro_actual = palabra[1:]
                parametro, valor = parametro_actual.split("=")
                datos[parametro] = valor
        #   print(datos)    
        return datos,comand

    elif comando.startswith("login"):
        comand=9
        partes = comando.split()
        parametro_actual = None
        for palabra in partes:
            if palabra.startswith("-"):
                parametro_actual = palabra[1:]
                parametro, valor = parametro_actual.split("=")
                datos[parametro] = valor
        return datos,comand
    
    elif comando.startswith("logout"):
        comand=10
        partes = comando.split()
        parametro_actual = None
        for palabra in partes:
            if palabra.startswith("-"):
                parametro_actual = palabra[1:]
                parametro, valor = parametro_actual.split("=")
                datos[parametro] = valor
        return datos,comand  
    
    elif comando.startswith("mkgrp"):

        comand=11
        partes = comando.split()
        parametro_actual = None
        for palabra in partes:
            if palabra.startswith("-"):
                parametro_actual = palabra[1:]
                parametro, valor = parametro_actual.split("=")
                datos[parametro] = valor
        return datos,comand  

    elif comando.startswith("mkusr"):
        comand=12
        partes = comando.split()
        parametro_actual = None
        for palabra in partes:
            if palabra.startswith("-"):
                parametro_actual = palabra[1:]
                parametro, valor = parametro_actual.split("=")
                datos[parametro] = valor
        return datos,comand  
    
    elif comando.startswith("rmusr"):
        comand=13
        partes = comando.split()
        parametro_actual = None
        for palabra in partes:
            if palabra.startswith("-"):
                parametro_actual = palabra[1:]
                parametro, valor = parametro_actual.split("=")
                datos[parametro] = valor
        return datos,comand  
    elif comando.startswith("execute"):
        comand=14
        partes = comando.split()
        parametro_actual = None
        for palabra in partes:
            if palabra.startswith("-"):
                parametro_actual = palabra[1:]
                parametro, valor = parametro_actual.split("=")
                datos[parametro] = valor
        return datos,comand 
    elif comando.startswith("remuser"):
        comand=15
        partes = comando.split()
        parametro_actual = None
        for palabra in partes:
            if palabra.startswith("-"):
                parametro_actual = palabra[1:]
                parametro, valor = parametro_actual.split("=")
                datos[parametro] = valor
        return datos,comand 
    elif comando.startswith("remgrp"):
        comand=16
        partes = comando.split()
        parametro_actual = None
        for palabra in partes:
            if palabra.startswith("-"):
                parametro_actual = palabra[1:]
                parametro, valor = parametro_actual.split("=")
                datos[parametro] = valor
        return datos,comand    
            

    return None,None
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
    coamando,opcion=procesar_comando(message)
    print("pal",coamando)
    print(opcion)
    if opcion==1:
        text = mkdisk(coamando)
    elif opcion == 4:
        if "size" in coamando:
            coamando["size"]=int(coamando["size"])  
        text = fdisk(coamando)
        
# mkdisk -size=3000 -unit=K -path=/home/daniel/Escritorio/MIAP2_202107190/p.dk
# fdisk -type=P -unit=M -name=Part1 -size=15 -path=/home/daniel/Escritorio/MIAP2_202107190/p.dk
   # print(words)
   #  if words:
    #     message = f'[Success] => comando {words[0]} ejecutado exitosamente'+f'[extra] => comando {words}'
   #  else:
     #    message = "No se encontraron palabras en el mensaje."

    respuesta = {
        'estado': 'OK',
        'mensaje': text,
    }

    # Esperamos 1 segundo, para simular proceso de ejecución
    time.sleep(1)

    return jsonify(respuesta)

if __name__ == '__main__':
    app.run(debug=True)