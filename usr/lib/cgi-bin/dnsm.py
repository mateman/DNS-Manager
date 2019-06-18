#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       dnsm.py
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

import sys, cgi, os, hashlib, socket, time

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
       
def conectarSlave(mensaje):
       s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       s.connect(('servidor.dominio.com.ar', 1234))
       s.send(mensaje)
       texto = ''
       while True:
             recivido = s.recv(1024)
             texto += recivido
             if len(recivido)==0:
                 break 
       s.close()
       return texto

def imprimirPagina(texto,color):
   print '''<HTML>
              <HEAD><TITLE>comentario</TITLE></HEAD>
              <BODY>
                <fieldset id="fb" align="center">'''
   print '<P>'+texto+'</P>'
   print '<input type="hidden" id="colorb" value='+color+'>'
   print '''    <input type="hidden" id="valido" value="true">
                </fieldset>
              </BODY>
           </HTML>'''


def reiniciarDNS():
   if conectar('reiniciarDNS')=='0':
      if conectarSlave('reiniciarDNS')=='0':
         imprimirPagina('Reiniciando DNS ','#00FF00')
      else: imprimirPagina('Fallo reinicio de Servidor ','#FF0000')
   else: imprimirPagina('No se pudo reiniciar Server','#FF0000')
   
   
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
        print '<TR><TH><IMG SRC="/images/edit.png" ALT="Ver info del Dominio" onClick="MostrarEditor(\''+linea+'\');"></TH><TD align="left"><a href="#" id="'+linea+'" onClick="MostrarDominio(\''+linea+'\');">'+linea+'</a></TD><TD><IMG SRC="/images/trash-16x16.png" ALT="Eliminar este Dominio" onClick="EliminarZona(\''+linea+'.dominio.com.ar\');"></TD></TR>\n'
     print '''</TABLE>
            </fieldset>
           </BODY>
           </HTML>'''

def agregarDominio(dom):
    texto = conectar('agregarDominio '+dom)
    if texto =='True':
		textoSlave = conectarSlave('agregarDominio '+dom)
		if textoSlave =='True':
            imprimirPagina('Agregado '+dom,'#00FF00')
        else: imprimirPagina('Error al crear '+dom+' en Servidor','#00FF00')
    else: imprimirPagina('No se pudo agregar','#FF0000')

def eliminarDominio(dom):
    texto = conectar('eliminarDominio '+dom)
    textoSlave = conectarSlave('eliminarDominio '+dom)
    imprimirPagina( 'Eliminado '+texto,'#00FF00')

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
           print '<TR><TH align="left">'+maquina+'</TH><TD align="center"> IN </TD><TD align="left">'+ip+'</TD><TD><IMG SRC="/images/edit.png" ALT="Ver info del Dominio" onClick="MostrarEditor(\''+maquina+ip+'\');"></TD><TD><IMG SRC="/images/trash-16x16.png" ALT="Borrar un dominio" onClick="BorrarDominio(\''+str(maquina+'.'+dom).replace(' ','')+'\');"></TD></TR>\n'
     ls = (conectar('listarCNAME '+dom)).split('\n')
     ls.remove('')
     ls.sort()
     for linea in ls:
           (maquina,ip) = linea.split(':')
           print '<TR><TH align="left">'+maquina+'</TH><TD align="center"> CN </TD><TD align="left">'+ip+'</TD><TD><IMG SRC="/images/edit.png" ALT="Ver info del Dominio" onClick="MostrarEditor(\''+maquina+ip+'\');"></TD><TD><IMG SRC="/images/trash-16x16.png" ALT="Borrar un alias" onClick="BorrarCNAME(\''+str(maquina+'.'+dom).replace(' ','')+'\');"></TD></TR>\n'
     print '''</TABLE>
             </fieldset>
           </BODY>
           </HTML>'''

def agregar(maq,ip):
    texto = conectar('agregar '+maq+' '+ip)
    imprimirPagina(texto,'#00FF00')

def eliminar(dom):
    texto = conectar('eliminar '+dom)
    imprimirPagina(texto+' '+dom,'#00FF00')

def agregarCNAME(cn,maq):
    texto = conectar('agregarCNAME '+cn+' '+maq)
    imprimirPagina(cn+'  '+texto,'#00FF00')    

def eliminarCNAME(dom):
    texto = conectar('eliminarCNAME '+dom)
    imprimirPagina(dom+' : '+texto,'#00FF00')

def editor(archivo):
     arch = open('/var/lib/dnsm/archivos/'+archivo , 'r')       
     for linea in arch:
            print linea+'\n'
     arch.close()

def saveedit(a,c):
     arch = open('/var/lib/dnsm/archivos/'+a , 'w')
     arch.write(c)
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


def nuevo(login,pwd):
      arch = open('/var/lib/dnsm/claves.txt' , 'r')
      d={}
      for linea in arch:
             linea = ''.join([ c for c in linea if c not in ('\n')])
             ls=linea.split(':')
             if ls[0]:
                  d[ls[0]] = ls[1]
      arch.close()
      if login in d and d[login]== hashlib.md5(pwd).hexdigest():
            session = str(time.time())
            archsession = open('/var/lib/dnsm/session/'+session, 'w')
            archsession.write('logeado: '+login+' a las:'+time.ctime()+'\n')
            archsession.close
#####Queda obsoleta la lectura del archivo de la pagina...... 
#           arch = open('/var/lib/dnsm/dnsmanager.html' , 'r')
#           for linea in arch.readlines():
#                      print linea
#           arch.close()
##################
            print '''
<html>
  <head>
     <title>DNSManager</title>
     <script src="../funciones-ajax.js"></script>
     <script type="text/javascript" src=" ../ckeditor/ckeditor.js"></script>
     <LINK REL="stylesheet" TYPE="text/css" HREF="../divstyle.css">
  </head>
  <body  bgcolor="#CDCDCD" onload="MostrarLista()">
     <DIV id="divform" name="dform"  align="left">'''
            print '<input type="hidden" id="sessionval" value="'+session+'">'
            print '''
         <TABLE>
            <TR><TH><input type="button" name="reiniciar"   id="reiniciar" value="Reiniciar DNS" onClick="ReiniciarDNS()"></TH><TD><IMG SRC="/images/info.png" ALT="Ver Delegaciones Total" align="left" onClick="verinfo();"></IMG>Armar Delegaciones Total</TD></TR>
            <TR><TH><input type="button" name="czone"   id="crearzone" value="Crear una zona" onClick="document.getElementById('divzona').style.visibility= 'visible';"></TH><TD align="left" ><input type="button" name="cdominio"   id="creardominio" value="Crear un dominio" onClick="document.getElementById('divcrear').style.visibility= 'visible';"><input type="button" name="ccname"   id="crearcname" value="Crear un alias de dominio" onClick="document.getElementById('divcrearalia').style.visibility= 'visible';"></TD></TR>
         </TABLE>  
    </DIV>
    <DIV id="divlistar" name='dlistar' align="left">
    </DIV>
    <DIV id="divdominio" name='ddominio' align="left">
        <fieldset id="fdominio">
        </fieldset>
    </DIV>
    <DIV id="divedit" name='dedit' align="left">
        <fieldset id="fedit">
         <A id='cdomi'>dominio.com.ar</A>
         <FORM action="script:saveedit()">
         <textarea class="ckeditor" cols="80" id="editor1" name="editor1" rows="10">Esto es un ejemplo </textarea>
           <input type="button" name="bcerrar"   id="botcerrar" value="Cerrar" onClick="veredit(false)">
           <input type="button" name="bsave"   id="botsave" value="Guardar" onClick="saveedit()">
         </FORM>  
         </fieldset>
    </DIV>
    <DIV id="espera" name="espera" align="center">
        <I width="72%"><B>Cargando...</B></I>
    </DIV>
    <DIV id="divcrear" name='divcrear' align="left">
        <fieldset id="fcrear">
        <A>Crear un dominio</A><BR>
        <TABLE>
           <TR><TH><P ALIGN="left">Nombre de la maquina: </P></TH><TD><input type=text name="maquina" id="maquinaagregar" size=20 maxlength=85 onBlur="verifica_agregar(this);" ></TD></TR>
           <TR><TH><P ALIGN="left">IP:</P></TH><TD><input type=text name="ip" id="ipagregar" size=15 maxlength=15 onBlur="verificaIp(this);"></TD></TR>
        </TABLE>
        <BR>
        <P><input type="button" value="Crear dominio" id="botoncreardominio" onClick="agregar();"></P>
        </fieldset>
    </DIV>

    <DIV id="divcrearalia" name='divcrearalia' align="left">
        <fieldset id="fcrearalia">
         <A>Crear un alias dominio</A><BR>
         <TABLE>
           <TR><TH><P ALIGN="left">Nombre del alias: </P></TH><TD><input type=text name="alias" id="alias" size=20 maxlength=28 onBlur="verifica_agregar(this);" ></TD></TR>
           <TR><TH><P ALIGN="left">Nombre de la maquina: </P></TH><TD><input type=text name="maquinaalias" id="maquinaalias" size=20 maxlength=85 onBlur="verifica_agregar(this);"></TD></TR>
         </TABLE>
         <BR>
         <P><input type="button" value="Crear alias" id="botoncrearalias" onClick="agregarCNAME();"></P>
        </fieldset>
    </DIV>

    <DIV id="divzona" name='divzona' align="left">
      <fieldset id="fzona">
       <A>Crear una zona</A><BR>
       <TABLE>
         <TR><TH><P ALIGN="left">Nombre de la zona: </P></TH><TD><input type=text name='agregarzona' id='agregarzona' size=20 maxlength=85 onBlur="verifica_agregar(this)" ></TD><TD><input type="button" id="agregarDominio" value="agregar un Dominio"  onClick="agregarDominio();"></TD></TR>
       </TABLE>
       <BR>
      </fieldset>
     </DIV>

     <DIV id='divb' name='divb' align="left">
         <input type="hidden" id="colorb" value="#00FF00">
         <input type="hidden" id="valido" value="true">
     </DIV>


     <DIV id="divsession" name='divsession' align="center">
        <fieldset id="fsession">
         <P ALIGN="center">Su sesi&oacute;n </P>
         <P ALIGN="center">ha caducado </P>
         <P ALIGN="center">Por FAVOR vuelva a loguearse</P>
        </fieldset>
     </DIV>



</body>
</html>'''
      else:
          print "<h1>Error! Nombre o contrase&ntilde;a no v&aacute;lida</h1>"

def sesion(asesion): 
      for archi in os.listdir('/var/lib/dnsm/session/'):
           if (os.path.getmtime('/var/lib/dnsm/session/'+archi)) < (time.time()-950.00):
                os.remove('/var/lib/dnsm/session/'+archi)
      if os.path.exists('/var/lib/dnsm/session/'+asesion): 
             os.system('/usr/bin/touch /var/lib/dnsm/session/'+asesion+'>/dev/null')
      else:
           print '''<HTML>
              <HEAD><TITLE>comentario</TITLE></HEAD>
              <BODY>
                <fieldset id="fb" align="center">
                  <input type="hidden" id="colorb" value="#FF0000">
                  <input type="hidden" id="valido" value="false">
                </fieldset>
              </BODY>
           </HTML>'''
      return os.path.exists('/var/lib/dnsm/session/'+asesion)

def main():
     print 'Content-type: text/html\n'	
     form = cgi.FieldStorage()	# parse query
     if form.has_key("session") and sesion(str(form["session"].value)):
         if form.has_key("listar") and form["listar"].value != "":
              listar(str(form['listar'].value))
         elif form.has_key("agregar") and form["agregar"].value != "" and form["ip"].value != "":
              agregar(str(form["agregar"].value),str(form["ip"].value))
         elif form.has_key("eliminar") and form["eliminar"].value != "":
              eliminar(str(form["eliminar"].value))
         elif form.has_key("agregarCNAME") and form["agregarCNAME"].value != "" and form["maquina"].value != "":
              agregarCNAME(form["agregarCNAME"].value,form["maquina"].value)
         elif form.has_key("eliminarCNAME") and form["eliminarCNAME"].value != "":
              eliminarCNAME(str(form["eliminarCNAME"].value))
         elif form.has_key("listardominios"):
              listardominios()
         elif form.has_key("agregarDominio") and form["agregarDominio"].value != "":
              agregarDominio(str(form["agregarDominio"].value))
         elif form.has_key("eliminarDominio") and form["eliminarDominio"].value != "":
              eliminarDominio(str(form["eliminarDominio"].value))
         elif form.has_key("editor") and form["editor"].value != "":
              editor(str(form['editor'].value))
         elif form.has_key("saveedit") and form["saveedit"].value != "":
              saveedit(str(form["saveedit"].value),str(form["contenido"].value))
         elif form.has_key("reiniciarDNS"):
              reiniciarDNS()
         else:
             print "<h1>Parametro no reconocido.</h1>"
     elif form.has_key("verinfo"):
              verinfo()
     else:
          nuevo(str(form["login"].value),str(form["pwd"].value))


     

if __name__ == '__main__':
        main()

