import struct
from FORMATEO.ext2.ext2 import Superblock, Inode, FolderBlock, FileBlock, PointerBlock, block, Content, Journal
import os
from MBR import MBR
from EBR import EBR
from prettytable import PrettyTable
from ress import publi
import boto3
import subprocess
from dotenv import load_dotenv
global_id=0
cc_graph=""
load_dotenv('.env')
acces_id=os.getenv('aws_access_key_id')
secret_id=os.getenv('aws_secret_acces_key')
name_bucket=os.getenv('bucket_name')
def rep(parametros, particiones,Mbt,contador_r):
    name = parametros.get('name')
    path = parametros.get('path')
    id = parametros.get('id', None)
    if id == None: #si no se especifica id
        #print("Error: no se especifico un id.")
        publi.ress = publi.ress + "\nError: no se especifico un id."
        return
    partition=None
    for partition_dict in particiones: # recorrer las particiones montadas
        l=list(partition_dict.values())[0]["id"]
 
        if id == l: # si el id esta en el diccionario
            #obtenemos la particion
            partition = list(partition_dict.values())[0]
            
            break
    if partition == None: # si no se encontro la particion
        # print(f"Error: la particion {id} no existe.")
        publi.ress = publi.ress +f"\nError: la particion {id} no existe."
        return
    #obtenemos el nombre del disco
    path = partition['path']
    inicio = partition['inicio']
    size = partition['size']
    filename = path
    full_path= f'{filename}' # obtener el path completo
    if not os.path.exists(full_path): # si no existe el archivo
        #print(f"Error: el archivo {full_path} no existe.") # imprimir error
        publi.ress = publi.ress + f"\nError: el archivo {full_path} no existe."
        return
    with open(full_path, "rb+") as file: # abrir el archivo
        if name=="mbr":
            file.seek(0) # ir al inicio del archivo
            mbr = MBR.unpack(file.read(MBR.SIZE))
            tipo_objeto, pt, lista, index = empac(mbr, 0)
            #--
            global global_id
            global_id=global_id+1
            hnodo = f'subgraph cluster_{tipo_objeto}{index}{"{"} label = "{tipo_objeto}{index}"; color=blue; style=filled; fillcolor=lightblue; \n'
            ndoTabla = f'\n{global_id} [label='
            htmlstr = '''<<TABLE BORDER="0" CELLBORDER="2" CELLSPACING="0" CELLPADDING="5">\n'''
            htmlstr += '''<TR>\n'''
            for i in pt.field_names:
                htmlstr += f'''<TD><B>{i}</B></TD>\n'''
            htmlstr += '''</TR>\n'''
            for i in pt._rows:
                htmlstr += '''<TR>\n'''
                for j in i:
                    htmlstr += f'''<TD>{j}</TD>\n'''
                htmlstr += '''</TR>\n'''

         #   htmlstr += '''</TABLE>>shape=box];\n'''
            #sep

        
            bloques = f''
           # bloques += '''<<TABLE BORDER="0" CELLBORDER="2" CELLSPACING="0" CELLPADDING="5">\n'''
            
            ii=4
            particiones= mbr.particiones
            for i in range(0,4):
                if particiones[i].type == 'E':
                    bloques += '''<TR>\n'''
                    bloques += f'''<TD><B>particion</B></TD>\n'''
                    bloques += f'''<TD><B>Extendida</B></TD>\n'''
                    bloques+= '''</TR>\n'''
                    bloques += '''<TR>\n'''
                    bloques += f'''<TD><B>Nombre</B></TD>\n'''
                    bloques += f'''<TD><B>{particiones[i].name} </B></TD>\n'''
                    bloques += '''</TR>\n'''
                    bloques += '''<TR>\n'''
                    bloques += f'''<TD><B>Inicio</B></TD>\n'''
                    bloques += f'''<TD><B>{particiones[i].byte_inicio} </B></TD>\n'''
                    bloques += '''</TR>\n'''
                    bloques += '''<TR>\n'''
                    bloques += f'''<TD><B>Size</B></TD>\n'''
                    bloques += f'''<TD><B>{particiones[i].actual_size} </B></TD>\n'''
                    bloques += '''</TR>\n'''
                    bloques += '''<TR>\n'''
                    bloques += f'''<TD><B>Fit</B></TD>\n'''
                    bloques += f'''<TD><B>{particiones[i].fit} </B></TD>\n'''
                    bloques += '''</TR>\n'''
                    bloques += '''<TR>\n'''
                    bloques += f'''<TD><B>Status</B></TD>\n'''
                    bloques += f'''<TD><B>{particiones[i].status} </B></TD>\n'''
                    bloques += '''</TR>\n'''
                elif particiones[i].type == 'P':
                    bloques += '''<TR>\n'''
                    bloques += f'''<TD><B>particion</B></TD>\n'''
                    bloques += f'''<TD><B>Primaria</B></TD>\n'''
                    bloques += '''</TR>\n'''
                    bloques += '''<TR>\n'''
                    bloques += f'''<TD><B>Nombre</B></TD>\n'''
                    bloques += f'''<TD><B>{particiones[i].name} </B></TD>\n'''
                    bloques += '''</TR>\n'''
                    bloques += '''<TR>\n'''
                    bloques += f'''<TD><B>Inicio</B></TD>\n'''
                    bloques += f'''<TD><B>{particiones[i].byte_inicio} </B></TD>\n'''
                    bloques += '''</TR>\n'''
                    bloques += '''<TR>\n'''
                    bloques += f'''<TD><B>Size</B></TD>\n'''
                    bloques += f'''<TD><B>{particiones[i].actual_size} </B></TD>\n'''
                    bloques += '''</TR>\n'''
                    bloques += '''<TR>\n'''
                    bloques += f'''<TD><B>Fit</B></TD>\n'''
                    bloques += f'''<TD><B>{particiones[i].fit} </B></TD>\n'''
                    bloques += '''</TR>\n'''
                    bloques += '''<TR>\n'''
                    bloques += f'''<TD><B>Status</B></TD>\n'''
                    bloques += f'''<TD><B>{particiones[i].status} </B></TD>\n'''
                    bloques += '''</TR>\n'''
                elif particiones[i].type == 'L':
                    bloques += '''<TR>\n'''
                    bloques += f'''<TD><B>particion</B></TD>\n'''
                    bloques += f'''<TD><B>Logica</B></TD>\n'''
                    bloques += '''</TR>\n'''
                    bloques += '''<TR>\n'''
                    bloques += f'''<TD><B>Nombre</B></TD>\n'''
                    bloques += f'''<TD><B>{particiones[i].name} </B></TD>\n'''
                    bloques += '''</TR>\n'''
                    bloques += '''<TR>\n'''
                    bloques += f'''<TD><B>Inicio</B></TD>\n'''
                    bloques += f'''<TD><B>{particiones[i].byte_inicio} </B></TD>\n'''
                    bloques += '''</TR>\n'''
                    bloques += '''<TR>\n'''
                    bloques += f'''<TD><B>Size</B></TD>\n'''
                    bloques += f'''<TD><B>{particiones[i].actual_size} </B></TD>\n'''
                    bloques += '''</TR>\n'''
                    bloques += '''<TR>\n'''
                    bloques += f'''<TD><B>Fit</B></TD>\n'''
                    bloques += f'''<TD><B>{particiones[i].fit} </B></TD>\n'''
                    bloques += '''</TR>\n'''
                    bloques += '''<TR>\n'''
                    bloques += f'''<TD><B>Status</B></TD>\n'''
                    bloques += f'''<TD><B>{particiones[i].status} </B></TD>\n'''
                    bloques += '''</TR>\n'''
            bloques += '''</TABLE>>shape=box];\n'''
            if lista is None:
                total = hnodo + ndoTabla + htmlstr +  '\n}'
            else:
                total = hnodo + ndoTabla + htmlstr + bloques + '\n}'


            if tipo_objeto == "FolderBlock":
                total = hnodo + bloques + '\n}'
            #creamos el .dot contador_r
            with open(f"/home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/mbr.dot", "w") as file:
                file.write(f'digraph G {{\n{total}\n}}')
            os.system(f"dot -Tpng /home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/mbr.dot -o /home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/mbr.png")
            os.system(f"/home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/mbr.png")
            
            
            
           # s3=boto3.client('s3',acces_id=acces_id,secret_id=secret_id)
           # s3.upload_file("mbr.png",name_bucket,"/reportes/mbr.png",)
            publi.ress = publi.ress + "\nreporte mbr creado con exito"

        elif name=="disk":
            ll = []
            file.seek(0)
            mbr = MBR.unpack(file.read(MBR.SIZE))
            ll.append('\n<TD>MBR</TD>')
            partitions = mbr.particiones
            for partition in partitions:
                print(str(partition))
                if partition.type == 'P' and partition.status == 1:
                    porcentaje = partition.actual_size/mbr.mbr_tamano
                    ll.append(f'\n<TD>primaria: {porcentaje}%</TD>')
                elif partition.type == 'E' and partition.status == 1:
                    porcentaje = partition.actual_size/mbr.mbr_tamano
                    e_ll = []
                    next = partition.byte_inicio
                    while next != -1:
                        file.seek(next)
                        ebr = EBR.unpack(file.read(EBR.SIZE))
                        e_ll.append(f'\n   <TD>EBR: {porcentaje}%</TD>')
                        if ebr.next != -1:
                            
                            e_ll.append(f'\n   <TD>logica: {porcentaje}%</TD>')
                        if ebr.next != -1 and ebr.next < (next + EBR.SIZE+ebr.actual_size):
                            e_ll.append(f'\n   <TD>LIBRE</TD>')
                        next = ebr.next
                    extended_content = "".join(e_ll)
                    ll.append(f'\n<TD><TABLE BORDER="2"><TR><TD colspan="10">extendida</TD></TR><TR>{extended_content}</TR></TABLE></TD>')
                elif partition.status == 0:
                    ll.append(f'\n<TD>LIBRE</TD>')
            graphviz_code = f'''digraph G {{
            node [shape=none];
            disk [label=<
            <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">

            <TR>{"".join(ll)}</TR>
            </TABLE>
            >];
            }}
                            '''
            
            with open(f'/home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/disk.dot', 'w') as f:
                    f.write(f'{graphviz_code}')
            os.system(f"dot -Tpng /home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/disk.dot -o /home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/disk.png")
            os.system(f"/home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/disk.png")
            publi.ress = publi.ress +  "\nreporte disk creado exitosamente"

        elif name == 'inode':
            graphviz_cod=""
            superblock = Superblock.unpack(file.read(Superblock.SIZE))
            cuid = 0
            cantidad_inodos = superblock.s_inodes_count
            FORMAT = f'{cantidad_inodos}s'
            SIZE = struct.calcsize(FORMAT)
            file.seek(superblock.s_bm_inode_start)
            bitmap_inodos = struct.unpack(FORMAT, file.read(SIZE))[0].decode('utf-8')
            for i,n in enumerate(bitmap_inodos):
                if n == '1':
                    inicio = superblock.s_inode_start + i*Inode.SIZE
                    file.seek(inicio)
                    #---
                    object = Inode.unpack(file.read(Inode.SIZE))
                  # object_type, pt, lista,index = imprimir_como_antes(object,inicio)
                    object_type=type(object).__name__
                    if object_type == "FileBlock":
                        object.b_content = object.b_content.replace("\x00", "")
                    if object_type == "FolderBlock":
                        for i in object.b_content:
                            i.b_name =i.b_name.replace("\x00", "")
                    tabla=PrettyTable(["Reporte_inodo"," "])
                    atributos=vars(object)
                    lista= None
                    for at, val in atributos.items():
                        tabla.add_row([at,val])
                            
                        
                            
                        
                    #---
                    #global global_id
                    global_id=global_id+1
                    hnodo = f'subgraph cluster_{object_type}{i}{"{"} label = "{object_type}{i}"; color=blue; style=filled; fillcolor=lightblue; \n'
                    ndoTabla = f'\n{global_id} [label=' 
                    htmlstr = '''<<TABLE BORDER="0" CELLBORDER="2" CELLSPACING="0" CELLPADDING="5">\n'''
                    htmlstr += "<TR>\n"
                    for i in tabla.field_names:
                        htmlstr += f"   <TD>{i}</TD>\n"
                    htmlstr += "</TR>\n"
                    for i in tabla._rows:
                        htmlstr += "<TR>\n"
                        for j in i:
                            j = str(j).replace("\n", "<BR/>")
                            htmlstr += f"<TD>{j}</TD>\n"
                        htmlstr += "</TR>\n"
                    htmlstr += "</TABLE>>shape=box];\n"

                    bloques = f'\n node [shape=record];\n bloques{global_id} [label = '
                    if lista is not None:
                        bloques += '"{'
                        for i,n in enumerate(lista):
                            bloques += f'<content{i}> {n.__str__()}|'
                        bloques += '\n}"];'
                    if lista is None:
                        total = hnodo + ndoTabla + htmlstr +  '\n}'
                    else:
                        total = hnodo + ndoTabla + htmlstr + bloques + '\n}'


                    if tipo_objeto == "FolderBlock":
                        total = hnodo + bloques + '\n}'

                    graphviz_cod += "\n"+total
            for i in range(cuid):
                graphviz_cod += f'\n{i} -> {i+1}'
            with open(f'/home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/reporte_inodos.dot', 'w') as f:
                    f.write(f'digraph G {{\n{graphviz_cod}\n}}')
            os.system(f"dot -Tpng /home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/reporte_inodos.dot -o /home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/reporte_inodos.png")
            os.system(f"reporte_inodos{contador_r}.png")
            publi.ress = publi.ress +  "\nreporte inode creado exitosamente"
        elif name == 'bm_inode':
            file.seek(inicio)
            superblock = Superblock.unpack(file.read(Superblock.SIZE))
            c_graph=""
            for i in Mbt:
                c_graph += f'\n{i[0]}'
            for i in range(len(Mbt)):
                c_graph += f'\ninodo_{i}  -> inodo_{i+1}'
            with open(f'/home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/bm_inode.dot', 'w') as f:
                    f.write(f'digraph G {{\n{c_graph}\n}}')
            os.system(f"dot -Tpng /home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/bm_inode.dot -o /home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/bm_inode.png")
            os.system(f"/home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/bm_inode.png")
            publi.ress = publi.ress +  "\nreporte bm_inode creado con exito"
        elif name=="bm_block":
            file.seek(inicio)
            superblock = Superblock.unpack(file.read(Superblock.SIZE))
            c_graph=""
            for i in Mbt:
                c_graph += f'\n{i[1]}'
            for i in range(len(Mbt)):
                c_graph += f'\nbloque_{i}  -> bloque_{i+1}'
            with open(f'/home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/bm_block.dot', 'w') as f:
                    f.write(f'digraph G {{\n{c_graph}\n}}')
            os.system(f"dot -Tpng /home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/bm_block.dot -o /home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/bm_block.png")
            os.system(f"/home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/bm_block.png")
            publi.ress = publi.ress +  "\nreporte bm_block creado con exito"
        elif name=="block":
            
            cgraph=""
            cid= 0
            lgraph=[]
            superblock = Superblock.unpack(file.read(Superblock.SIZE))
            c_bloques=superblock.s_blocks_count
            FORMAT = f'{c_bloques}s'
            SIZE = struct.calcsize(FORMAT)
            file.seek(superblock.s_bm_block_start)
            bitmapBloques= struct.unpack(FORMAT, file.read(SIZE))[0].decode('utf-8')
            for i,n in enumerate(bitmapBloques):
                if n=="1":
                    inicio=superblock.s_block_start + i*64 #64 es el tamaño de un bloque
                    file.seek(inicio)
                    try:
                        object=FolderBlock.unpack(file.read(FolderBlock.SIZE))
                    except:
                        object=FileBlock.unpack(file.read(FileBlock.SIZE))
                    try:
                        object=FileBlock.unpack(file.read(FileBlock.SIZE))
                    except:
                        pass
                    t_objeto=type(object).__name__
                    if t_objeto == "FileBlock":
                        object.b_content = object.b_content.replace("\x00", "")
                    if t_objeto == "FolderBlock":
                        for i in object.b_content:
                            i.b_name =i.b_name.replace("\x00", "")
                    tabla=PrettyTable(["Reporte_bloque"," "])
                    atributos=vars(object)
                    lista= None
                    for at, val in atributos.items():
                        if not isinstance(val, list):
                            tabla.add_row([at,val])
                        else:
                            lista=val
                    
                    global_id=global_id+1
                    hnodo = f'subgraph cluster_{t_objeto}{i}{"{"} label = "{t_objeto}{i}"; color=blue; style=filled; fillcolor=lightblue; \n'
                    ndoTabla = f'\n{global_id} [label='
                    htmlstr = '''<<TABLE BORDER="0" CELLBORDER="2" CELLSPACING="0" CELLPADDING="5">\n'''
                    htmlstr += "<TR>\n"
                    for i in tabla.field_names:
                        htmlstr += f"   <TD>{i}</TD>\n"
                    htmlstr += "</TR>\n"
                    for i in tabla._rows:
                        htmlstr += "<TR>\n"
                        for j in i:
                            j = str(j).replace("\n", "<BR/>")
                            htmlstr += f"<TD>{j}</TD>\n"
                        htmlstr += "</TR>\n"
                    htmlstr += "</TABLE>>shape=box];\n"

                    bloques = f'\n node [shape=record];\n bloques{global_id} [label = '
                    if lista is not None:
                        bloques += '"{'
                        for i,n in enumerate(lista):
                            bloques += f'<content{i}> {n.__str__()}|'
                        bloques += '\n}"];'
                    if lista is None:
                        total = hnodo + ndoTabla + htmlstr +  '\n}'
                    else:
                        total = hnodo + ndoTabla + htmlstr + bloques + '\n}'
                    if t_objeto == "FolderBlock":
                        total = hnodo + bloques + '\n}'

                    cgraph += "\n"+total
            for i in range(cid):
                cgraph += f'\n{i} -> {i+1}'
            with open(f'/home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/reporte_bloques.dot', 'w') as f:
                    f.write(f'digraph G {{\n{cgraph}\n}}')
            os.system(f"dot -Tpng /home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/reporte_bloques.dot -o /home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/reporte_bloques.png")
            publi.ress = publi.ress +  "\nreporte block creado con exito"
        elif name=="sb":
            file.seek(inicio)
            superblock = Superblock.unpack(file.read(Superblock.SIZE))
            tabla =  PrettyTable(["Reporte_superbloque"," "])
            atributos=vars(superblock)
            l = None
            for at, val in atributos.items():
                tabla.add_row([at,val])
            global_id=global_id+1
            hnodo = f'subgraph cluster_sb{inicio}{"{"} label = "sb{inicio}"; color=blue; style=filled; fillcolor=lightblue; \n'
            ndoTabla = f'\n{global_id} [label='
            htmlstr = '''<<TABLE BORDER="0" CELLBORDER="2" CELLSPACING="0" CELLPADDING="5">\n'''
            htmlstr += "<TR>\n"
            for i in tabla.field_names:
                htmlstr += f"   <TD>{i}</TD>\n"
            htmlstr += "</TR>\n"
            for i in tabla._rows:
                htmlstr += "<TR>\n"
                for j in i:
                    j = str(j).replace("\n", "<BR/>")
                    htmlstr += f"<TD>{j}</TD>\n"
                htmlstr += "</TR>\n"
            htmlstr += "</TABLE>>shape=box];\n"
            bloques = f'\n node [shape=record];\n bloques{global_id} [label = '
            if l is not None:
                bloques += '"{'
                for i,n in enumerate(l):
                    bloques += f'<content{i}> {n.__str__()}|'
                bloques += '\n}"];'
            if l is None:
                total = hnodo + ndoTabla + htmlstr +  '\n}'
            else:
                total = hnodo + ndoTabla + htmlstr + bloques + '\n}'

            with open('/home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/reporte_superbloque.dot', 'w') as f:
    
                f.write(f'digraph G {{\n{total}\n}}')
            os.system(f"dot -Tpng /home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/reporte_superbloque.dot -o /home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/reporte_superbloque.png")
            publi.ress = publi.ress +  "\nreporte sb creado exitosamente"
        elif name=="tree":
            global cc_graph
            

            file.seek(inicio)
            superblock = Superblock.unpack(file.read(Superblock.SIZE))
            cid=0
            cc_graph=""
            try:
                p=rama_g(file,superblock.s_inode_start,0)
              
                cc_graph += f"\nhome -> {p}"
                
                with open(f'/home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/reporte_tree.dot', 'w') as f:
                    f.write(f'digraph G {{\n{cc_graph}\n}}')
                os.system(f"dot -Tpng /home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/reporte_tree.dot -o /home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/reporte_tree.png")
                publi.ress = publi.ress + "\ngrafica tree generada con exito"
            except:
                publi.ress = publi.ress + "\nerror"
            
        
        elif name=="journaling":
            file.seek(inicio)
            superblock = Superblock.unpack(file.read(Superblock.SIZE))
            file.seek(inicio+superblock.SIZE)
            try:
                journal= Journal.unpack(file.read(Journal.SIZE))
            except:
                print("Error: la particion no es ext2")
                return
            cgraph=""
            cgraph += f'digraph G {{\n{journal.journal_data}\n}}'
            #print(f"journaling: {journal.journal_data}")
            formatt=journal.journal_data.replace("\n","\\n")
            cgraph = f'digraph G {{\n  uniconodo [shape=box, label=" { formatt } "];\n}}'
            with open(f'/home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/reporte_journaling.dot', 'w') as f:
                    f.write(f'{cgraph}')
            os.system(f"dot -Tpng /home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/reporte_journaling.dot -o /home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes/reporte_journaling.png")
            publi.ress = publi.ress + "\nreporte journaling creado exitosamente"
def empac(emp, index):
    tipo_objeto = type(emp).__name__ #obtenemos el tipo de objeto
    if tipo_objeto == "FileBlock": #si es un FileBlock
        emp.b_content = emp.b_content.replace("\x00", "") #remplazamos el   \x00 por un espacio
    if tipo_objeto == "FolderBlock":
        for i in emp.b_content:
            i.b_name =i.b_name.replace("\x00", "")
    tabla=PrettyTable(["Reporte_mbr"," "]) #creamos la tabla
    atributos=vars(emp) #obtenemos los atributos del objeto
    lista= None
    for at, val in atributos.items():
        if not isinstance(val, list): #si no es una lista
            tabla.add_row([at,val]) #agregamos a la tabla
        else:
            lista=val
    return tipo_objeto, tabla, lista,index
    
def rama_g(file,id_init, index):
    global cc_graph
    
    if id_init == -1:
        return None
    file.seek(id_init)
    if index == 0:
        object = Inode.unpack(file.read(Inode.SIZE))
    elif index == 1:
        object = FolderBlock.unpack(file.read(FolderBlock.SIZE))
    elif index == 2:
        object = FileBlock.unpack(file.read(FileBlock.SIZE))
    elif index == 3:
        object = PointerBlock.unpack(file.read(PointerBlock.SIZE))
    object_type, pt, lista,index = empac(object,id_init)
    total, id = ff(object_type, pt, lista,id_init)
#--
    cc_graph += "\n"+total
    if object_type== 'Inode':
        for i,n in enumerate(lista):
            if object.i_type == '0':
                apuntado = rama_g(file,n,1)
                if apuntado is not None:
                   
                    cc_graph += f"\nbloques{id}:<content{i}> -> bloques{apuntado}"
                
            else:
                apuntado =rama_g(file,n,2)
                if apuntado is not None:
                   
                    cc_graph += f"\nbloques{id}:<content{i}> -> {apuntado}"
    elif object_type== 'FolderBlock':
        for i,n in enumerate(lista):
            if n.b_inodo != -1:
                apuntado =rama_g(file,n.b_inodo,0)
                if apuntado is not None:
                    cc_graph += f"\nbloques{id}:<content{i}> -> {apuntado}"
            
    #print(cc_graph)
    #print(id)
    return id


        
def ff(object_type, pt, lista,id_init):
    global global_id
    global_id+=1
    hnodo = f'subgraph cluster_{object_type}{id_init}{"{"} label = "{object_type}{id_init}"; color=blue; style=filled; fillcolor=lightblue; \n'
    ndoTabla = f'\n{global_id} [label='
    htmlstr = '''<<TABLE BORDER="0" CELLBORDER="2" CELLSPACING="0" CELLPADDING="5">\n'''
    htmlstr += "<TR>\n"
    for i in pt.field_names:
        htmlstr += f"   <TD>{i}</TD>\n"
    htmlstr += "</TR>\n"
    for i in pt._rows:
        htmlstr += "<TR>\n"
        for j in i:
            j = str(j).replace("\n", "<BR/>")
            htmlstr += f"<TD>{j}</TD>\n"
        htmlstr += "</TR>\n"


    htmlstr += "</TABLE>>shape=box];\n"
    bloques = f'\n node [shape=record];\n bloques{global_id} [label = '
    if lista is not None:
        bloques += '"{'
        for i,n in enumerate(lista):
            bloques += f'<content{i}> {n.__str__()}|'
        bloques += '\n}"];'
    if lista is None:
        total = hnodo + ndoTabla + htmlstr +  '\n}'
    else:
        total = hnodo + ndoTabla + htmlstr + bloques + '\n}'    
    if object_type == "FolderBlock":
        total = hnodo + bloques + '\n}'
    #print(total)  /home/daniel/Escritorio/MIAP2_202107190/fronted/mia-react/src/reportes
    return total, global_id
  
