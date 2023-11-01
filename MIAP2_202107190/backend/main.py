from flask import Flask, jsonify, request
from mkdisk import mkdisk, fdisk
from FORMATEO.ext2.ext2 import Superblock, Inode,Journal
from mount import mount, unmount
from mkfs import mkfs,login,makegroup,makeuser,remgroup,remuser
from mkfile import mkfile, cat,remove, rename,copy, move, find
from journal import add_j
import time
from reporte import rep
from ress import publi
import math
from flask_cors import CORS
import struct
import os
#202107190ubuntu
app = Flask(__name__)
CORS(app)
usuarios_montados = [] 
cont=0
mbytes = []
contMb= 0
contador_r=0
usuarios = None
part_act=None
@staticmethod
def bitMaps(instruccion, mounted_partitions, id):
    publi.ress = ""
    partition = None
    for partition_dict in mounted_partitions:
        if id in partition_dict:
            partition = partition_dict[id]
            break
    if not partition:
        publi.ress = publi.ress +f"Error: la partiion con id {id} no existe."
       # print(f"Error: la partiion con id {id} no existe.")
        return
    # Retrieve partition details.
    path = partition['path']
    inicio = partition['inicio']
    size = partition['size']
    filename = path
    current_directory = os.getcwd()
    full_path= f'{filename}'
    if not os.path.exists(full_path):
    #    print(f"Error: el file {full_path} no existe.")
        publi.ress = publi.ress +f"Error: el file {full_path} no existe."
        return
    with open(full_path, "rb+") as file:
        file.seek(inicio)
        superblock = Superblock.unpack(file.read(Superblock.SIZE))
        
       # print("Bitmap de inodos")
        publi.ress = publi.ress +"Bitmap de inodos"
        bitmap_bloques_inicio = superblock.s_bm_block_start
        cantidad_bloques = superblock.s_blocks_count
        FORMAT = f'{cantidad_bloques}s'
        SIZE = struct.calcsize(FORMAT)
        file.seek(bitmap_bloques_inicio)
        bitmap_bloques = struct.unpack(FORMAT, file.read(SIZE))
        bitmap_bloques=bitmap_bloques[0].decode('utf-8')
        bitmap_inodos_inicio = superblock.s_bm_inode_start
        cantidad_inodos = superblock.s_inodes_count
        FORMAT = f'{cantidad_inodos}s'
        SIZE = struct.calcsize(FORMAT)
        file.seek(bitmap_inodos_inicio)
        bitmap_inodos = struct.unpack(FORMAT, file.read(SIZE))
        bitmap_inodos=bitmap_inodos[0].decode('utf-8')
        texto =f'\nInstruccion: {instruccion.upper()}'
        texto +="\n______ESTADO BITMAPS______"
        texto +="\nbloques"
        texto +="\n"+bitmap_bloques
        texto +="\ninodos"
        texto +="\n"+bitmap_inodos
        texto +="\n______FIN ESTADO BITMAPS______"
        global contMb
        inodo_dot = generate_dot(instruccion,bitmap_inodos, "inodo", contMb)
        bloque_dot = generate_dot(instruccion,bitmap_bloques, "bloque", contMb)
        global mbytes
        mbytes.append((inodo_dot, bloque_dot))
        contMb += 1
@staticmethod
def generate_dot(instruccion, bitmap, label, contador):
    publi.ress = ""
    length = len(bitmap)
    rows = math.ceil(math.sqrt(length))
    
    # Split the bitmap string into rows
    split_bitmap = [bitmap[i:i+rows] for i in range(0, length, rows)]
    
    # Join the split rows with <br> tags
    formatted_bitmap = '\\n'.join(split_bitmap)
    #dot_string += f'label="gg";\n'
    
    # Use the formatted bitmap in the label of the node
    dot_string = f'{label}_{contador} [shape=box,  label="{instruccion}\n{formatted_bitmap}"];\n'
    return dot_string
@staticmethod
def procesar_comando(comando):
    datos = {} 
    comand=0
    if comando.startswith("mkdisk")  :
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

       #  print("mostrando montados")

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
            
    elif comando.startswith("mkfile") or comando.startswith("mkdir"):
        comand=17
        partes = comando.split()
        parametro_actual = None
        for palabra in partes:
            if palabra.startswith("-r"):
                datos["-r"] = None
            elif palabra.startswith("-"):

                parametro_actual = palabra[1:]
                parametro, valor = parametro_actual.split("=")
                datos[parametro] = valor
        
            
        return datos,comand    

    elif comando.startswith("cat"):
        comand=18
        partes = comando.split()
        parametro_actual = None
        for palabra in partes:
            if palabra.startswith("-"):
                parametro_actual = palabra[1:]
                parametro, valor = parametro_actual.split("=")
                datos[parametro] = valor
        return datos,comand  
    
    elif comando.startswith("remove"):
        comand=19
        partes = comando.split()
        parametro_actual = None
        for palabra in partes:
            if palabra.startswith("-"):
                parametro_actual = palabra[1:]
                parametro, valor = parametro_actual.split("=")
                datos[parametro] = valor
        return datos,comand  
    
    elif comando.startswith("rename"):
        comand=20
        partes = comando.split()
        parametro_actual = None
        for palabra in partes:
            if palabra.startswith("-"):
                parametro_actual = palabra[1:]
                parametro, valor = parametro_actual.split("=")
                datos[parametro] = valor
        return datos,comand  

    elif comando.startswith("copy"):
        comand=21
        partes = comando.split()
        parametro_actual = None
        for palabra in partes:
            if palabra.startswith("-"):
                parametro_actual = palabra[1:]
                parametro, valor = parametro_actual.split("=")
                datos[parametro] = valor
        return datos,comand  
    elif comando.startswith("find"):
        comand=22
        partes = comando.split()
        parametro_actual = None
        for palabra in partes:
            if palabra.startswith("-"):
                parametro_actual = palabra[1:]
                parametro, valor = parametro_actual.split("=")
                datos[parametro] = valor
        return datos,comand  
    elif comando.startswith("move"):
        comand=23
        partes = comando.split()
        parametro_actual = None
        for palabra in partes:
            if palabra.startswith("-"):
                parametro_actual = palabra[1:]
                parametro, valor = parametro_actual.split("=")
                datos[parametro] = valor
        return datos,comand  
    elif comando.startswith("#"):
        comand=24
        
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
    global cont
    global part_act
    global usuarios
    data = request.get_json()
    message = data.get('command', '')

    # Dividir el mensaje en palabras
    words = message.split()
    coamando,opcion=procesar_comando(message)
    print("pal",coamando)
    print(opcion)
    if opcion==1:
        text = mkdisk(coamando)
    elif opcion ==3:
        global contador_r
        text=""
        rep(coamando,usuarios_montados, mbytes,contador_r)
        text = text + publi.ress 
        contador_r=contador_r+1

    elif opcion == 4:
        if "size" in coamando:
            coamando["size"]=int(coamando["size"])  
        text = fdisk(coamando)
    elif opcion == 5:
        text = mount(coamando,usuarios_montados,cont)
        cont=cont+1
        publi.ress = publi.ress + "\nmostrando montados"
        for i in usuarios_montados:
           #  print("id",i)
            publi.ress = publi.ress + "\n\nid"+str(i)
            for id in i:
               #  print("path",i[id]["path"])
                publi.ress = publi.ress + "\npath :"+str(i[id]["path"])
               #  print("name",i[id]["name"])
                publi.ress = publi.ress + "\nname :"+str(i[id]["name"])
               #  print("index",i[id]["index"])
                publi.ress = publi.ress + "\nindex :"+str(i[id]["index"])
                # print("inicio",i[id]["inicio"])
                publi.ress = publi.ress + "\ninicio :"+str(i[id]["inicio"])
               #  print("size",i[id]["size"])
                publi.ress = publi.ress + "\nsize"+str(i[id]["size"])
                # print("partition",i[id]["partition"])
                publi.ress = publi.ress + "\npartition"+str(i[id]["partition"])
               #  print("id",i[id]["id"])
                publi.ress = publi.ress + "\nid"+str(i[id]["id"])

        text= text + publi.ress

    elif opcion == 6:
        text=unmount(coamando,usuarios_montados)

    elif opcion ==8:
        text=mkfs(coamando, usuarios_montados)
        add_j(usuarios_montados,part_act,str(( "mkfs",coamando)))
        text = text + publi.ress
    elif opcion ==9:
        
        

        usuarios,part_act,text= login(coamando,usuarios_montados)
        
        bitMaps("login"+str(coamando), usuarios_montados, part_act)
        text=text + publi.ress
        add_j(usuarios_montados,part_act,str(("login",coamando)))
        text=text + publi.ress
    elif opcion==10:
        
        if usuarios is not None:
            ex = usuarios
            usuarios=None
            part_act=None
        else:
            
            print("no hay usuario logeado")
        add_j(usuarios_montados,part_act,str(( "logout",{})))
    elif opcion == 11:
        text=makegroup(coamando,usuarios_montados,part_act)
        bitMaps("mkgrp"+str(coamando), usuarios_montados, part_act)
        add_j(usuarios_montados,part_act,str(( "mkgrp",coamando)))
    elif opcion == 12:
        text=makeuser(coamando,usuarios_montados,part_act)
        bitMaps("mkusr"+str(coamando), usuarios_montados, part_act)
        add_j(usuarios_montados,part_act,str(( "mkuser",coamando)))
    elif opcion ==15:
        text=remuser(coamando,usuarios_montados,part_act)
        bitMaps("rmusr"+str(coamando), usuarios_montados, part_act)
        add_j(usuarios_montados, part_act,str(( "rmuser", coamando)))
    elif opcion ==16:
    
        text=remgroup(coamando,usuarios_montados,part_act)
        bitMaps("rmgrp"+str(coamando), usuarios_montados, part_act)
        add_j(usuarios_montados,part_act,str(( "rmgrp", coamando)))

    elif opcion == 17:
        if usuarios != None:
            text=""
            mkfile(coamando,usuarios_montados,part_act,usuarios)
            text=text + publi.ress
            bitMaps("mkfile"+str(coamando),usuarios_montados,part_act)
            text=text + publi.ress
            add_j(usuarios_montados, part_act,str(( "mkfile", coamando)))
            text=text + publi.ress
        else:
            text="\nError: no hay usuario logeado"
    
    elif opcion == 18:
        if usuarios != None:
            text=""
            cat(coamando,usuarios_montados,part_act,usuarios)
            text=text + publi.ress
 
        else:
            text="\nError: no hay usuario logeado"

    elif opcion == 19:
        if usuarios != None:
            text=""
            remove(coamando,usuarios_montados,part_act,usuarios)
            text=text + publi.ress
            bitMaps("remove"+str(coamando),usuarios_montados,part_act)
            text=text + publi.ress
            add_j(usuarios_montados, part_act,str(( "remove", coamando)))
            text=text + publi.ress
        else:
            text="\nError: no hay usuario logeado"
    elif opcion == 20:
        if usuarios != None:
            text=""
            rename(coamando,usuarios_montados,part_act,usuarios)
            text=text + publi.ress
            bitMaps("rename"+str(coamando),usuarios_montados,part_act)
            text=text + publi.ress
            add_j(usuarios_montados, part_act,str(( "rename", coamando)))
            text=text + publi.ress
        else:
            text="\nError: no hay usuario logeado"


    elif opcion == 21:
        if usuarios != None:
            text=""
            copy(coamando,usuarios_montados,part_act,usuarios)
            text=text + publi.ress
            bitMaps("copy"+str(coamando),usuarios_montados,part_act)
            text=text + publi.ress
            add_j(usuarios_montados, part_act,str(( "copy", coamando)))
            text=text + publi.ress
        else:
            text="\nError: no hay usuario logeado"

    elif opcion == 22:
        if usuarios != None:
            text=""
            find(coamando,usuarios_montados,part_act,usuarios)
            text=text + publi.ress
          
        else:
            text="\nError: no hay usuario logeado"
    elif opcion == 23:
        if usuarios != None:
            text=""
            move(coamando,usuarios_montados,part_act,usuarios)
            text=text + publi.ress
            bitMaps("move"+str(coamando),usuarios_montados,part_act)
            text=text + publi.ress
            add_j(usuarios_montados, part_act,str(( "move", coamando)))
            text=text + publi.ress
        else:
            text="\nError: no hay usuario logeado"
    elif opcion == 24:
        text="\ncomentario"


    else:
        text="\ncomando no valido"
   

#mkdisk -size=3000 -unit=K -path=/home/daniel/Escritorio/MIAP2_202107190/p.dk
#fdisk -type=P -unit=M -name=Part1 -size=15 -path=/home/daniel/Escritorio/MIAP2_202107190/p.dk
#mount -path=/home/daniel/Escritorio/MIAP2_202107190/p.dk -name=Part1
# print(words)
   #  if words:
    #     message = f'[Success] => comando {words[0]} ejecutado exitosamente'+f'[extra] => comando {words}'
   #  else:
     #    message = "No se encontraron palabras en el mensaje."
    if text == "":
        text = "\nerr"
    elif text == None:
        text = "\nerr"

    respuesta = {
        'estado': 'OK',
        'mensaje': text,
    }

    # Esperamos 1 segundo, para simular proceso de ejecución
    time.sleep(1)

    return jsonify(respuesta)

if __name__ == '__main__':
    app.run(debug=True)