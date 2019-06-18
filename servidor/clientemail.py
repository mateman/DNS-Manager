#+----------------------------------+ 
#| Client TCP/IP                    | 
#+----------------------------------+ 

import socket 

s = socket.socket() 

#invoco el metodo connect del socket pasando como parametro la tupla IP , puerto 
s.connect(("server.dominio.com.ar", 1234)) 
while True: 
  mensaje = raw_input("Mensaje a enviar: ") 

#invoco el metodo send pasando como parametro el string ingresado por el usuario 
  print s.recv(1024)
  s.send(mensaje) 

  if mensaje == "salir": break 
  print "adios" 

#cierro socket 
  s.close()
