#!/usr/bin/perl
#
# Hecho por Pablo Adolfo Cuyeu (cuyeu@hotmail.com)
#

use IO::Socket;

sub metodo_forma {
						my($metodo)=$ENV{'REQUEST_METHOD'};
						my($entrada);
						#Validamos primero el tipo de codificacion
						if (($ENV{'CONTENT_TYPE'} !~ /^application\/x-www-form-urlencoded/i) && ($ENV{'CONTENT_TYPE'} ne '')) 
									{
										print("Content-type: text/html\r\n\r\n");
										print("<html><head><title>Error en CGI</title></head>\n");
										print("<body bgcolor=#FFFFFF>\n");
										print("<H1>Error: Codificacion desconocida\n</H1>");
										print("<H2>Soporta: application\/x-www-form-urlencoded\n</H2>");
										print("</body></html>\n");
										exit;
									}
						$metodo =~ tr/A-Z/a-z/; #Convierta la respuesta a minusculas
						#El metodo es POST y tiene longitud > 0
						if (($metodo eq "post") && ($ENV{'CONTENT_LENGTH'} > 0)) 
									{
										read(STDIN,$entrada,$ENV{'CONTENT_LENGTH'});
										return($entrada);
									} else { #Metodo desconocido o valor nulo
												print("Content-type: text/html\r\n\r\n");
												print("<html><head><title>Error en CGI</title></head>\n");
												print("<body bgcolor=#FFFFFF>\n");
												print("<H1>Error: Metodo desconocido o valor nulo\n</H1>");
												print("<H2>Soporta: Method=POST\n</H2>");
												print("</body></html>\n");
												exit;
											}
			} #Fin metodo_forma()

# La siguiente rutina decodifica la entrada y la guarda en
# un arreglo asociativo
sub decodificar_forma($) {
					my($BUENOS_CARACTERES)='-a-zA-Z0-9_.@ '; #Caracteres validos en los datos
					my($entrada)=@_;
					my(%pares,$clave,$valor);
					$entrada =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("c",hex($1))/ge; #Convierto a alfanumerico los caracteres en hexadecimal
					@pares=split('&',$entrada); #Separo cada par y lo guardo en un arreglo
					foreach $par (@pares) { # proceso cada par en pares
								($clave,$valor)=split(/=/,$par); #Guarde clave,valor usando la busqueda anterior
								$valor =~ s/\+/ /g; #Cambie + por espacio en toda la cadena
								# Seguridad  en caracteres,segun aviso del Cern en
								# http://geek-girl.com/bugtraq/1997_4/0232.html
								$clave =~ s/[^$BUENOS_CARACTERES]/_/go;
								$valor =~ s/[^$BUENOS_CARACTERES]/_/go;
								#Finalmente construya el arreglo asociativo
								$pares{$clave}=$valor;
												}
					return(%pares);
									} # Fin Decodificar_forma()
	

# Comienzo del programa principal
$entrada=&metodo_forma();
%datos=&decodificar_forma($entrada);
my $server = $datos{'server'};
$| = 1; #Vaciamos el buffer de escritura lo mas rapido posible<h2></h2>
print("Content-type: text/html\r\n\r\n");	
print('<html>');
print('<head><title>Listar cuentas</title></head>');
print('<body>');
print('<input type="hidden" id="valido" value="true">');
print('<fieldset id="fmail">');
print('<legend>Cuentas de correo</legend><BR>');
print('<table border=2 >');		
$sock = new IO::Socket::INET (PeerAddr => $server,
                              PeerPort => 1234,
                              Proto    => 'tcp') or die "Error creating socket: $!\n";

recv($sock, $pregunta, 30,undef);
print $sock "listar.pl";
while(<$sock>) {
        ($cuenta,$nombre,$sector,$tel)=split(/\,/,$_);
        print ('<TR><TH>'.$cuenta.'</TH><TD>'.$nombre.'</TD><TD>'.$sector.'</TD><TD>'.$tel.'</TD></TR>');
   }		
close $sock;
print('</table>');
print('</fieldset>');
print('</form>');
print('</body>');
print('</html>');



