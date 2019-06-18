#!/usr/bin/env python
#+----------------------------------+ 
#| Client TCP/IP                    | 
#+----------------------------------+ 

import socket 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#invoco el metodo connect del socket pasando como parametro la tupla IP , puerto 
s.connect(("server.dominio.com.ar", 1234)) 
while True: 
   mensaje = raw_input("Mensaje a enviar: ") 
   if mensaje == "salir": 
         break 
#invoco el metodo send pasando como parametro el string ingresado por el usuario 
   s.send(mensaje) 
   texto = ''
   while True:
          recivido = s.recv(1024)
          texto += recivido
          if len(recivido)==0:
                  break
   print texto 
#cierro socket 
print "adios"
s.close()
