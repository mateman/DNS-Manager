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

class Zone:
  
   def __init__(self,unString,unDom):
      self.archivo = unString
      if not(os.path.exists(unString) and os.path.isfile(unString)):
          arch = open(unString, 'w')
          arch.write('$ORIGIN .\n$TTL 7200	; 2 hours\n; Creado automaticamente por DNSManager \n; con el nombre: '+unString+'\n')
          arch.write(unDom+'	IN SOA	server.dominio.com.ar. root.gob.gba.gov.ar. (\n				')
          arch.write(str((datetime.datetime.today()).date()).replace('-','')+'00 ; serial\n				43200      ; refresh (12 hours)\n')
          arch.write ('				900        ; retry (15 minutes)\n				604800     ; expire (1 week)\n				3600       ; minimum (1 hour)\n				)\n')
          arch.write(' 			NS	server.gob.gba.gov.ar.\n			NS	servidor.dominio.com.ar.\n			MX	10 mail.dominio.com.ar.\n			MX	20 mx1.dominio.com.ar.\n			MX	100 relay-1.gba.gov.ar.\n			MX	200 relay-2.gba.gov.ar.\n			MX	300 relay-14.gba.gov.ar.\n			MX	400 relay-13.gba.gov.ar.\n			MX	500 relay-12.gba.gov.ar.\n')
          arch.write('$ORIGIN '+unDom+'.\n')
          arch.close()
 
## Formato con el que crea al archivo de Zone
##
##$ORIGIN .
##$TTL 7200	; 2 hours
##1.40.10.in-addr.arpa	IN SOA	server.dominio.com.ar. root.dominio.com.ar. (
##				2011051000 ; serial
##				43200      ; refresh (12 hours)
##				900        ; retry (15 minutes)
##				604800     ; expire (1 week)
##				3600       ; minimum (1 hour)
##				)
## 			NS	server.dominio.com.ar.
##			NS	servidor.dominio.com.ar.
##			MX	10 mail.dominio.com.ar.
##			MX	20 mx1.dominio.com.ar
.
##			MX	100 relay-1.dominio.com.ar.
##			MX	200 relay-2.dominio.com.ar.
##			MX	300 relay-14.dominio.com.ar.
##			MX	400 relay-13.dominio.com.ar.
##			MX	500 relay-12.dominio.com.ar.
##$ORIGIN 1.40.10.in-addr.arpa.
##         
          
   def listar(self):
       arch = open(self.archivo, 'r')
       dic = {}
       for linea in arch:
           par = re.match("^([\d\w\-\.]+)\s+(A|PTR)\s+([\d\w\-\.]+)",linea.encode())
           if par:
              dic[par.group(1)] = par.group(3)
       arch.close()
       return dic
          
   def listarCNAME(self):
       arch = open(self.archivo, 'r')
       dic = {}
       for linea in arch:
           par = re.match("^([\d\w\-\.]+)\s+(CNAME)\s+([\d\w\-\.]+)",linea.encode())
           if par:
              dic[par.group(1)] = par.group(3)
       arch.close()
       return dic
    
   def existe(self, unValor):
        d = self.listar()
        return unValor in d
    
   def existeCNAME(self, unValor):
        d = self.listarCNAME()
        return unValor in d
            
   def agregar(self, unValor, unaAsociacion):
        valor = not(self.existe(unValor) or self.existeCNAME(unValor)) 
        if valor:
            arch = open(self.archivo, 'a')
            if ((re.match('([\d]+)',unValor)) and (re.match('([\w\d\-\.]+)',unaAsociacion))):
                arch.write(unValor+'\t\t\tPTR\t'+unaAsociacion+'.\n')
            elif ((re.match('([\w\d\-\.]+)',unValor)) and (re.match('([\d\.]+)',unaAsociacion))):
                arch.write(unValor+'\t\t\tA\t'+unaAsociacion+'\n')
            arch.close()
        return valor

   def eliminar(self, unValor):
       arch = open(self.archivo, 'r')
       archresg = open(self.archivo+'~','w')
       ret = None
       for linea in arch:
           par = re.match("^("+unValor.encode()+")\s+(A|PTR)\s+([\d\w\-\.]+)",linea.encode())
           if par:
                ret = (par.group(1),par.group(3))
           else:
               archresg.write(linea.encode())
       archresg.close()
       arch.close()
       os.remove(self.archivo)
       os.rename(self.archivo+'~',self.archivo)
       return ret

   def agregarCNAME(self, unValor, unaAsociacion):
        valor = not(self.existeCNAME(unValor) or self.existe(unValor))      
        if valor:
            arch = open(self.archivo, 'a') 
            arch.write(unValor+'     CNAME          '+unaAsociacion+'\n')
            arch.close()
        return valor

   def eliminarCNAME(self, unValor):
       arch = open(self.archivo, 'r')
       archresg = open(self.archivo+'~','w')
       ret = None
       for linea in arch:
           par = re.match("^("+unValor.encode()+")\s+(CNAME)\s+([\d\w\-\.]+)",linea.encode())
           if par:
                ret = (par.group(1),par.group(3))
           else:
               archresg.write(linea.encode())
       archresg.close()
       arch.close()
       os.remove(self.archivo)
       os.rename(self.archivo+'~',self.archivo)
       return ret

   def setSerial(self):
       arch = open(self.archivo, 'r')
       archresg = open(self.archivo+'~','w')
       adentro = False
       listo = False
       for linea in arch:
           if not listo:
                 esSOA = re.match('^([\d\w\-\.]*)\s+(IN SOA)\s+([\d\w\-\.\s]*)\(\n',linea.encode())
                 if esSOA and not adentro:
                      adentro = True
                 esSerial = re.match('^([\s\w]*)(\d{10})([\s\w;\n]*)',linea.encode())
                 if esSerial and adentro:
                      newSerial = str((datetime.datetime.today()).date()).replace('-','')
                      valor = int(esSerial.group(2))
                      if valor < int(newSerial+'00'):
                         linea = str(esSerial.group(1))+newSerial+'00'+str(esSerial.group(3))
                      else:
                         linea = esSerial.group(1)+str(int(esSerial.group(2))+1)+esSerial.group(3)
                      listo = True
           archresg.write(linea.encode())
       archresg.close()
       arch.close()
       os.remove(self.archivo)
       os.rename(self.archivo+'~',self.archivo)

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
            arch.write('zone "'+unaZone+'"{\n        type master;\n        file "'+unArchivo+'";\n        notify yes;\n};\n')
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
            arch.write('zone "'+'.'.join([i for i in reversed(unaZone.split('.'))])+'.IN-ADDR.ARPA"{\n        type master;\n        file "'+unArchivo+'";\n        notify yes;\n};\n')
            arch.close()
        return valor

   def eliminarInversa(self, unValor):
       return self.eliminar('.'.join([i for i in reversed(unValor.split('.'))])+'.IN-ADDR.ARPA')

def agregar(unDom, unaIP):
    n = Zones('/etc/bind/named.conf.local') 
    if not(n.existe('.'.join(unDom.split('.')[1:]))):
        n.agregar('.'.join(unDom.split('.')[1:]),'/etc/bind/zonas/'+'.'.join(unDom.split('.')[1:]))
    if not(n.existeInversa('.'.join(unaIP.split('.')[:-1]))):
        n.agregarInversa('.'.join(unaIP.split('.')[:-1]),'/etc/bind/zonas/'+'.'.join(unaIP.split('.')[:-1]))
    d = Zone(n.listar()['.'.join(unDom.split('.')[1:])],'.'.join(unDom.split('.')[1:]))
    i = Zone(n.listarInversa()['.'.join(unaIP.split('.')[:-1])],'.'.join(reversed(unaIP.split('.')[:-1]))+'.IN-ADDR.ARPA')
    if (d.existe(unDom.split('.')[0]))or(i.existe(unaIP.split('.')[-1])):
        return 'Existe!'
    else:
        d.agregar(unDom.split('.')[0],unaIP)
        i.agregar(unaIP.split('.')[-1],unDom)
        i.setSerial()
        return ' Agregado con exito!'
    
def eliminar(unDom):
    n = Zones('/etc/bind/named.conf.local') 
    if not(n.existe('.'.join(unDom.split('.')[1:]))):
        return 'No existe Dominio'
    else:
        d = Zone(n.listar()['.'.join(unDom.split('.')[1:])],'.'.join(unDom.split('.')[1:]))
        unaIP = d.listar()[unDom.split('.')[0]]
        d.eliminar(unDom.split('.')[0])
        i = Zone(n.listarInversa()['.'.join(unaIP.split('.')[:-1])],'.'.join(reversed(unaIP.split('.')[:-1]))+'.IN-ADDR.ARPA')
        i.eliminar(unaIP.split('.')[-1])
        i.setSerial()
        return 'Eliminado'

def listar(unDom):
    n = Zones('/etc/bind/named.conf.local') 
    if not(n.existe(unDom)):
        return 'No existe Dominio'
    else:
        s=''
        d = Zone(n.listar()[unDom],unDom)
        dd = d.listar()
        for e in dd.keys():
            s+=(e+' : '+dd[e]+'\n')
        return s

def agregarCNAME(unCN, unDom):
    n = Zones('/etc/bind/named.conf.local') 
    if not(n.existe('.'.join(unCN.split('.')[1:]))):
        n.agregar('.'.join(unCN.split('.')[1:]),'/etc/bind/zonas/'+'.'.join(unCN.split('.')[1:]))
    if not(n.existe('.'.join(unDom.split('.')[1:]))):
        return 'No existe maquina con ese dominio'
    d = Zone(n.listar()['.'.join(unCN.split('.')[1:])],'.'.join(unCN.split('.')[1:]))
    if (d.existe(unCN.split('.')[0])):
        return 'Existe ya ese nombre en una maquina!'
    else:
        d.agregarCNAME(unCN.split('.')[0],unDom)
        return ' Agregado con exito!'
    
def eliminarCNAME(unCN):
    n = Zones('/etc/bind/named.conf.local') 
    if not(n.existe('.'.join(unCN.split('.')[1:]))):
        return 'No existe Dominio'
    else:
        d = Zone(n.listar()['.'.join(unCN.split('.')[1:])],'.'.join(unCN.split('.')[1:]))
        d.eliminarCNAME(unCN.split('.')[0])
        return 'Eliminado'
        
def listarCNAME(unDom):
    n = Zones('/etc/bind/named.conf.local') 
    if not(n.existe(unDom)):
        return 'No existe Dominio'
    else:
        s=''
        d = Zone(n.listar()[unDom],unDom)
        dd = d.listarCNAME()
        for e in dd.keys():
            s+=(e+' : '+dd[e]+'\n')
        return s

def setSerial(unDom):
     n = Zone('/etc/bind/zonas/'+unDom,unDom)
     n.setSerial()

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
    
def listarDominios():
    n = Zones('/etc/bind/named.conf.local')
    dd = n.listar()
    s = ''
    for d in dd.keys():
       s += d+'\n'
    return s

       
def main():  
        return 0

if __name__ == '__main__':
        main()
