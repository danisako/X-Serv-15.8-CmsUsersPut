from django.shortcuts import render
from django.http import HttpResponse
from .models import Pages
from django.views.decorators.csrf import csrf_exempt



def index(request):
	if request.user.is_authenticated():
		logged = 'Logged in as -->     ' + request.user.username + '<a href="/logout">Logout</a>'
	else:
		logged = 'Not logged in. Para entrar como invitado </br> (user: invitado, password: 1234) </br><a href = "/login">Login</a>'

	respuesta = logged+"<h2>Lista de páginas: </h2></br>"
	paginas = Pages.objects.all()
	
	for p in paginas:
		respuesta += "Nombre de pagina:" + p.name + "</br><li>contenido:" +str(p.page) + "    <li>ID:"+str(p.id)+"</br>"
		respuesta += "<li><a href=cms/" + str(p.id) + ">Enlace a la página de: " + p.name + "</a></li><br>"
		
	return HttpResponse(respuesta)


def muestra(request,idpagina):
	
	try:
		pagina = Pages.objects.get(id = idpagina)
		respuesta = pagina.page
	except Pages.DoesNotExist:
		respuesta = "Error"

	return HttpResponse(respuesta)

def redirect(request):

	resp = "Autenticado como: " +request.user.username +"</br>"
	resp += '<head><meta http-equiv="Refresh" content="5;url='"http://127.0.0.1:8000"'"></head>'" Redirigiendo a la pagina principal " 
	
	return HttpResponse(resp)
	

@csrf_exempt

def new_page(request,name,content):
	if request.method == "GET":
		new_page = Pages(name = name,page = content)
		new_page.save()
	elif request.method == "PUT" or request.method == "POST":
		new_page = Pages(name = name, page = request.body)
		new_page.save()
	return HttpResponse("<h2>Pagina añadida correctamente!</h2>")
