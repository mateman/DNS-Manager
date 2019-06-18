	
			var http = nuevoAjax();
			var lista = nuevoAjax();
			var dominu = nuevoAjax();
			var elegido =" ";

		
	//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

			function nuevoAjax(){ 
				var xmlhttp=false;
				try{
					xmlhttp=new ActiveXObject("Msxml2.XMLHTTP");
				}catch(e){
					try{
						xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
					}catch(E){
						if (!xmlhttp && typeof XMLHttpRequest!='undefined') xmlhttp=new XMLHttpRequest();
					};
				};
				return xmlhttp; 
			};
			
		
	//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

			function crea_query_string(agr) {
  				return "cuenta=" + encodeURIComponent(agr.value);
			};

		//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

			function MostrarLista(){			
				Espera(true);				
				lista.open("POST","./dnsm.py", true);
				lista.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");				
				lista.send("listardominios= "+"&session="+document.getElementById('sessionval').value);
				lista.onreadystatechange=function() {
				if(lista.readyState == 4) {
					document.getElementById('divlistar').innerHTML = lista.responseText;
					if (document.getElementById('valido').value == 'false') { errorSession();}	
				}
				}		
				Espera(false);				
			}

		//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

			function MostrarDominio(d){			
				if (d!=" "){
					elegido = d;
				    Espera(true);				
					dominu.open("POST","./dnsm.py", true);
				    dominu.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");				
					dominu.send("listar="+ encodeURIComponent(d+".dominio.com.ar")+"&session="+document.getElementById('sessionval').value);
				    dominu.onreadystatechange=function() {
						if(dominu.readyState == 4) {
							document.getElementById('divdominio').innerHTML = dominu.responseText;
							if (document.getElementById('valido').value == 'false') { errorSession();}
						}
					}
			     Espera(false);						
			     }
			}


		//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

			function MostrarEditor(d){			
				Espera(true);
				document.getElementById('cdomi').innerHTML = d;
				document.getElementById('cdomi').value = d;
				http.open("POST","./dnsm.py", true);
				http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");				
				http.send("editor="+ encodeURIComponent(d)+"&session="+document.getElementById('sessionval').value);
				http.onreadystatechange=function() {
				if(http.readyState == 4) {
					CKEDITOR.instances.editor1.setData(http.responseText);
					if (document.getElementById('valido').value == 'false') { errorSession();}	
					else {veredit(true);}
				}
				}
			    Espera(false);						
			}
			

	//------------------------------------------------------------

			function ReiniciarDNS(){
				Espera(true);				
				http.open("POST","./dnsm.py", true);
				http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
				http.send("reiniciarDNS= &session="+document.getElementById('sessionval').value);
				http.onreadystatechange = function(){
								if(http.readyState == 4) {
										document.getElementById('divb').innerHTML = http.responseText;
										if (document.getElementById('valido').value == 'false') { errorSession();}	
										else {recalculando(document.getElementById('divb'));
											  document.getElementById('divb').style.background = document.getElementById('colorb').value;
											  document.getElementById('divb').style.visibility="visible";
											  setTimeout("document.getElementById('divb').style.visibility='hidden';",3000);}
								}
								Espera(false);						
								document.getElementById('divcrearalia').style.visibility= "hidden";

				}
			}

	//------------------------------------------------------------

		//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

			function saveedit(){			
				Espera(true);				
				http.open("POST","./dnsm.py", true);
				http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");				
				http.send("saveedit="+ encodeURIComponent(document.getElementById('cdomi').value)+"&contenido="+encodeURIComponent(CKEDITOR.instances.editor1.getData())+"&session="+document.getElementById('sessionval').value);
				http.onreadystatechange=function() {
				   if (document.getElementById('valido').value == 'false') { errorSession();}	
				}
			    Espera(false);						
			}


	//------------------------------------------------------------
	
			function agregar(){
				Espera(true);				
				http.open("POST","./dnsm.py", true);
				http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");	
				http.send("agregar="+encodeURIComponent((document.getElementById('maquinaagregar').value))+"&ip="+encodeURIComponent((document.getElementById('ipagregar').value))+"&session="+document.getElementById('sessionval').value);
				http.onreadystatechange = function(){
					if(http.readyState == 4) {
						document.getElementById('divb').innerHTML = http.responseText;
						if (document.getElementById('valido').value == 'false') { errorSession();}	
						else { recalculando(document.getElementById('divb'));
							   document.getElementById('divb').style.background = document.getElementById('colorb').value;
							   document.getElementById('divb').style.visibility="visible";
							   setTimeout("document.getElementById('divb').style.visibility='hidden';",3000);}
						}
					Espera(false);						
					document.getElementById('divcrear').style.visibility= "hidden";
					MostrarLista();
					MostrarDominio(elegido);
				}
			}
			

	//------------------------------------------------------------

			function agregarDominio(){
				Espera(true);				
				http.open("POST","./dnsm.py", true);
				http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
				http.send("agregarDominio="+encodeURIComponent(document.getElementById('agregarzona').value)+"&session="+document.getElementById('sessionval').value);
				http.onreadystatechange = function(){
								if(http.readyState == 4) {
										document.getElementById('divb').innerHTML = http.responseText;
										if (document.getElementById('valido').value == 'false') { errorSession();}	
										else {recalculando(document.getElementById('divb'));
											  document.getElementById('divb').style.background = document.getElementById('colorb').value;
											  document.getElementById('divb').style.visibility="visible";
											  setTimeout("document.getElementById('divb').style.visibility='hidden';",3000);}
								}
								Espera(false);
								document.getElementById('divzona').style.visibility= "hidden";
								MostrarLista();
				}
			}

	//------------------------------------------------------------

			function agregarCNAME(){
				Espera(true);				
				http.open("POST","./dnsm.py", true);
				http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
				http.send("agregarCNAME="+encodeURIComponent(document.getElementById('alias').value) +"&maquina="+encodeURIComponent(document.getElementById('maquinaalias').value)+"&session="+document.getElementById('sessionval').value);
				http.onreadystatechange = function(){
								if(http.readyState == 4) {
										document.getElementById('divb').innerHTML = http.responseText;
										if (document.getElementById('valido').value == 'false') { errorSession();}	
										else { recalculando(document.getElementById('divb'));
											   document.getElementById('divb').style.background = document.getElementById('colorb').value;
											   document.getElementById('divb').style.visibility="visible";
											   setTimeout("document.getElementById('divb').style.visibility='hidden';",3000);}
								}
								Espera(false);						
								document.getElementById('divcrearalia').style.visibility= "hidden";
								MostrarLista();
								MostrarDominio(elegido);
				}
			}

	//------------------------------------------------------------


			function BorrarDominio(a){
				if (confirm("Est&aacute; seguro que desea borrar este dominio?")){
				Espera(true);				
				http.open("POST","./dnsm.py", true);
				http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
				http.send("eliminar="+encodeURIComponent(a)+"&session="+document.getElementById('sessionval').value);}
				http.onreadystatechange = function(){
						if(http.readyState == 4) {
								document.getElementById('divb').innerHTML = http.responseText;
								if (document.getElementById('valido').value == 'false') { errorSession();}	
								else {recalculando(document.getElementById('divb'));
									  document.getElementById('divb').style.background = document.getElementById('colorb').value;
									  document.getElementById('divb').style.visibility="visible";
									  setTimeout("document.getElementById('divb').style.visibility='hidden';",3000);}
						}
						Espera(false);
						MostrarDominio(elegido);
				}
			}
			
	//------------------------------------------------------------


			function BorrarCNAME(a){
				if (confirm("Est&aacute; seguro que desea borrar este alias?")){
					Espera(true);				
					http.open("POST","./dnsm.py", true);
					http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
					http.send("eliminarCNAME="+encodeURIComponent(a)+"&session="+document.getElementById('sessionval').value);}
					http.onreadystatechange = function(){
							if(http.readyState == 4) {
								document.getElementById('divb').innerHTML = http.responseText;
								if (document.getElementById('valido').value == 'false') { errorSession();}	
								else {recalculando(document.getElementById('divb'));
									  document.getElementById('divb').style.background = document.getElementById('colorb').value;
									  document.getElementById('divb').style.visibility="visible";
									  setTimeout("document.getElementById('divb').style.visibility='hidden';",3000);}
							}
							Espera(false);
							MostrarDominio(elegido);
					}
			}
			


	//------------------------------------------------------------


			function EliminarZona(a){
				if (confirm("Est&aacute; seguro que desea borrar esta zona?")){
					Espera(true);
					http.open("POST","./dnsm.py", true);
					http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
					http.send("eliminarDominio="+encodeURIComponent(a)+"&session="+document.getElementById('sessionval').value);}
					http.onreadystatechange = function(){
								if(http.readyState == 4) {
										document.getElementById('divb').innerHTML = http.responseText;
										if (document.getElementById('valido').value == 'false') { errorSession();}	
										else {recalculando(document.getElementById('divb'));
											  document.getElementById('divb').style.background = document.getElementById('colorb').value;
											  document.getElementById('divb').style.visibility="visible";
											  setTimeout("document.getElementById('divb').style.visibility='hidden';",3000);}
								}
								Espera(false);
								MostrarLista();
								elegido = " ";
								document.getElementById('divdominio').innerHTML = " <fieldset id='fdominio'></fieldset> ";
					}
			}

	//------------------------------------------------------------

			function Espera(activo){
				
				if (activo==true){					
					document.getElementById('espera').style.visibility= "visible";
				}else{
					document.getElementById('espera').style.visibility= "hidden";
				}				
			}
			
			
	//------------------------------------------------------------

			function veredit(activo){
				
				if (activo==true){
					recalculando(document.getElementById('divedit'));
					document.getElementById('divedit').style.visibility= "visible";
				}else{
					document.getElementById('divedit').style.visibility= "hidden";
				}				
			}
			
			
	//------------------------------------------------------------
			function recalculando(d){
					d.style.position='fixed'; 
					d.style.left=(document.body.offsetWidth/2-((parseInt(d.style.width))/2))+'px';
					d.style.top=(document.body.offsetHeight/2-((parseInt(d.style.height))/2))+'px';					
			}
	
	//------------------------------------------------------------


			function verinfo(){
				var nw = window.open('../verinfo.html',"Delegaciones Total","scrollbars=YES, menubar=NO, location=NO, toolbars=No, status=NO")						

			}


	//------------------------------------------------------------
			function verificaIp(crea){
				if (!(/(^\d+\.\d+\.\d+\.\d+)$/).test(crea.value)||((/(^\s+|^)$/).test(crea.value)))
	              {
	                  alert('El valor ingreasdo debe ser un n&uacute;mero v&aacute;lido');	
	                  crea.value='';
	                  crea.focus();
	              }
	            return false;
			}

	//------------------------------------------------------------
			function verifica_agregar(crea){
				var maq_error = /(^([0-9a-z]|\-)+|^)$/;
				var dom_error = /(^([0-9a-z]|\.|\-)+(.servidor|.mail1).dominio.com.ar)$/;
				if (!dom_error.test(crea.value)) {
					if (maq_error.test(crea.value) && elegido!=" "){ crea.value = crea.value+'.'+elegido+'.dominio.com.ar'}
					else {alert('error valor no aceptado'); //Colocamos el cursor en ese campo	  
					      crea.focus(); //Colocamos el cursor en ese campo
					      crea.value=''; //Borramos el error
					}
					}
					return false;
			}
			//------------------------------------------------------------
			//Funcion de Error por session
			function errorSession(){
				recalculando(document.getElementById('divsession'));
				document.bgcolor='#808080';
				document.getElementById('divform').style.visibility= "hidden";
				document.getElementById('divlistar').style.visibility= "hidden";
				document.getElementById('divdominio').style.visibility= "hidden";
				document.getElementById('divedit').style.visibility= "hidden";
				document.getElementById('divzona').style.visibility= "hidden";
				document.getElementById('divcrear').style.visibility= "hidden";
				document.getElementById('divcrearalia').style.visibility= "hidden";
				document.getElementById('divb').style.visibility= "hidden";
				document.getElementById('divsession').style.visibility= "visible";
				setTimeout("window.location='../login.html'",7000);
			}

			//------------------------------------------------------------
			//Salir del sistema 
			function Salir() { 
				window.location='index.cgi';
				cerrar_ajax();
			}
	



