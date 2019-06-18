#!/usr/bin/env python

# Ensure that the local library is loaded first.  Normally you don't
# want to do this.
import sys, time, socket, DNSManager, os
sys.path.insert(0, '/home/myhome/daemonize/')

import daemonize

def main():
      #Creo el objeto socket
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

      PUERTO = 1234

      #Invoco al metodo bind, pasando como parametro una tupla con nombre y puerto
      #s.bind(("localhost", 9999)), socket.gethostname() <- me da el nombre del host para usar en publico

      s.bind((socket.gethostname(), PUERTO))
  
      #Invoco el metodo listen para escuchar conexiones con el numero maximode conexiones como parametro
      s.listen(8)
  
      #El metodo accept bloquea la ejecucion a la espera de conexiones
      #accept devuelve un objeto socket y una tupla Ip y puerto
      so = open('/tmp/daemon-write.txt', 'a+')
      while True:
           sc, addr = s.accept()
           so.write("Recibo conexion de la IP: " + str(addr[0]) + " Puerto: " + str(addr[1]))
           ingreso = []
           texto = ''
           while True:
                recivido = sc.recv(1024)
                texto += recivido
                if len(recivido)<1024:
                       break 
                so.write( "Recibido: "+texto)
           ver = texto.split(' ')
           for val in ver:
                  if val:
                    ingreso.append(val)
           if ingreso[0] == "salir":
                     break
           elif ingreso[0] == 'agregar':
                     sc.send(str(DNSManager.agregar(ingreso[1], ingreso[2])))
           elif ingreso[0] == 'eliminar':
                     sc.send(str(DNSManager.eliminar(ingreso[1])))
           elif ingreso[0] == 'agregarDominio':
                     sc.send(DNSManager.agregarDominio(ingreso[1]))
           elif ingreso[0] == 'eliminarDominio':
                     sc.send(DNSManager.eliminarDominio(ingreso[1]))
           elif ingreso[0] == 'agregarCNAME':
                     sc.send(str(DNSManager.agregarCNAME(ingreso[1], ingreso[2])))
           elif ingreso[0] == 'eliminarCNAME':
                     sc.send(str(DNSManager.eliminarCNAME(ingreso[1])))
           elif ingreso[0] == 'listar':
                     sc.send(DNSManager.listar(ingreso[1]))
           elif ingreso[0] == 'listarDominios':
                     sc.send(DNSManager.listarDominios())
           elif ingreso[0] == 'listarCNAME':
                     sc.send(DNSManager.listarCNAME(ingreso[1]))
           elif ingreso[0] == 'setSerial':
                     sc.send(DNSManager.setSerial(ingreso[1]))
           elif ingreso[0] == 'reiniciarDNS':
                     sc.send(str(os.system('/etc/init.d/bind9 restart')))
           else: sc.send('Comando no reconocido')
           sc.close()
      so.close()
      s.close()


daemonize.start(main, debug=False)
