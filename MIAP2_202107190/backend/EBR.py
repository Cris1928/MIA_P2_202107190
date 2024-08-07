import os
import struct
import time
import random
from part import Partition
from ress import publi
class EBR:
  
    FORMAT = 'i c c i i 16s i'
    SIZE = struct.calcsize(FORMAT)
    def __init__(self, params, start):
        unit = params.get('unit', 'M').upper()
        self.actual_size = params.get('size')
        
        if self.actual_size < 0:
            raise ValueError("El tamaño debe ser un numero mayor a 0")

        unit = params.get('unit', 'K').upper()
        if unit == 'B':
            self.actual_size = self.actual_size
        elif unit == 'K':
            self.actual_size = self.actual_size * 1024
        elif unit == 'M':
            self.actual_size = self.actual_size * 1024 * 1024
        self.fit = params.get('fit', 'FF').upper()
        self.status = 0
        self.type = params.get('type','L').upper()
        self.start = start
        self.name = params.get('name')
        if not self.name:
            raise ValueError("El nombre de la partición no puede estar vacío")
        self.next = -1
        
        
    def __str__(self):
        return f"EBR: name={self.name}, size={self.actual_size} bytes, next={self.next}"
    
    def pack(self):
        fit_char = self.fit[0].encode()  # Take the first character of fit type and encode it
        #FORMAT = 'i c c i i 16s i'
        packed_mbr = struct.pack(self.FORMAT, self.status,fit_char, self.type.encode('utf-8'), self.start, self.actual_size, self.name.encode('utf-8'), self.next)
        return packed_mbr
    @classmethod
    def unpack(cls, data):
       # print("\nDESEMPAQUETANDO EBR...")
        publi.ress = publi.ress + "\nDESEMPAQUETANDO EBR..."

        unpacked_data = struct.unpack(cls.FORMAT, data)
        ex = {'size': 1, 'path': 'path', 'name': 'name_t'}
        ebr = cls(ex,-1)
        ebr.status = unpacked_data[0]
        fit_char = unpacked_data[1].decode()  
        fit_map = {'B': 'BF', 'F': 'FF', 'W': 'WF', 'N': 'NF'}
        ebr.fit = fit_map[fit_char]
        ebr.type = unpacked_data[2].decode('utf-8')
        ebr.start = unpacked_data[3]
        ebr.actual_size = unpacked_data[4]
        ebr.name = unpacked_data[5].decode('utf-8').strip('\x00')
        ebr.next = unpacked_data[6]
        return ebr
        