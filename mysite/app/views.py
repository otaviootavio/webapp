from distutils.log import error
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import Http404
from app.models import VooBase, VooReal,ESTADOS_VOO

from app.forms import VooBaseForm, VooRealForm

# Create your views here.

@login_required
def createBase(request):
    if request.method == 'POST':
        forms_voo_base = VooBaseForm(request.POST)
        if forms_voo_base.is_valid():
            forms_voo_base.save()
            return redirect('update-base', pk = request.POST['codigo_voo'])
        return render(request, 'create-base.html', {'forms_voo_base': forms_voo_base})
    else:
        forms_voo_base = VooBaseForm()
    return render(request, 'create-base.html', {'forms_voo_base': forms_voo_base, 'title':"Formulário para creação de voo"})
    
@login_required
def updateBase(request, pk):
    try:
        voo_base_obj = VooBase.objects.get(codigo_voo = pk)
    except VooBase.DoesNotExist:
        raise Http404("No matches to the given query")
    
    forms_voo_base = VooBaseForm(instance = voo_base_obj)
                       
    if request.method == 'POST':
        forms_voo_base = VooBaseForm(request.POST, instance = voo_base_obj)
        if forms_voo_base.is_valid():
            forms_voo_base.save()
            return redirect('home')
    else:
        forms_voo_base = VooBaseForm(instance = voo_base_obj)
    return render(request, 'create-base.html', {'forms_voo_base': forms_voo_base, 'title':"Formulário para atualização de voo"})

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
    all_voo_base = VooBase.objects.all()
    if request.method == 'POST':
        try:
            voo_base_obj = VooBase.objects.get(codigo_voo = request.POST["id-voo"])
            return redirect('monitoração_update', pk = request.POST['id-voo'])
        except Exception as e:
            return render(request, "monitoracao.html", {"error_message": e}) 
    return render(request,"monitoracao.html", context= {'data_voo_base':all_voo_base})

@login_required
def monitoracao_update(request, pk):    
    try:
        voo_real_obj = VooReal.objects.filter(voo_base__codigo_voo = pk).first()
        voo_base_obj = VooBase.objects.filter(codigo_voo = pk).first()
        if voo_real_obj:
            forms_voo_real = VooRealForm(instance = voo_real_obj)
    except (VooReal.DoesNotExist, VooBase.DoesNotExist) as e:
        return render(request, "create-base.html", {"error_message": e}) 

    if request.method == 'POST':
        forms_voo_real = VooRealForm(request.POST, instance = voo_real_obj)
        if forms_voo_real.is_valid():
            forms_voo_real.instance.voo_base = voo_base_obj
            forms_voo_real.save()
            return redirect('home')
    else:
        forms_voo_real = VooRealForm(instance = voo_real_obj)
        
        ## override old format ( YYYY-MM-DD )
        forms_voo_real.initial["data_voo"] = forms_voo_real.instance.data_voo.strftime("%m-%d-%Y")
    return render(request, 'create-real.html', {'forms_voo_real': forms_voo_real, 'title':'Formulário para atualizar status do voo'})

@login_required
def monitoracao_delete(request, pk):    
    try:
        voo_base_obj = VooBase.objects.filter(codigo_voo = pk).first()
        voo_base_obj.delete()
    except (VooBase.DoesNotExist) as e:
        return redirect('monitoração')
    return redirect('monitoração')


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