from distutils.log import error

# report generating
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
####

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
            return redirect('crud')
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
            return redirect('crud')
    else:
        forms_voo_base = VooBaseForm(instance = voo_base_obj)
    return render(request, 'create-base.html', {'forms_voo_base': forms_voo_base, 'title':"Formulário para atualização de voo"})

@login_required
def deleteBase(request, pk):    
    try:
        voo_base_obj = VooBase.objects.filter(codigo_voo = pk).first()
        voo_base_obj.delete()
    except (VooBase.DoesNotExist) as e:
        return redirect('crud')
    return redirect('crud')

def string_to_date(str_format):
    try:
        date_format = datetime.strptime(str_format, "%Y-%m-%d")
        return date_format
    except:
        return("Error at method string_to_date")

def flightData(request):
    if request.method == 'POST':
        return render(request,"crud.html")
    return render(request,"flight-data.html")

@login_required
def crud(request):
    all_voo_base = VooBase.objects.all()
    if request.method == 'POST' and request.POST['id-voo'] is not '':
        try:
            filtered_voo_base = VooBase.objects.all().filter(codigo_voo = request.POST["id-voo"])
            return render(request,"CRUD.html", context= {'dados_voo_base':filtered_voo_base})
        except Exception as e:
            return render(request, "CRUD.html", {"error_message": e, 'dados_voo_base':all_voo_base}) 
    return render(request,"CRUD.html", context= {'dados_voo_base':all_voo_base})

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
        if forms_voo_real.instance.data_voo:
            forms_voo_real.initial["data_voo"] = forms_voo_real.instance.data_voo.strftime("%d-%m-%Y")
    return render(request, 'create-real.html', {'forms_voo_real': forms_voo_real, 'title':'Formulário para atualizar status do voo'})

@login_required
def monitoracao_delete(request, pk):    
    try:
        voo_base_obj = VooBase.objects.filter(codigo_voo = pk).first()
        voo_base_obj.delete()
    except (VooBase.DoesNotExist) as e:
        return redirect('monitoração')
    return redirect('monitoração')

def generate_report_airline(request, pk):
     # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    line_break = 20
    top_page = 700
    margin_col = 90
    margin_sides = 20
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    report_voo = VooBase.objects.all().filter(companhia_aerea = pk)
    x = top_page
    for voo in report_voo:
        p.drawString(margin_sides, x, voo.codigo_voo)
        p.drawString(margin_sides + 1*margin_col, x, voo.companhia_aerea)
        p.drawString(margin_sides + 2*margin_col, x, voo.dia_da_semana)
        p.drawString(margin_sides + 3*margin_col, x, voo.horario_partida_base.strftime("%H:%M:%S"))
        p.drawString(margin_sides + 4*margin_col, x, voo.duracao_base.strftime("%H:%M:%S"))
        p.drawString(margin_sides + 5*margin_col, x, voo.origem)
        p.drawString(margin_sides + 6*margin_col, x, voo.destino)
        x = x - line_break

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='report_by_airport.pdf')

def generate_report_data(request, start_date, end_date):
     # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    line_break = 20
    top_page = 700
    margin_col = 90
    margin_sides = 20
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    report_voo = VooReal.objects.all().filter( data_voo__range =[start_date, end_date])
    x = top_page
    for voo in report_voo:
        p.drawString(margin_sides, x, voo.voo_base.codigo_voo)
        p.drawString(margin_sides + 1*margin_col, x, voo.voo_base.companhia_aerea)
        p.drawString(margin_sides + 2*margin_col, x, voo.voo_base.dia_da_semana)
        p.drawString(margin_sides + 3*margin_col, x, voo.voo_base.horario_partida_base.strftime("%H:%M:%S"))
        p.drawString(margin_sides + 4*margin_col, x, voo.voo_base.duracao_base.strftime("%H:%M:%S"))
        x = x - line_break
        p.drawString(margin_sides + 1*margin_col, x, voo.voo_base.origem)
        p.drawString(margin_sides + 2*margin_col, x, voo.voo_base.destino)
        p.drawString(margin_sides + 3*margin_col, x, voo.data_voo.strftime("%m/%d/%Y"))
        p.drawString(margin_sides + 4*margin_col, x, voo.estado_voo)
        x = x - line_break
        p.drawString(margin_sides + 1*margin_col, x, voo.horario_real_chegada.strftime("%H:%M:%S"))
        p.drawString(margin_sides + 2*margin_col, x, voo.horario_real_partida.strftime("%H:%M:%S"))
        x = x - line_break

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='report_by_time.pdf')

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
    if request.POST.get('cia_id'):
        return generate_report_airline(request, request.POST.get('cia_id'))
    elif request.POST.get('aeroporto_id'):
        ## data_inicial = string_to_date(request.POST.get('data_inicial_id'))
        ## data_final = string_to_date(request.POST.get('data_final_id'))
        data_inicial = request.POST.get('data_inicial_id')
        data_final = request.POST.get('data_final_id')
        return generate_report_data(request, data_inicial, data_final)
    else:
        return generate_report_airline(request, 10)
  else:
    return render(request, "relatorios.html")

def relatoriosPdf(request):
    return render(request, "relatorios-pdf.html")

def relatoriosBase(request):
    return render(request, "relatorios-base.html")