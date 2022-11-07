import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from datetime import datetime
from django.shortcuts import render, redirect
from app.models import VooBase
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404

from app.forms import VooBaseForm

# Create your views here.

# @login_required
# def createBase(request):
#     if request.method == 'POST':
        
#         horario_partida_array = request.POST.get('duracao').split(":")
#         horario_partida_sec_int = int(horario_partida_array[0])*3600 + int(horario_partida_array[1])*60
       
#         duracao_array = request.POST.get('duracao').split(":")
#         duracao_sec_int = int(duracao_array[0])*3600 + int(duracao_array[1])*60
        
#         novo_voo_base = VooBase.objects.create(
#             codigo_voo = request.POST.get('codigo-voo'),
#             companhia_aerea = request.POST.get('companhia-aerea'),
#             dia_da_semana = request.POST.get('dia-da-semana')[:3].upper(),
#             horario_partida_base = horario_partida_sec_int,
#             duracao_base = duracao_sec_int,
#             origem = request.POST.get('origem'),
#             destino = request.POST.get('destino')
#         )
#         return render(request,"create-base.html")
#     return render(request,"create-base.html")

@login_required
def createBase(request):

    if request.method == 'POST':
        form = VooBaseForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = VooBaseForm()
    return render(request, 'create-base.html', {'form': form})

@login_required
def updateBase(request, pk):
    voo_base_obj = get_object_or_404(VooBase, codigo_voo = pk)
    form = VooBaseForm(instance = voo_base_obj)
                       
    if request.method == 'POST':
        form = VooBaseForm(request.POST, instance = voo_base_obj)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = VooBaseForm(instance = voo_base_obj)
    return render(request, 'create-base.html', {'form': form})

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