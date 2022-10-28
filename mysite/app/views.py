from datetime import timedelta,datetime
from django.shortcuts import render
from app.models import VooBase

# Create your views here.

globalAccess = ""

def create(request):
    if request.method == 'POST':
        
        data_partida_date = string_to_date(request.POST.get('data-hora-partida'))
        data_chegada_date = string_to_date(request.POST.get('data-hora-chegada'))
        
        novo_voo_base = VooBase.objects.create(
            codigo_voo = request.POST.get('numero-voo'),
            companhia_aerea = request.POST.get('companhia-aerea'),
            dia_da_semana = data_partida_date.weekday(),
            horario_partida_base = data_partida_date.time(),
            duracao_base = (data_chegada_date - data_partida_date).seconds,
            origem = request.POST.get('origem'),
            destino = request.POST.get('destino')
        )
        return render(request,"create.html")
    return render(request,"create.html")

def string_to_date(str_format):
    try:
        date_format = datetime.strptime(str_format, "%Y-%m-%dT%H:%M")
        return date_format
    except:
        return("Error at method string_to_date")
        
def update(request):
    if request.method == 'POST':
        return render(request,"update.html")
    return render(request,"update.html")

def delete(request):
    if request.method == 'POST':
        return render(request,"crud.html")
    return render(request,"crud.html")

def flightData(request):
    if request.method == 'POST':
        return render(request,"crud.html")
    return render(request,"flight-data.html")

def crud(request):
    global globalAccess
    if globalAccess == 'crud' or globalAccess == 'admin':
      return render(request,"CRUD.html")
    else:
      return render(request,"home.html", {'error_message': 'You don\'t have permission to access this resource.'})


def olamundo(request):
    return render(request,"ola-mundo.html")

def home(request):
    if request.method == 'POST':
        return render(request,"home.html")
    return render(request,"home.html")

def monitoracao(request):
  global globalAccess
  if globalAccess == 'moni' or globalAccess == 'admin':
    if request.method == 'POST':
      if request.POST.get('voo_id') == "7":
        return render(request,"monitoracao_resultado.html")
    return render(request,"monitoracao.html")
  else:
    return render(request,"home.html", {'error_message': 'You don\'t have permission to access this resource.'})

def monitoracao_update(request):
    if request.method == 'POST':
        return render(request,"monitoracao_resultado.html")
    return render(request,"monitoracao_resultado.html")

def login(request):
    if request.method == 'POST':
        # Process the request if posted data are available
        username = request.POST['username']
        password = request.POST['password']
        global globalAccess
        globalAccess = username
        # Check username and password combination if correct
        #user = authenticate(username=username, password=password)
        if ((username == 'admin' and password == 'admin') or 
        (username == 'crud' and password == 'crud') or
        (username == 'moni' and password == 'moni') or
        (username == 'rela' and password == 'rela')):
          # Save session as cookie to login the user
          #login(request, user)
          # Success, now let's login the user.
          print(globalAccess)
          return render(request, "home.html")
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, "login.html", {'error_message': 'Incorrect username and / or password.'})
    else:
        # No post data availabe, let's just show the page to the user.
        return render(request, "login.html")

def relatorios(request):
    global globalAccess
    if globalAccess == 'rela' or globalAccess == 'admin':
      if request.method == 'POST':
        if request.POST.get('btn_id')=="periodo" and request.POST.get('aeroporto_id') == "Congonhas" and request.POST.get('data_inicial_id') == "2022-10-01" and request.POST.get('data_final_id') == "2022-10-19":
          return render(request,"relatorios-pdf.html")
        elif request.POST.get('btn_id')=="cia" and request.POST.get('cia_id') == "Latam":
          return render(request,"relatorios-pdf.html")
        else:
          return render(request, "relatorios.html")
      else:
        return render(request, "relatorios.html")
    else:
      return render(request,"home.html", {'error_message': 'You don\'t have permission to access this resource.'})

def relatoriosPdf(request):
    return render(request, "relatorios-pdf.html")