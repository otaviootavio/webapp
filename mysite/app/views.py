import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from datetime import datetime
from django.shortcuts import render, redirect
from app.models import VooBase,VooReal

# Create your views here.

@login_required
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

@login_required
def crud(request):
      return render(request,"CRUD.html")  

def olamundo(request):
    return render(request,"ola-mundo.html")

@login_required
def home(request):
    if request.method == 'POST':
        return render(request,"home.html")
    return render(request,"home.html")

@login_required
def monitoracao(request):
  permissionGroup = ['pilotos','funcionarios','operadores','torres','torres','torres','admin']
  if  request.user.groups.filter(name__in=permissionGroup).exists():
    if request.method == 'POST':
        VooId = request.POST.get('voo_id')
        #if True:
        try:
            voo = VooBase.objects.get(codigo_voo=VooId)
            destino = voo.destino
            origem = voo.origem
            
            vooreal = VooReal.objects.get(voo_base=voo)
            estadoVoo = vooreal.estado_voo
            context = {'voo_id' : VooId, 'destino' : destino, 'origem': origem,
                        'estado_voo' : estadoVoo}
            return render(request,"monitoracao_resultado.html",context)
        except:
            return render(request,"monitoracao.html")
  return render(request,"monitoracao.html")

def monitoracao_update(request):
    if request.method == 'POST':
        return render(request,"monitoracao_resultado.html")
    return render(request,"monitoracao_resultado.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user = user)
            return redirect(home)
        else:
            return render(request, "login.html", {'error_message': 'Ops... usuário ou senha inválido'})
    else:
        return render(request, "login.html")
    
def logout_view(request):
    logout(request)
    return render(request, "login.html")

@login_required
def relatorios(request):
  if request.method == 'POST':
    if request.POST.get('btn_id')=="periodo" and request.POST.get('aeroporto_id') == "Congonhas" and request.POST.get('data_inicial_id') == "2022-10-01" and request.POST.get('data_final_id') == "2022-10-19":
      return render(request,"relatorios-pdf.html")
    elif request.POST.get('btn_id')=="cia" and request.POST.get('cia_id') == "Latam":
      return render(request,"relatorios-pdf.html")
    else:
      return render(request, "relatorios.html")
  else:
    return render(request, "relatorios.html")

def relatoriosPdf(request):
    return render(request, "relatorios-pdf.html")

def relatoriosBase(request):
    return render(request, "relatorios-base.html")