import os
from FORMATEO.ext2.ext2 import Superblock, Inode,Journal
from ress import publi
def add_j(montadas, id , text):
    publi.ress = ""
    #print(text)
    if id == None:
        #p print("Error: id no especificado")
        publi.ress = publi.ress +"\nError: id no especificado"
        return
    particion= None
    for particion_montada in montadas:
        if id in particion_montada:
            particion = particion_montada[id]
            break
    if not particion:
        #pprint("Error: particion no montada")
        publi.ress = publi.ress +"\nError: particion no montada"
        return
    path= particion['path']
    inicio= particion['inicio']
    filename = path
    full_path= f'{filename}' #aqui se obtiene la ruta completa del archivo
    #verificar que el archivo exista
    if not os.path.exists(full_path):
      #  print(f"Error: {full_path} no existe.")
        publi.ress = publi.ress +f"\nError: {full_path} no existe."
        return
    
    with open(full_path, "rb+") as file:
        file.seek(inicio)
        superblock= Superblock.unpack(file.read(Superblock.SIZE))
        try:
            file.seek(inicio+superblock.SIZE)
            journal= Journal.unpack(file.read(Journal.SIZE))
            cc= journal.journal_data + ""
            cc+= text+"\n"
    
            if len(cc) > Journal.SIZE:
               # print("El journel estaba llen")
                publi.ress = publi.ress +"\nEl journel estaba lleno"
                return
  
            journal.journal_data= cc
            file.seek(inicio+superblock.SIZE)
            file.write(journal.pack())
        except:
          #  print("Error: la particion no es ext2")
            publi.ress = publi.ress +"\nError: la particion no es ext2"
            return
def journalActual(particiones,id):
    if id==None:
      #  print("Error: id no especificado")
        publi.ress = publi.ress +"\nError: id no especificado"
        return
    particion= None
    for particion_montada in particiones:
        if id in particion_montada:
            particion = particion_montada[id]
            break
    if particion == None:
     #   print("Error: particion no montada")
        publi.ress = publi.ress +"\nError: particion no montada"
        return
    path= particion['path']
    inicio= particion['inicio']
    filename = path
    full_path= f'{filename}' #aqui se obtiene la ruta completa del archivo
    #verificar que el archivo exista
    if not os.path.exists(full_path):
       # print(f"Error: {full_path} no existe.")
        publi.ress = publi.ress +f"\nError: {full_path} no existe."
        return
    with open(full_path, "rb+") as file:
        file.seek(inicio)
        superblock= Superblock.unpack(file.read(Superblock.SIZE))
        try:
            file.seek(inicio+superblock.SIZE)
            journal= Journal.unpack(file.read(Journal.SIZE))

       
           # print("journal en "+journal.journal_data)
            publi.ress = publi.ress +"\njournal en "+journal.journal_data
        except:
          #  print("Error: la particion no es ext2")
            publi.ress = publi.ress +"\nError: la particion no es ext2"
            return
def recovery(montadas,id):
    if id==None:
       # print("Error: id no especificado")
        publi.ress = publi.ress +"\nError: id no especificado"
        return
    particion= None
    for particion_montada in montadas:
        if id in particion_montada:
            particion = particion_montada[id]
            break
    if particion == None:
      #  print("Error: particion no montada")
        publi.ress = publi.ress +"\nError: particion no montada"
        return
    path= particion['path']
    inicio= particion['inicio']
    filename = path
    full_path= f'{filename}' #aqui se obtiene la ruta completa del archivo
    #verificar que el archivo exista
    if not os.path.exists(full_path):
       # print(f"Error: {full_path} no existe.")
        publi.ress = publi.ress +f"\nError: {full_path} no existe."
        return
    with open(full_path, "rb+") as file:
        file.seek(inicio)
        superblock= Superblock.unpack(file.read(Superblock.SIZE))
        try:
            file.seek(inicio+superblock.SIZE)
            journal= Journal.unpack(file.read(Journal.SIZE))
            cc= journal.journal_data
            cc= cc.split("\n")
            for i in range(len(cc)-1):
                print(cc[i])
            journal.journal_data= ""
            file.seek(inicio+superblock.SIZE)
            file.write(journal.pack())
        except:
            publi.ress = publi.ress +"\nError: la particion no es ext2"
           # print("Error: la particion no es ext2")
            return
        
def printJournal(montadas,id):
    if id==None:
       # print("Error: id no especificado")
        publi.ress = publi.ress +"\nError: id no especificado"
        return
    particion= None
    for particion_montada in montadas:
        if id in particion_montada:
            particion = particion_montada[id]
            break
    if particion == None:
        #print("Error: particion no montada")
        publi.ress = publi.ress +"\nError: particion no montada"
        return
    path= particion['path']
    inicio= particion['inicio']
    filename = path
    full_path= f'{filename}' #aqui se obtiene la ruta completa del archivo
    #verificar que el archivo exista
    if not os.path.exists(full_path):
        #print(f"Error: {full_path} no existe.")
        publi.ress = publi.ress + f"\nError: {full_path} no existe."
        return
    with open(full_path, "rb+") as file:
        file.seek(inicio)
        superblock= Superblock.unpack(file.read(Superblock.SIZE))
        try:
            file.seek(inicio+superblock.SIZE)
            journal= Journal.unpack(file.read(Journal.SIZE))
            cc= journal.journal_data
            cc= cc.split("\n")
            for i in range(len(cc)-1):
                print(cc[i])
        except:
            #print("Error: la particion no es ext2")
            publi.ress = publi.ress + "\nError: la particion no es ext2"
            return

def loss(parametros, particiones):
    id = parametros.get('id', None)#obtiene el id
    particion= None
    for particion_montada in particiones:
        if id in particion_montada:
            particion = particion_montada[id]
            break
    if particion == None:
        #print("Error: particion no montada")
        publi.ress = publi.ress +"\nError: particion no montada"
        return
    path= particion['path']
    inicio= particion['inicio']
    filename = path
    full_path= f'{filename}' #aqui se obtiene la ruta completa del archivo
    #verificar que el archivo exista
    if not os.path.exists(full_path):
        #print(f"Error: {full_path} no existe.")
        publi.ress = publi.ress +f"\nError: {full_path} no existe."
        return
    with open(full_path, "rb+") as file:
      #   file.seek(inicio)
      #   superblock= Superblock.unpack(file.read(Superblock.SIZE))
        try:
            file.seek(inicio+superblock.SIZE)
          #  journal= Journal.unpack(file.read(Journal.SIZE))
           # journal.journal_data= ""
          #  file.seek(inicio+superblock.SIZE)
          #  file.write(journal.pack())
        except:
            #print("Error: la particion no es ext2")
            publi.ress = publi.ress +"\nError: la particion no es ext2"
            return
        file.seek(inicio)
        superblock= Superblock.unpack(file.read(Superblock.SIZE))
        file.seek(superblock.s_bm_inode_start)
        file.write(b'\x00' * superblock.s_inodes_count)
        file.seek(superblock.s_bm_block_start)
        file.write(b'\x00' * superblock.s_blocks_count)
        file.seek(superblock.s_inode_start)
        file.write(b'\x00' * (superblock.s_inodes_count * Inode.SIZE))
        file.seek(superblock.s_block_start)
        file.write(b'\x00' * (superblock.s_blocks_count * 64))
        file.seek(inicio+superblock.SIZE)
        journal= Journal.unpack(file.read(Journal.SIZE))
       #print("journal en "+journal.journal_data)
        publi.ress = publi.ress +"\nError: la particion no es ext2"