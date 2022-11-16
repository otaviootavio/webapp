from distutils.log import error
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.shortcuts import render, redirect
from app.models import VooBase, VooReal,ESTADOS_VOO
from django.http import Http404

from app.forms import VooBaseForm

# Create your views here.

@login_required
def createBase(request):
    if request.method == 'POST':
        form = VooBaseForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'create-base.html', {'form': form})
    else:
        form = VooBaseForm()
    return render(request, 'create-base.html', {'form': form})
    
@login_required
def updateBase(request, pk):
    try:
        voo_base_obj = VooBase.objects.get(codigo_voo = pk)
    except VooBase.DoesNotExist:
        raise Http404("No MyModel matches the given query")
    
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
    if request.method == 'POST' and request.POST['id-voo'] is not None:
        try:
            voo_base_obj = VooBase.objects.get(codigo_voo = request.POST["id-voo"])
            return redirect('update-base', pk = request.POST['id-voo'])
        except Exception as e:
            return render(request, "CRUD.html", {"error_message": e}) 
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
        VooId = request.POST["voo_id"]
        if True:
        #try:
            voo = VooBase.objects.get(codigo_voo = VooId)
            destino = voo.destino
            origem = voo.origem
            
            vooreal = VooReal.objects.get(voo_base=voo)
            estadoVoo = vooreal.get_estado_voo_display 
            context = {'voo_id' : VooId, 'destino' : destino, 'origem': origem,
                        'estado_voo' : estadoVoo, 'estados_voo_possiveis': ESTADOS_VOO}
            return render(request,"monitoracao_resultado.html",context)
        #except:
            return render(request,"monitoracao.html")
  return render(request,"monitoracao.html")

def monitoracao_update(request,vooBase):
    permissionGroup = ['pilotos','funcionarios','operadores','torres','torres','torres','admin']
    if  request.user.groups.filter(name__in=permissionGroup).exists():
        if request.method == 'POST':
            estado = request.POST["novo_estado"]
            voo = VooBase.objects.get(codigo_voo = vooBase)

            vooreal = VooReal.objects.get(voo_base=voo)
            vooreal.estado_voo = estado
            vooreal.save()

            context = {'voo_id' : voo.codigo_voo, 'destino' : voo.destino, 'origem': voo.origem,
                        'estado_voo' : vooreal.get_estado_voo_display , 'estados_voo_possiveis': ESTADOS_VOO}
            return render(request,"monitoracao_resultado.html", context)
    return render(request,"monitoracao_resultado.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        ## Define o numero de tentativas
        num_max = 3
        
        if "load_count" in request.session:
            count = request.session["load_count"]
        else:
            count = 0
            request.session["load_count"] = 0
        
        if count > num_max:
            return render(request, "login.html", {'error_message': 'Número de tentativas excedido'})
            
        if user is not None:
            if count <= num_max:
                request.session["load_count"] = 0
                request.session.save()
                login(request, user = user)
                return redirect(home)
        else:
            request.session["load_count"] = request.session["load_count"] + 1
            return render(request, "login.html", {'error_message': 'Ops... usuário ou senha inválido' })
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