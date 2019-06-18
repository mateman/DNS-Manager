#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#      zone.py
#       
#       Copyright 2011 Pablo Adolfo Cuyeu <mateman@ubuntu>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import re,os, datetime


class Zones:

   def __init__(self,unString):
      self.archivo = unString
              
   def listar(self):
       arch = open(self.archivo, 'r')
       dic = {}
       adentro = False
       for linea in arch:
           eszone = re.match('^zone\s+"([\w\-\.]+)"\s*{',linea.encode())
           nozone = re.match('^zone\s+"(\d+\.\d+\.\d+)\.((IN-ADDR.ARPA)|(in-addr.arpa))"\s*{',linea.encode())
           if eszone and not nozone:
               mizone = eszone.group(1)
               adentro = True
           esfile = re.match('^\s*file\s+"([\w\-\.\/]+)";',linea.encode())
           if esfile and adentro:
               dic[mizone] = esfile.group(1)
               adentro = False
       arch.close()
       return dic
          
   def listarInversa(self):
       arch = open(self.archivo, 'r')
       dic = {}
       adentro = False
       for linea in arch:
           eszone = re.match('^zone\s+"(\d+\.\d+\.\d+)\.((IN-ADDR.ARPA)|(in-addr.arpa))"\s*{',linea.encode())
           if eszone:
               mizone = eszone.group(1)
               mizone = '.'.join([i for i in reversed(mizone.split('.'))])
               adentro = True
           esfile = re.match('^\s*file\s+"([\w\-\.\/]+)";',linea.encode())
           if esfile and adentro:
               dic[mizone] = esfile.group(1)
               adentro = False
       arch.close()
       return dic
    
   def existe(self, unValor):
        d = self.listar()
        return unValor in d
        
   def existeInversa(self, unValor):
        d = self.listarInversa()
        return unValor in d

   def agregar(self, unaZone, unArchivo):
        valor = not self.existe(unaZone)       
        if valor:
            arch = open(self.archivo, 'a') 
            arch.write('zone "'+unaZone+'"{\n        type slave;\n        file "'+unArchivo+'";\n        masters {10.40.1.1; };\n};\n')
            arch.close()
        return valor

   def eliminar(self, unValor):
       arch = open(self.archivo, 'r')
       archresg = open(self.archivo+'~','w')
       guardado = True
       ret = None
       for linea in arch:
           eszone = re.match('^zone\s+"([\w\-\.]+)"\s*{',linea.encode())
           if eszone:
               guardado = not (eszone.group(1) == unValor)
               ret = unValor
           if guardado:
               archresg.write(linea.encode())
       archresg.close()
       arch.close()
       os.remove(self.archivo)
       os.rename(self.archivo+'~',self.archivo)
       return ret    

   def agregarInversa(self, unaZone, unArchivo):
        valor = not self.existeInversa(unaZone)       
        if valor:
            arch = open(self.archivo, 'a') 
            arch.write('zone "'+'.'.join([i for i in reversed(unaZone.split('.'))])+'.IN-ADDR.ARPA"{\n        type slave;\n        file "'+unArchivo+'";\n        masters {10.40.1.1; };\n};\n')
            arch.close()
        return valor

   def eliminarInversa(self, unValor):
       return self.eliminar('.'.join([i for i in reversed(unValor.split('.'))])+'.IN-ADDR.ARPA')



def agregarDominio(unDom):
    n = Zones('/etc/bind/named.conf.local')
    n.agregar(unDom,'/etc/bind/zonas/'+unDom)
    return 'True'
    
def eliminarDominio(unDom):
    n = Zones('/etc/bind/named.conf.local')
    if n.existe(unDom):
        d = Zone(n.listar()[unDom],unDom)
        dd = d.listar()
        for maq in dd.keys():
           eliminar(maq+'.'+unDom)
        os.remove(n.listar()[unDom])
        return 'eliminado '+ n.eliminar(unDom)
    return 'No existe dominio'

def main():  
        return 0

if __name__ == '__main__':
        main()
