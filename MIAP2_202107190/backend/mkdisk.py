import os
import struct
import time
import random
import struct
from MBR import MBR
from EBR import EBR
from part import Partition
from colorama import Fore, Back, Style
from ress import publi
def mkdisk(params):
    publi.ress=f""
   # print(params)
    publi.ress = publi.ress +"\ncreando disk..."
    #print(Fore.BLUE+"\n\t\t\t creando disk...")
    #print(Style.RESET_ALL)
   #aqui se obtienen los parametros
    size = params.get('size') 
    filename = params.get('path')
    unit = params.get('unit', 'M')
    fit = params.get('fit', 'FF')

    if type(size) is str: #si el tamaño es string
        size = int(size) #se convierte a entero

    # aqui se verifica que los parametros obligatorios esten
    if not size or not filename: #si no estan
        publi.ress = publi.ress + "\n no se encuentra el parametro size!"
        #print(Fore.RED+"no se encuentra el parametro size!") #se imprime el error
        #print(Style.RESET_ALL)
        return publi.ress

    # aqui se calcula el tamaño total en bytes
    if unit == 'K':
        total_size_bytes = size * 1024
    elif unit == 'M':
        total_size_bytes = size * 1024 * 1024
    else:
        publi.ress = publi.ress + f"\nUnit invalido: {unit}"
        #print(Fore.RED+f"Unit invalido: {unit}")
        #print(Style.RESET_ALL)
        return publi.ress

    # aqui se verifica que el fit sea valido
    if fit not in ['BF', 'FF', 'WF']:
        publi.ress = publi.ress + f"\nno valido el: {fit}"
        #print(Fore.RED+f"no valido el: {fit}")
        #print(Style.RESET_ALL)
        return publi.ress

   #current_directory = os.getcwd() #aqui se obtiene el directorio actual
   
    full_path= f'{filename}' #aqui se obtiene la ruta completa del archivo
  
    path = full_path #aqui se obtiene la ruta completa del archivo

    directory = os.path.dirname(path) #aqui se obtiene el directorio del archivo
    if not os.path.exists(directory): #aqui se verifica si existe el directorio
        os.makedirs(directory) #aqui se crea el directorio

   
    with open(path, "wb") as file: #aqui se abre el archivo
        file.write(b'\0' * total_size_bytes) #aqui se escribe el archivo con el tamaño total en bytes

    publi.ress = publi.ress + f"\n**Disk creado en {path} con tamano {size}{unit}."
    #print(Fore.YELLOW+f"**Disk creado en {path} con tamano {size}{unit}.") #aqui se imprime el mensaje de exito
    #print(Style.RESET_ALL)
    example = MBR(params) #aqui se crea el MBR
    with open(path, "rb+") as file: #aqui se abre el archivo
        file.seek(0) #nos posicionamos en el inicio del archivo
        file.write(example.pack())  #aqui se escribe el MBR en el archivo
 

    return publi.ress



def fdisk(params): #aqui se crea la particion
    publi.ress=f""
    #print("\n creando particion...")
    publi.ress = publi.ress + "\n creando particion..."
    filename = params.get('path') #aqui se obtiene el nombre del disco
    current_directory = os.getcwd() #aqui se obtiene el directorio actual
    full_path= f'{filename}' #aqui se obtiene la ruta completa del archivo
    #verificar que el archivo exista
    if not os.path.exists(full_path):
        #print(f"Error: {full_path} no existe.")
        publi.ress = publi.ress +f"\nError: {full_path} no existe."
        return publi.ress
    
    ex = {'size': 10, 'path': 'path', 'name': 'name_t'}
    
    nueva_particion = None
    
    if 'delete' in params or 'add' in params: #si se desea eliminar o agregar espacio a una particion
        nueva_particion = Partition(ex) #se crea una particion vacia
    else:
        nueva_particion = Partition(params) #se crea una particion con los parametros dados
    nueva_particion.status = 1 #se le asigna el estado de ocupado
    particion_temporal = nueva_particion #se guarda la particion temporalmente
    
    
    #leer el archivo
    partitions = []
    with open(full_path, "rb+") as file: #aqui se abre el archivo
        file.seek(0) #nos posicionamos en el inicio del archivo
        data = file.read(MBR.SIZE) #leemos el MBR
        x = MBR.unpack(data[:MBR.SIZE]) #desempaquetamos el MBR
        disk_size = x.mbr_tamano #obtenemos el tamaño del disco
        disk_fit = x.fit #obtenemos el fit del disco
        #print("disk size ",disk_size) #imprimimos el tamaño del disco
        publi.ress = publi.ress +"\ndisk size "+ str(disk_size)
        space = disk_size - MBR.SIZE #calculamos el espacio disponible
        
        
        
        for i in range(4): #recorremos las 4 particiones
            file.seek(struct.calcsize(MBR.FORMAT)+(i*Partition.SIZE)) #nos posicionamos en el inicio de la particion
            #desempaquetamos la particion
            data = file.read(Partition.SIZE) #leemos la particion
            particion_temporal = Partition.unpack(data)# desempaquetamos la particion
            partitions.append(particion_temporal) #agregamos la particion a la lista de particiones
        realizar = True 
        if 'delete' in params or 'add' in params: #si se desea eliminar o agregar espacio a una particion
            realizar = False #no se realiza la creacion de la particion
        elif all(item.status == 1 for item in partitions) and 'type' in params and nueva_particion.type != 'L': #si todas las particiones estan ocupadas y la particion a crear no es logica
            realizar = False #no se realiza la creacion de la particion
            publi.ress = publi.ress + "\nNo se puede crear la particion, ya que todas las particiones estan ocupadas"
           # print(Fore.RED+"No se puede crear la particion, ya que todas las particiones estan ocupadas") #se imprime el error
            #print(Style.RESET_ALL)
            return publi.ress
        count_E = sum(1 for item in partitions if item.type == 'E') #se cuenta el numero de particiones extendidas
        if count_E == 1 and nueva_particion.type == 'E': #si hay una particion extendida y se desea crear otra
            realizar = False #no se realiza la creacion de la particion
            publi.ress = publi.ress + "\nNo se puede crear la particion, ya que ya existe una particion extendida"
            #print(Fore.RED+"No se puede crear la particion, ya que ya existe una particion extendida") #se imprime el error
            #print(Style.RESET_ALL)
            return publi.ress
        
        partitions2 = partitions #se guarda la lista de particiones en otra variable
        nueva_particion.fit = disk_fit #se le asigna el fit del disco a la particion
        byteinicio = MBR.SIZE #se le asigna el byte de inicio del MBR a la particion
        if nueva_particion.type == 'L' and realizar: #si la particion a crear es logica y se desea crear
            #se busca la particion extendida
            for i, item in enumerate(partitions): #se recorren las particiones
                if item.type == 'E': #si la particion es extendida
                    tamano_de_e = item.actual_size #se obtiene el tamaño de la particion extendida
                    inicio_de_e = item.byte_inicio #se obtiene el byte de inicio de la particion extendida
                    byteinicio = item.byte_inicio #se le asigna el byte de inicio de la particion extendida a la particion a crear
                    limite_final_de_e = item.byte_inicio+item.actual_size #se obtiene el limite final de la particion extendida
                    file.seek(byteinicio) #nos posicionamos en el byte de inicio de la particion extendida
                    ebr = EBR.unpack(file.read(EBR.SIZE)) #desempaquetamos el EBR
                    if ebr.next == -1: #si no hay particiones logicas
                        #creamos el ebr
                        ebr = EBR(params, byteinicio) #creamos el ebr 
                        ebr.next= byteinicio+EBR.SIZE+ebr.actual_size #calculamos el byte de inicio de la siguiente particion
                        #verificamos que haya espacio para crear la particion
                        if ebr.next > limite_final_de_e: #si no hay espacio
                          # print("\nNo hay espacio para crear la particion")
                            publi.ress = publi.ress + "\nNo hay espacio para crear la particion"
                            return publi.ress
                        file.seek(byteinicio) #nos posicionamos en el byte de inicio de la particion extendida
                        file.write(ebr.pack()) #escribimos el ebr en el archivo
                        nuevo_ebr = EBR(ex, ebr.next) #creamos el nuevo ebr
                        file.seek(ebr.next) #nos posicionamos en el byte de inicio de la siguiente particion
                        file.write(nuevo_ebr.pack()) #escribimos el nuevo ebr en el archivo
                        return publi.ress
                    else :
                        while ebr.next != -1: #mientras haya particiones logicas
                            file.seek(ebr.next) #nos posicionamos en el byte de inicio de la siguiente particion    
                            ebr = EBR.unpack(file.read(EBR.SIZE)) #desempaquetamos el ebr
                        #creamos el ebr
                        nuevo_ebr = EBR(params, ebr.start) #creamos el nuevo ebr
                        nuevo_ebr.next = nuevo_ebr.start+EBR.SIZE+nuevo_ebr.actual_size #calculamos el byte de inicio de la siguiente particion
                        if nuevo_ebr.next > limite_final_de_e: #si no hay espacio
                            publi.ress = publi.ress + "\nNo hay espacio para crear la particion"
                            #print("No hay espacio para crear la particion") #se imprime el error
                            return publi.ress
                        file.seek(ebr.start) #nos posicionamos en el byte de inicio de la particion extendida
                        file.write(nuevo_ebr.pack())    #escribimos el nuevo ebr en el archivo
                        nuevo_nuevo_ebr = EBR(ex, nuevo_ebr.next) #creamos el nuevo ebr
                        file.seek(nuevo_ebr.next) #nos posicionamos en el byte de inicio de la siguiente particion
                        file.write(nuevo_nuevo_ebr.pack()) #escribimos el nuevo ebr en el archivo
                        return  publi.ress
            publi.ress = publi.ress +f'\nno existe una particion extendida, por lo que no se pudo agregar la particion logica{params.get("name") }'
            #print(Fore.RED+f'no existe una particion extendida, por lo que no se pudo agregar la particion logica{params.get("name") }')   #se imprime el error          
           # print(Style.RESET_ALL)
            return publi.ress
                
            
            
            
            
        
        
        
        if nueva_particion.fit == 'FF' and realizar: #si el fit es first fit y se desea crear la particion
            nueva_particion.fit = params.get('fit', 'FF').upper() #se le asigna el fit de la particion
            for i, item in enumerate(partitions):    #se recorren las particiones
                if (item.status == 0 and item.name == "name_t") or (item.status ==0 and space >= nueva_particion.actual_size):  #si la particion esta vacia o hay espacio disponible  
                    if i == 0: #si es la primera particion
                        byteinicio = MBR.SIZE #se le asigna el byte de inicio del MBR a la particion
                    else : #si no es la primera particion
                        byteinicio = partitions[i-1].byte_inicio+partitions[i-1].actual_size #se le asigna el byte de inicio de la particion anterior a la particion
                    probable = byteinicio+nueva_particion.actual_size #se calcula el byte de inicio de la siguiente particion
                    permiso = True #se le asigna el permiso de crear la particion
                    for j, item2 in enumerate(partitions2[(i+1):]): #se recorren las particiones
                        if probable > item2.byte_inicio and item2.byte_inicio != 0: #si el byte de inicio de la siguiente particion es mayor al byte de inicio de la particion actual
                            permiso = False #no se le asigna el permiso de crear la particion
                        
                    if permiso == True: #si se le asigno el permiso de crear la particion
                        nueva_particion.byte_inicio = byteinicio #se le asigna el byte de inicio a la particion
                        partitions[i] = nueva_particion #se le asigna la particion a la lista de particiones
                        item = nueva_particion #se le asigna la particion a la particion temporal
                        publi.ress = publi.ress + f"\nParticion {partitions[i]} creada exitosamente."
                        #print(Fore.YELLOW+f"Particion {partitions[i]} creada exitosamente.") #se imprime el mensaje de exito
                        #print(Style.RESET_ALL)
                        break  #se rompe el ciclo
            packed_objetos = b''.join([obj.pack() for obj in partitions]) #se empaquetan las particiones    
            file.seek(struct.calcsize(MBR.FORMAT)) #nos posicionamos en el inicio del archivo
            file.write(packed_objetos) #escribimos las particiones en el archivo
            if nueva_particion.type == 'E': #si la particion es extendida
                #creamoe el ebr
                ebr = EBR(ex, nueva_particion.byte_inicio) #creamos el ebr
                file.seek(nueva_particion.byte_inicio) #nos posicionamos en el byte de inicio de la particion
                file.write(ebr.pack()) #escribimos el ebr en el archivo
            
            return publi.ress
        elif nueva_particion.fit == 'BF' and realizar: #si el fit es best fit y se desea crear la particion
            nueva_particion.fit = params.get('fit', 'FF').upper() #se le asigna el fit de la particion
            sale = space+1 #se le asigna un valor a la variable sale
            indice = -1 #se le asigna un valor a la variable indice
            for i,n in enumerate(partitions): #se recorren las particiones
                print("i ",i) #se imprime el indice
                if (n.status == 0 and n.name == "name_t") and (i==0 or partitions[i-1].status == 1): #si la particion esta vacia o hay espacio disponible
                    if i == 0:
                        anterior = MBR.SIZE #se le asigna el byte de inicio del MBR a la particion
                    else :
                        anterior = partitions[i-1].byte_inicio+partitions[i-1].actual_size #se le asigna el byte de inicio de la particion anterior a la particion
                        
                    siguiente = -1     #se le asigna un valor a la variable siguiente
                    
                    
                    if i == 3 and n.status == 0: #si es la ultima particion
                        siguiente = disk_size #se le asigna el tamaño del disco a la variable siguiente
                    for j, n2 in enumerate(partitions2[(i+1):]): #se recorren las particiones
                        print("j ",j) #se imprime el indice 
                        if n2.status == 1: #si la particion esta ocupada
                            siguiente = n2.byte_inicio #se le asigna el byte de inicio de la particion a la variable siguiente
                            break #se rompe el ciclo
                        elif j ==len(partitions2[(i+1):])-1 and n2.status == 0: #si es la ultima particion y esta vacia
                            siguiente = disk_size #se le asigna el tamaño del disco a la variable siguiente
                            
                  #  print("siguiente ",siguiente) #se imprime el byte de inicio de la siguiente particion
                  #  print("anterior ",anterior) #se imprime el byte de inicio de la particion anterior
                  #  print("actual size ",nueva_particion.actual_size) #se imprime el tamaño de la particion
                  #  print("sale ",sale) #se imprime el valor de la variable sale
                    espacio = siguiente-anterior #se calcula el espacio disponible
                    #print("espacio ",espacio) #se imprime el espacio disponible
                    publi.ress = publi.ress +  "\nespacio "+str(espacio)
                  #  print(nueva_particion.actual_size <= espacio and espacio < sale) #se imprime el resultado de la comparacion
                    
                    
                    if nueva_particion.actual_size <= espacio and espacio < sale: #si el tamaño de la particion es menor o igual al espacio disponible y el espacio disponible es menor a la variable sale
                        sale = espacio #se le asigna el espacio disponible a la variable sale
                       # print("\t\tsale ",sale) #se imprime el valor de la variable sale
                        publi.ress = publi.ress + "\n\tsale "+str(sale)
                        indice = i #se le asigna el indice a la variable indice
                       # print("\t\tindice ",indice) #se imprime el valor de la variable indice
                        publi.ress = publi.ress +"\n\tindice "+str(indice)
                        byteinicio = anterior #se le asigna el byte de inicio de la particion anterior a la variable byteinicio
                       # print("\t\tbyteinicio ",byteinicio) #se imprime el valor de la variable byteinicio
                        publi.ress = publi.ress +"\n\tbyteinicio "+str(byteinicio)
            nueva_particion.byte_inicio = byteinicio #se le asigna el byte de inicio a la particion
            partitions[indice] = nueva_particion #se le asigna la particion a la lista de particiones
            #print tamano de la particion
            #print("tamaño de particiones: ",len(partitions))
            publi.ress = publi.ress +"\ntamaño de particiones: "+str(len(partitions))
            
            #print(f"se escribio la particion en el indice {indice}")
            publi.ress = publi.ress +f"\nse escribio la particion en el indice {indice}"
            packed_objetos = b''.join([obj.pack() for obj in partitions]) #se empaquetan las particiones
            file.seek(struct.calcsize(MBR.FORMAT)) #nos posicionamos en el inicio del archivo
            file.write(packed_objetos) #escribimos las particiones en el archivo
            if nueva_particion.type == 'E': #si la particion es extendida
                #creamoe el ebr
                ebr = EBR(ex, nueva_particion.byte_inicio) #creamos el ebr
                file.seek(nueva_particion.byte_inicio) #nos posicionamos en el byte de inicio de la particion
                file.write(ebr.pack()) #escribimos el ebr en el archivo
            return publi.ress
        elif nueva_particion.fit == 'WF' and realizar: #si el fit es worst fit y se desea crear la particion
            nueva_particion.fit = params.get('fit', 'FF').upper() #se le asigna el fit de la particion
            max_space = -1  # Start with a negative value as a sentinel.
            indice = -1 #se le asigna un valor a la variable indice
            for i, n in enumerate(partitions): #se recorren las particiones
                print("i ", i) #se imprime el indice
                if (n.status == 0 and n.name == "name_t") and (i == 0 or partitions[i - 1].status == 1): #si la particion esta vacia o hay espacio disponible
                    if i == 0:
                        anterior = MBR.SIZE #se le asigna el byte de inicio del MBR a la particion
                    else: 
                        anterior = partitions[i - 1].byte_inicio + partitions[i - 1].actual_size #se le asigna el byte de inicio de la particion anterior a la particion

                    siguiente = -1

                    if i == 3 and n.status == 0:
                        siguiente = disk_size
                    for j, n2 in enumerate(partitions2[(i + 1):]): #se recorren las particiones 
                        print("j ", j) #se imprime el indice
                        if n2.status == 1: #si la particion esta ocupada
                            siguiente = n2.byte_inicio #se le asigna el byte de inicio de la particion a la variable siguiente
                            break #se rompe el ciclo
                        elif j == len(partitions2[(i + 1):]) - 1 and n2.status == 0: #si es la ultima particion y esta vacia
                            siguiente = disk_size #se le asigna el tamaño del disco a la variable siguiente
                    publi.ress = publi.ress +"\nsiguiente "+str(siguiente)
                   # print("siguiente ", siguiente) #se imprime el byte de inicio de la siguiente particion
                    publi.ress = publi.ress +"\nanterior "+str(anterior)
                   # print("anterior ", anterior) #se imprime el byte de inicio de la particion anterior
                    publi.ress = publi.ress +"\nactual size "+ str(nueva_particion.actual_size)
                   # print("actual size ", nueva_particion.actual_size) #se imprime el tamaño de la particion
                    espacio = siguiente - anterior #se calcula el espacio disponible
                    publi.ress = publi.ress +"\nespacio "+ str(espacio)
                   # print("espacio ", espacio) #se imprime el espacio disponible

                    if nueva_particion.actual_size <= espacio and espacio > max_space:  #si el tamaño de la particion es menor o igual al espacio disponible y el espacio disponible es mayor a la variable max_space
                        max_space = espacio #se le asigna el espacio disponible a la variable max_space
                        #print("\t\tEspacio maximo:d ", max_space) #se imprime el valor de la variable max_space
                        publi.ress = publi.ress +"\n\tEspacio maximo:d "+str( max_space)
                        indice = i #se le asigna el indice a la variable indice
                      # print("\t\tindice ", indice) #se imprime el valor de la variable indice
                        publi.ress = publi.ress +"\n\tindice "+str(indice)
                        byteinicio = anterior #se le asigna el byte de inicio de la particion anterior a la variable byteinicio
                        #print("\t\tbyte de inicio ", byteinicio) #se imprime el valor de la variable byteinicio
                        publi.ress = publi.ress +"\n\tbyte de inicio "+ str(byteinicio)
            if indice != -1: #si el indice es diferente a -1
                nueva_particion.byte_inicio = byteinicio #se le asigna el byte de inicio a la particion
                partitions[indice] = nueva_particion #se le asigna la particion a la lista de particiones
                #print("partitions size ", len(partitions)) #se imprime el tamaño de la lista de particiones
                publi.ress = publi.ress +"\npartitions size "+ str(len(partitions))
               # print(f"se escribio la particion en el indice {indice}") #se imprime el mensaje de exito
                publi.ress = publi.ress +f"\nse escribio la particion en el indice {indice}"
                packed_objetos = b''.join([obj.pack() for obj in partitions]) #se empaquetan las particiones
                file.seek(struct.calcsize(MBR.FORMAT)) #nos posicionamos en el inicio del archivo
                file.write(packed_objetos) #escribimos las particiones en el archivo
                if nueva_particion.type == 'E': #si la particion es extendida
                    #creamos el ebr
                    ebr = EBR(ex, nueva_particion.byte_inicio) #creamos el ebr
                
                    file.seek(nueva_particion.byte_inicio) #nos posicionamos en el byte de inicio de la particion
                    file.write(ebr.pack()) #escribimos el ebr en el archivo
                return publi.ress
            else:
                publi.ress = publi.ress + "\nNo hay espacio disponible para la partición que utiliza el algoritmo WF."
                #print("No hay espacio disponible para la partición que utiliza el algoritmo WF.")
        elif 'delete' in params: #si se desea eliminar una particion
            partition_name_to_delete = params.get('name') #se obtiene el nombre de la particion a eliminar
            if not partition_name_to_delete: #si no se obtiene el nombre de la particion a eliminar
               #print("Error: No se proporciono ningun nombre de particion para eliminar.") #se imprime el error
                publi.ress = publi.ress + "\nError: No se proporciono ningun nombre de particion para eliminar."
                return publi.ress
            partition_found = False #se le asigna un valor a la variable partition_found
            for i, partition in enumerate(partitions): #se recorren las particiones
                if partition.name == partition_name_to_delete: #si el nombre de la particion es igual al nombre de la particion a eliminar
                    # confirmar la eliminacion
                   #  user_input = input(f"Está seguro de que desea eliminar la partición {partition_name_to_delete}? (s/n): ")
                   #  if user_input.lower() != "s":
                        # print("No se elimino la particion.")
                    #     publi.ress = publi.ress +"\nNo se elimino la particion."
                    #     return publi.ress

                    partition_found = True
                    # Update the partition details
                    partition.status = 0
                    partition.name = "name_t"
                    partition.type = "P"

                    packed_objetos = b''.join([obj.pack() for obj in partitions])
                    file.seek(struct.calcsize(MBR.FORMAT))
                    file.write(packed_objetos)
                   # print(Fore.BLUE+f"La particion {partition_name_to_delete} a sido eliminada correctamente.")
                    publi.ress = publi.ress +f"\nLa particion {partition_name_to_delete} a sido eliminada correctamente."
                   # print(Style.RESET_ALL)
                    return publi.ress

            if not partition_found:
                #print(Fore.RED+f"Error: La particion {partition_name_to_delete} no existe.")
                publi.ress = publi.ress +f"\nError: La particion {partition_name_to_delete} no existe."
                #print(Style.RESET_ALL)
                return publi.ress
        elif 'add' in params:
            # obtener el nombre de la particion a redimensionar
            partition_name_to_resize = params.get('name')
            if not partition_name_to_resize:
                #print("Error: No se proporciona ningún nombre de particion.")
                publi.ress = publi.ress + "\nError: No se proporciona ningún nombre de particion."
                return publi.ress

            # obtener el tamaño adicional
            try:
                additional_size = int(params['add']) # si no se proporciona el tamaño adicional, se usa 0
                unit = params.get('unit', 'K').upper()  # si no se proporciona la unidad, se usa K
                if unit == 'B':
                    multiplier = 1
                elif unit == 'K':
                    multiplier = 1024
                elif unit == 'M':
                    multiplier = 1024 * 1024
                
                additional_size = additional_size * multiplier # convertir el tamaño adicional a bytes
            except ValueError:
                #print("Error: Valor no válido para tamaño adicional.")
                publi.ress = publi.ress + "\nError: Valor no válido para tamaño adicional."
                return publi.ress

            partition_found = False #se le asigna un valor a la variable partition_found
            for i, partition in enumerate(partitions): #se recorren las particiones
                if partition.name == partition_name_to_resize: #si el nombre de la particion es igual al nombre de la particion a redimensionar
                    partition_found = True
                    
                    # si la particion es extendida, no se puede redimensionar
                    if i == len(partitions) - 1:  # si es la ultima particion
                        free_space = disk_size - (partition.byte_inicio + partition.actual_size) #se calcula el espacio disponible
                    else:
                        for j,m in enumerate(partitions2[(i + 1):]): #se recorren las particiones
                            if m.status == 1: #si la particion esta ocupada
                                free_space = m.byte_inicio - (partition.byte_inicio + partition.actual_size) #se calcula el espacio disponible
                                break
                            elif j == len(partitions2[(i + 1):]) - 1 and m.status == 0: #si es la ultima particion y esta vacia
                                free_space = disk_size - (partition.byte_inicio + partition.actual_size) #se calcula el espacio disponible
                                break
                        
                        
                        

                    # Check if we have enough space to add the additional_size
                    if additional_size <= free_space:
                        # Update the partition's size
                        partition.actual_size += additional_size
                       #  print(Fore.BLUE+f"La particion {partition_name_to_resize} ha sido redimensionada con exito.")
                        publi.ress = publi.ress + f"\nLa particion {partition_name_to_resize} ha sido redimensionada con exito."
                       #  print(Style.RESET_ALL)
                        # Update the partition table in the file
                        packed_objetos = b''.join([obj.pack() for obj in partitions])
                        file.seek(struct.calcsize(MBR.FORMAT))
                        file.write(packed_objetos)
                    else:
                       # print(Fore.BLUE+f"Error: No hay suficiente espacio para ampliar la partición {partition_name_to_resize}.")
                       # print(Style.RESET_ALL)
                        publi.ress = publi.ress +f"\nError: No hay suficiente espacio para ampliar la partición {partition_name_to_resize}."
                    return publi.ress

            if not partition_found:
               #print(f"Error: La particion {partition_name_to_resize} no fue encontrada.")
                publi.ress = publi.ress + f"\nError: La particion {partition_name_to_resize} no fue encontrada."
                return publi.ress

                    
    
     
          
    return publi.ress
    
    