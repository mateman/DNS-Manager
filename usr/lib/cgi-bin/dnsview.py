#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       sin título.py
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


import sys, cgi, os.path, socket

def conectar(mensaje):
       s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       s.connect(('server.dominio.com.ar', 1234))
       s.send(mensaje)
       texto = ''
       while True:
             recivido = s.recv(1024)
             texto += recivido
             if len(recivido)==0:
                 break 
       s.close()
       return texto

def listardominios():
     ls = (conectar('listarDominios')).replace('.dominio.com.ar','').split('\n')
     ls.sort()
     ls.remove('')
     print '''<HTML>
              <HEAD><TITLE>listardominios</TITLE></HEAD>
              <BODY>
                <fieldset id="flistar">
                 <legend>Lista de Dominios</legend>
                 <TABLE>'''
     for linea in ls:
        print '<TR><TH><IMG SRC="/images/edit.png" ALT="Ver info del Dominio" onClick="MostrarEditor(\''+linea+'\');"></TH><TD align="left"><a href="#" id="'+linea+'" onClick="MostrarDominio(\''+linea+'\');">'+linea+'</a></TD></TR>\n'
     print '''</TABLE>
            </fieldset>
           </BODY>
           </HTML>'''

def listar(dom):
     ls = (conectar('listar '+dom)).split('\n')
     print '''<HTML>
              <HEAD><TITLE>listar</TITLE></HEAD>
              <BODY>'''
     print '<fieldset id="fdominio" >\n  <legend>Lista de maquinas de '+dom+'</legend><BR>\n<TABLE>\n'
     ls.remove('')
     ls.sort()
     for linea in ls:
           (maquina,ip) = linea.split(':')
           print '<TR><TH align="left">'+maquina+'</TH><TD align="center"> IN </TD><TD align="left">'+ip+'</TD><TD><IMG SRC="/images/edit.png" ALT="Ver info del Dominio" onClick="MostrarEditor(\''+maquina+ip+'\');"></TD></TR>\n'
     ls = (conectar('listarCNAME '+dom)).split('\n')
     ls.remove('')
     ls.sort()
     for linea in ls:
           (maquina,ip) = linea.split(':')
           print '<TR><TH align="left">'+maquina+'</TH><TD align="center"> CN </TD><TD align="left">'+ip+'</TD><TD><IMG SRC="/images/edit.png" ALT="Ver info del Dominio" onClick="MostrarEditor(\''+maquina+ip+'\');"></TD></TR>\n'
     print '''</TABLE>
             </fieldset>
           </BODY>
           </HTML>'''
           
def editor(archivo):
     arch = open('/var/lib/dnsm/archivos/'+archivo , 'r')       
     for linea in arch:
            print linea+'\n'
     arch.close()

def savedoc(a):
     arch = open('/var/lib/dnsm/dnsview/TelefonosDoc' , 'w')
     arch.write(a)
     arch.close()

def verdoc():
     arch = open('/var/lib/dnsm/dnsview/TelefonosDoc' , 'r')       
     for linea in arch:
            print linea+'\n'
     arch.close()

def saveplani(c):
     arch = open('/var/lib/dnsm/dnsview/Planilla' , 'w')
     arch.write(c)
     arch.close()
     
def verplani():
     arch = open('/var/lib/dnsm/dnsview/Planilla' , 'r')       
     for linea in arch:
            print linea+'\n'
     arch.close()

def verinfo():
     ls = (conectar('listarDominios')).replace('.dominio.com.ar','').split('\n')
     ls.sort()
     ls.remove('')
     for linea in ls:
        if os.path.exists('/var/lib/dnsm/archivos/'+linea):
             arch = open('/var/lib/dnsm/archivos/'+linea , 'r')       
             for larch in arch.readlines():
                 print larch+'\n'
             arch.close()
             print '<BR>'   

def mail(servidor):
      s = socket.socket()
      s.connect((servidor, 1235))
      mens = s.recv(1024)
      s.send('listar.pl')
      texto = ''
      while True:
             recivido = s.recv(1024)
             texto += recivido
             if len(recivido)<1024:
                 break 
      s.close()
      lista = texto.split('\n')
      lista.sort()
      print '''
              <HTML>
              <HEAD><TITLE>mails</TITLE></HEAD>
              <BODY>'''
      print '<fieldset id="fmail" >\n  <legend>Lista de mails de '+servidor+'</legend><BR>\n<TABLE>\n'
      for linea in lista:
                  print '<TR>'
                  for ls in linea.split(','):
                        print '<TD>'+ls+'</TD>'
                  print '</TR>\n'
                  print '''</TABLE>
             </fieldset>
           </BODY>
           </HTML>'''



def main():
     print 'Content-type: text/html\n'	
     form = cgi.FieldStorage()	# parse query
     if form.has_key("listar") and form["listar"].value != "":
           listar(str(form['listar'].value))
     elif form.has_key("listardominios"):
           listardominios()
     elif form.has_key("editor") and form["editor"].value != "":
           editor(str(form['editor'].value))
     elif form.has_key("verinfo"):
           verinfo()
     elif form.has_key("verdoc"):
           verdoc()
     elif form.has_key("savedoc") and form["savedoc"].value != "":
           savedoc(str(form["savedoc"].value))
     elif form.has_key("verplani"):
           verplani()
     elif form.has_key("saveplani") and form["saveplani"].value != "":
           saveplani(str(form["saveplani"].value))
     elif form.has_key("mail") and form["mail"].value != "":
           mail(str(form["mail"].value))
     else:
         print "Error! comando no reconocido"


if __name__ == '__main__':
     main()

