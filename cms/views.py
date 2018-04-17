from django.shortcuts import render
from django.http import HttpResponse
from .models import Pages
from django.views.decorators.csrf import csrf_exempt


formulario = """
<form action = "" method ="POST">
	Nombre: <input type="text" name="nombre" value=""><br>
    Pagina: <input type="text" name="page" value=""><br>
    <input type="submit" value="Enviar">
    </form>
"""

@csrf_exempt
def index(request):
	if request.user.is_authenticated():
		logged = 'Logged in as -->     ' + request.user.username + '<a href="/logout">Logout</a></br></br>'
		logged += formulario
		if request.method == "POST":
			pagina = Pages(name = request.POST['nombre'], page = request.POST['page'])
			pagina.save()
	else:
		logged = 'Not logged in. Entra para poder añadir páginas </br><a href = "/login">Login</a>'

	respuesta = 'Para acceder a la configuración: <a href = "/admin">Configuracion</a></br></br>'
	respuesta += logged+"<h2>Lista de páginas: </h2></br>"
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
	



def new_page(request,name,content):
	if request.method == "GET":
		new_page = Pages(name = name,page = content)
		new_page.save()
	elif request.method == "PUT" or request.method == "POST":
		new_page = Pages(name = name, page = request.body)
		new_page.save()
	return HttpResponse("<h2>Pagina añadida correctamente!</h2>")
