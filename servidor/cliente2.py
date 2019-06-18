#!/usr/bin/env python
#+----------------------------------+
#| Client TCP/IP                    |
#+----------------------------------+

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#invoco el metodo connect del socket pasando como parametro la tupla IP , puerto
s.connect(("testing.dominio.com.ar", 1235))

while True:
  mensaje = raw_input("Mensaje a enviar: ")

  #invoco el metodo send pasando como parametro el string ingresado como comando a ejecutar
  s.send(mensaje)
  texto = ''
  while True:
     recivido = s.recv(1024)
     texto += recivido
     if len(recivido)==0:
        break  
  print texto
  if mensaje == "salir":
    break

print "adios"

#cierro socket
s.close()

