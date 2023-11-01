import os
import struct
import time
import random
from ress import publi
class Partition:
    # Usa el mismo formato que el MBR
    FORMAT = 'i 16s c c i c i'
    SIZE = struct.calcsize(FORMAT)

    def __init__(self, params):
     # estrae los parametros del diccionario
        self.actual_size = params.get('size')
        print("quiero ver", self.actual_size)
        
        if int(self.actual_size) < 0:
            publi.ress = publi.ress + "tamañño de particion no puede ser negativo"
            raise publi.ress 

        # Extrae el path del diccionario

      
        self.name = params.get('name')
        if not self.name:
            raise ValueError("nombre de la particon requrido")

        # Extrae el unit del diccionario
        self.unit = params.get('unit', 'K').upper()
        if self.unit not in ['B', 'K', 'M']:
            raise ValueError(f"Invalid unit: {self.unit}")

        # Calcula el tamaño real de la particion
        if self.unit == 'B':
            self.actual_size = self.actual_size
        elif self.unit == 'K':
            self.actual_size = self.actual_size * 1024
        elif self.unit == 'M':
            self.actual_size = self.actual_size * 1024 * 1024
        self.type = params.get('type', 'P').upper()
        self.status = 0
        #add the fit parameter too
        self.fit = params.get('fit', 'FF').upper()
        self.byte_inicio = 0
        

    def __str__(self):
        return f"Partition: name={self.name}, size={self.actual_size} bytes,  unit={self.unit}, type={self.type}"

    def pack(self):
        fit_char = self.fit[0].encode() 
        packed_partition = struct.pack(self.FORMAT, self.actual_size, self.name.encode('utf-8'), self.unit.encode('utf-8'), self.type.encode('utf-8'), self.status, fit_char, self.byte_inicio)
        return packed_partition

    @classmethod
    def unpack(cls, data):
        unpacked_data = struct.unpack(cls.FORMAT, data)
        ex = {'size': 10, 'path': 'path', 'name': 'name'}
        partition = cls(ex)
        partition.actual_size = unpacked_data[0]
        partition.name = unpacked_data[1].decode('utf-8').strip('\x00')
        partition.unit = unpacked_data[2].decode('utf-8')
        partition.type = unpacked_data[3].decode('utf-8')
        partition.status = unpacked_data[4]
        fit_char = unpacked_data[5].decode()
        fit_map = {'B': 'BF', 'F': 'FF', 'W': 'WF', 'N': 'NF'}
        partition.fit = fit_map[fit_char]
        partition.byte_inicio = unpacked_data[6]
        
            
        return partition
