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
				lista.open("POST","/cgi-bin/dnsview.py", true);
				lista.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");				
				lista.send("listardominios= ");
				lista.onreadystatechange=function() {
				if(lista.readyState == 4) {
					document.getElementById('divlistar').innerHTML = lista.responseText;
				}
				}		
				Espera(false);				
			}

		//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

			function MostrarDominio(d){			
				if (d!=" "){
					elegido = d;
				    Espera(true);				
					dominu.open("POST","./cgi-bin/dnsview.py", true);
				    dominu.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");				
					dominu.send("listar="+ encodeURIComponent(d+".dominio.com.ar"));
				    dominu.onreadystatechange=function() {
						if(dominu.readyState == 4) {
							document.getElementById('divdominio').innerHTML = dominu.responseText;
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
				http.open("POST","./cgi-bin/dnsview.py", true);
				http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");				
				http.send("editor="+ encodeURIComponent(d));
				http.onreadystatechange=function() {
				if(http.readyState == 4) {
					veredit('divedit',true);
					CKEDITOR.instances.editor1.setData(http.responseText);
				}
				}
			    Espera(false);						
			}
			

		//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

			function MostrarTelefono(){			
				Espera(true);
				http.open("POST","./cgi-bin/dnsview.py", true);
				http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");				
				http.send("verdoc= ");
				http.onreadystatechange=function() {
				if(http.readyState == 4) {
					veredit('divdoc',true);
					CKEDITOR.instances.editor2.setData(http.responseText);
				}
				}
			    Espera(false);						
			}
			


		//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

			function MostrarPlanilla(){			
				Espera(true);
				http.open("POST","./cgi-bin/dnsview.py", true);
				http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");				
				http.send("verplani= ");
				http.onreadystatechange=function() {
				if(http.readyState == 4) {
					veredit('divplani',true);
					CKEDITOR.instances.editor3.setData(http.responseText);
				}
				}
			    Espera(false);						
			}
			

		//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

			function MostrarMail(d){			
				Espera(true);
				http.open("POST","./cgi-bin/listar.pl", true);
				http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");				
				http.send("server="+d);
				http.onreadystatechange=function() {
				if(http.readyState == 4) {
					focoMail(true);
					document.getElementById('divmail').innerHTML = http.responseText;
				}
				}
			    Espera(false);						
			}
			

		//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

			function savedoc(){			
				Espera(true);				
				http.open("POST","./cgi-bin/dnsview.py", true);
				http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");				
				http.send("savedoc="+encodeURIComponent(CKEDITOR.instances.editor2.getData()));
				http.onreadystatechange=function() {
				}
			    Espera(false);						
			}


		//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

			function saveplani(){			
				Espera(true);				
				http.open("POST","./cgi-bin/dnsview.py", true);
				http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");				
				http.send("saveplani="+encodeURIComponent(CKEDITOR.instances.editor3.getData()));
				http.onreadystatechange=function() {
				}
			    Espera(false);						
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
				function focoMail(activo){
				
				if (activo==true){					
					document.getElementById('divdominio').style.visibility= "hidden";
					document.getElementById('divlistar').style.visibility= "hidden";
					document.getElementById('divmail').style.visibility= "visible";
				}else{
					document.getElementById('divmail').style.visibility= "hidden";
					document.getElementById('divdominio').style.visibility= "visible";
					document.getElementById('divlistar').style.visibility= "visible";
				}				
			}
			
					
	//------------------------------------------------------------

			function veredit(quien,activo){
				
				if (activo==true){
					recalculando(document.getElementById(quien));
					document.getElementById(quien).style.visibility= "visible";
				}else{
					document.getElementById(quien).style.visibility= "hidden";
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
				var nw = window.open('/verinfo.html',"Delegaciones Total","scrollbars=YES, menubar=NO, location=NO, toolbars=No, status=NO")						

			}
