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
from app.models import VooBase, VooReal, ESTADOS_VOO, Group
from app.forms import VooBaseForm, VooRealForm
from app.decorators import check_user_able_to_see_page
from django.db.models import Avg, FloatField,Sum,Count,F

# Messaging
from django.contrib import messages
###

# Create your views here.


@check_user_able_to_see_page(Group.operadores)
def createBase(request):
    if request.method == "POST":
        forms_voo_base = VooBaseForm(request.POST)
        if forms_voo_base.is_valid():
            voo_base_obj = forms_voo_base.save()
            
            forms_voo_real = VooRealForm()
            voo_real_temp = forms_voo_real.save(commit=False)
            voo_real_temp.voo_base =  voo_base_obj
            voo_real_temp.save()
            
            messages.add_message(request, messages.SUCCESS, 'Voo criado com sucesso')
            return redirect("crud")
        return render(request, "create-base.html", {"forms_voo_base": forms_voo_base})
    else:
        forms_voo_base = VooBaseForm()
    return render(
        request,
        "create-base.html",
        {"forms_voo_base": forms_voo_base, "title": "Formulário para criação de voo"},
    )


@check_user_able_to_see_page(Group.operadores)
def updateBase(request, pk):
    try:
        voo_base_obj = VooBase.objects.get(id=pk)
    except VooBase.DoesNotExist:
        raise Http404("No matches to the given query")

    forms_voo_base = VooBaseForm(instance=voo_base_obj)

    if request.method == "POST":
        forms_voo_base = VooBaseForm(request.POST, instance=voo_base_obj)
        #Workaround to show the forms disabled AND the correct value at form
        forms_voo_base.data._mutable = True
        forms_voo_base.data["codigo_voo"] = voo_base_obj.codigo_voo
        forms_voo_base.data["companhia_aerea"] = voo_base_obj.companhia_aerea
        forms_voo_base.data._mutable = False

        if forms_voo_base.is_valid():
            forms_voo_base.save()
            messages.add_message(request, messages.SUCCESS, 'Voo editado com sucesso')
            return redirect("crud")
    else:
        forms_voo_base = VooBaseForm(instance=voo_base_obj)
        forms_voo_base.fields["codigo_voo"].disabled = True
        forms_voo_base.fields["companhia_aerea"].disabled = True
    return render(
        request,
        "create-base.html",
        {
            "forms_voo_base": forms_voo_base,
            "title": "Formulário para atualização de voo",
        },
    )

@check_user_able_to_see_page(Group.operadores)
def deleteBase(request, pk):
    try:
        voo_base_obj = VooBase.objects.filter(id=pk)
        voo_base_obj.delete()
        messages.add_message(request, messages.SUCCESS, 'Voo deletado com sucesso')
    except (VooBase.DoesNotExist) as e:
        return redirect("crud")
    return redirect("crud")

@check_user_able_to_see_page(Group.operadores)
def crud(request):
    all_voo_base = VooBase.objects.all()
    user = request.user

    if (
        request.method == "POST"
        and request.POST["id-voo"] != ""
        and request.POST["id-voo"] != None
    ):
        try:
            filtered_voo_base = VooBase.objects.all().filter(
                codigo_voo=request.POST["id-voo"]
            )
            return render(
                request, "CRUD.html", context={"dados_voo_base": filtered_voo_base}
            )
        except Exception as e:
            messages.warning(request, e)
            return render(
                request,
                "CRUD.html",
                {"dados_voo_base": all_voo_base},
            )
    return render(request, "CRUD.html", context={"dados_voo_base": all_voo_base})

def home(request):
    obj_voo_real_origem = VooReal.objects.all().filter(voo_base__origem="SP")
    obj_voo_real_chegada = VooReal.objects.all().filter(voo_base__destino="SP")
    if request.method == "POST":
        return render(request, "home.html")
    return render(
        request,
        "home.html",
        {
            "dados_voo_real_origem": obj_voo_real_origem,
            "dados_voo_real_chegada": obj_voo_real_chegada,
        },
    )


@check_user_able_to_see_page(Group.torres, Group.funcionarios, Group.pilotos)
def monitoracao(request):
    obj_voo_real_origem = VooReal.objects.all().filter(voo_base__origem="SP")
    obj_voo_real_chegada = VooReal.objects.all().filter(voo_base__destino="SP")
    if request.method == "POST":
        try:
            voo_base_obj = VooBase.objects.get(codigo_voo=request.POST["id-voo"])
            return redirect("monitoração_update", pk=request.POST["id-voo"])
        except Exception as e:
            messages.warning(request, e)
            return render(request, "monitoracao.html")
    return render(request, "monitoracao.html",
                  context={
                      "dados_voo_real_origem": obj_voo_real_origem,
                      "dados_voo_real_chegada": obj_voo_real_chegada,
                  })




@check_user_able_to_see_page(Group.torres, Group.funcionarios, Group.pilotos)
def monitoracao_update(request, pk):
    try:
        voo_real_obj = VooReal.objects.filter(id=pk).first()
        voo_base_obj = VooBase.objects.filter( id = voo_real_obj.voo_base.id).first()
        if voo_real_obj:
            forms_voo_real = VooRealForm(instance=voo_real_obj)
    except (VooReal.DoesNotExist, VooBase.DoesNotExist) as e:
        messages.warning(request, e)
        return render(request, "create-base.html")

    if request.method == "POST":
        forms_voo_real = VooRealForm(request.POST, instance=voo_real_obj)
        
        #Workaround to send correct data to database
        ## if forms_voo_real.instance.data_voo:
        ##     forms_voo_real.data._mutable = True
        ##     forms_voo_real.data["data_voo"] = voo_real_obj.data_voo.strftime("%d-%m-%Y")
        ##     forms_voo_real.fields["data_voo"].disabled = True
        ##     forms_voo_real.data._mutable = False
                
        if forms_voo_real.is_valid():
            forms_voo_real.instance.voo_base = voo_base_obj
            forms_voo_real.save()
            messages.add_message(request, messages.SUCCESS, 'Voo atualizado com sucesso')
            return redirect("monitoração")
    else:
        forms_voo_real = VooRealForm(instance=voo_real_obj)

        ## override old format ( YYYY-MM-DD ) and disable Date input
        ## if forms_voo_real.instance.data_voo:
        ##     forms_voo_real.initial["data_voo"] = forms_voo_real.instance.data_voo.strftime("%d-%m-%Y")
        ##     forms_voo_real.fields["data_voo"].disabled = True
        
    return render(
        request,
        "update-real.html",
        {
            "forms_voo_real": forms_voo_real,
            "title": "Formulário para atualizar status do voo",
        },
    )


@check_user_able_to_see_page(Group.torres, Group.funcionarios, Group.pilotos)
def monitoracao_delete(request, pk):
    try:
        voo_real_obj = VooReal.objects.filter(id=pk).first()
        voo_real_obj.delete()
        messages.add_message(request, messages.SUCCESS, 'Voo deletado com sucesso')
    except (VooBase.DoesNotExist) as e:
        return redirect("monitoração")
    return redirect("monitoração")

@check_user_able_to_see_page(Group.gerentes)
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
    report_voo = VooReal.objects.all().filter(voo_base__companhia_aerea=pk)
    
    if not report_voo:
        messages.warning(request, 'Não há voos para serem mostrados no relatorio')
        return render(request, "relatorios.html")
        
    x = top_page

    p.drawString(margin_sides, x, "Total de voos:")
    p.drawString(margin_sides + 1 * margin_col, x, "Total voos cancelados:")
    p.drawString(margin_sides + 3 * margin_col, x, "Duração média dos voos:")
    
    x = x - line_break

    p.drawString(margin_sides, x, str(report_voo.count()))
    p.drawString(margin_sides + 1 * margin_col, x, str(report_voo.filter(estado_voo='CAN').count()))
    
    a = VooReal.objects.aggregate(price_diff=Avg(F('horario_real_chegada') - F('horario_real_partida')))['price_diff']
    p.drawString(margin_sides + 3 * margin_col, x, str(a))

    x = x - 2*line_break
    for voo in report_voo:
        
        horario_partida_base_str = voo.voo_base.horario_partida_base.strftime("%H:%M:%S") if voo.voo_base.horario_partida_base else '---'
        data_voo_str = voo.voo_base.data_voo.strftime("%d/%m/%Y") if voo.voo_base.data_voo else '---'
        horario_real_partida_str = voo.horario_real_partida.strftime("%H:%M:%S") if voo.horario_real_partida else '---'
        horario_real_chegada_str = voo.horario_real_chegada.strftime("%H:%M:%S") if voo.horario_real_chegada else '---'
        duracao_base_srt = voo.voo_base.duracao_base.strftime("%H:%M:%S") if voo.voo_base.duracao_base else '---'
        
        p.drawString(margin_sides, x, voo.voo_base.codigo_voo)
        p.drawString(margin_sides + 1 * margin_col, x, voo.voo_base.companhia_aerea)
        p.drawString(margin_sides + 2 * margin_col, x, voo.voo_base.dia_da_semana)
        p.drawString(
            margin_sides + 3 * margin_col,
            x,
            horario_partida_base_str,
        )
        p.drawString(
            margin_sides + 4 * margin_col,
            x,
            duracao_base_srt,
        )
        x = x - line_break
        p.drawString(margin_sides + 1 * margin_col, x, voo.voo_base.origem)
        p.drawString(margin_sides + 2 * margin_col, x, voo.voo_base.destino)
        p.drawString(
            margin_sides + 3 * margin_col, x, data_voo_str
        )
        p.drawString(margin_sides + 4 * margin_col, x, voo.estado_voo)
        x = x - line_break
        p.drawString(
            margin_sides + 1 * margin_col,
            x,
            horario_real_partida_str,
        )
        p.drawString(
            margin_sides + 2 * margin_col,
            x,
            horario_real_chegada_str,
        )
        x = x - line_break

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    messages.success(request, 'Relatório criado com sucesso')
    return FileResponse(buffer, as_attachment=True, filename="report_by_airport.pdf")

@check_user_able_to_see_page(Group.gerentes)
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
    report_voo = VooReal.objects.all().filter(voo_base__data_voo__range=[start_date, end_date])
    
    if not report_voo:
        messages.warning(request, 'Não há voos para serem mostrados no relatorio')
        return render(request, "relatorios.html")
    
    x = top_page

    p.drawString(margin_sides, x, "Total de voos:")
    p.drawString(margin_sides + 1 * margin_col, x, "Total voos cancelados:")
    p.drawString(margin_sides + 3 * margin_col, x, "Duração média dos voos:")
    
    x = x - line_break

    p.drawString(margin_sides, x, str(report_voo.count()))
    p.drawString(margin_sides + 1 * margin_col, x, str(report_voo.filter(estado_voo='CAN').count()))
    
    a = VooReal.objects.aggregate(price_diff=Avg(F('horario_real_chegada') - F('horario_real_partida')))['price_diff']
    p.drawString(margin_sides + 3 * margin_col, x, str(a))

    x = x - 2*line_break

    for voo in report_voo:

         
        horario_partida_base_str = voo.voo_base.horario_partida_base.strftime("%H:%M:%S") if voo.voo_base.horario_partida_base else '---'
        data_voo_str = voo.voo_base.data_voo.strftime("%d/%m/%Y") if voo.voo_base.data_voo else '---'
        horario_real_partida_str = voo.horario_real_partida.strftime("%H:%M:%S") if voo.horario_real_partida else '---'
        horario_real_chegada_str = voo.horario_real_chegada.strftime("%H:%M:%S") if voo.horario_real_chegada else '---'
        duracao_base_srt = voo.voo_base.duracao_base.strftime("%H:%M:%S") if voo.voo_base.duracao_base else '---'
        
        p.drawString(margin_sides, x, voo.voo_base.codigo_voo)
        p.drawString(margin_sides + 1 * margin_col, x, voo.voo_base.companhia_aerea)
        p.drawString(margin_sides + 2 * margin_col, x, voo.voo_base.dia_da_semana)
        p.drawString(
            margin_sides + 3 * margin_col,
            x,
            horario_partida_base_str,
        )
        p.drawString(
            margin_sides + 4 * margin_col,
            x,
            duracao_base_srt,
        )
        x = x - line_break
        p.drawString(margin_sides + 1 * margin_col, x, voo.voo_base.origem)
        p.drawString(margin_sides + 2 * margin_col, x, voo.voo_base.destino)
        p.drawString(
            margin_sides + 3 * margin_col, x, data_voo_str
        )
        p.drawString(margin_sides + 4 * margin_col, x, voo.estado_voo)
        x = x - line_break
        p.drawString(
            margin_sides + 1 * margin_col,
            x,
            horario_real_partida_str,
        )
        p.drawString(
            margin_sides + 2 * margin_col,
            x,
            horario_real_chegada_str,
        )
        x = x - line_break

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    messages.success(request, 'Relatório criado com sucesso')
    return FileResponse(buffer, as_attachment=True, filename="report_by_time.pdf")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        ## Define o numero de tentativas
        num_max = 3

        # for each post there will be a try

        if "load_count" not in request.session:
            request.session["load_count"] = 1
        else:
            request.session["load_count"] = request.session["load_count"] + 1

        if request.session["load_count"] >= num_max:
            messages.warning(request, 'Número de tentativas excedido')
            return render(request,"login.html")

        if user is not None:
            if request.session["load_count"] <= num_max:
                request.session["load_count"] = 0
                request.session.save()
                login(request, user=user)
                return redirect(home)
        else:
            messages.warning(request,"Ops... usuário ou senha inválido")
            return render(request,"login.html")
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return render(request, "login.html")


@check_user_able_to_see_page(Group.gerentes)
def relatorios(request):
    if request.method == "POST":
        if request.POST.get("cia_id"):
            return generate_report_airline(request, request.POST.get("cia_id"))
        elif request.POST.get("data_inicial_id"):
            data_inicial = request.POST.get("data_inicial_id")
            data_final = request.POST.get("data_final_id")
            if(data_inicial > data_final):
                messages.warning(request, 'A data inicial deve ocorrer antes da data final')
                return render(request, "relatorios.html")
            return generate_report_data(request, data_inicial, data_final)
        else:
            return render(request, "relatorios.html")
    else:
        return render(request, "relatorios.html")

@check_user_able_to_see_page(Group.gerentes)
def relatoriosPdf(request):
    messages.add_message(request, messages.SUCCESS, 'Relatorio gerado com suceso')
    return render(request, "relatorios-pdf.html")

@check_user_able_to_see_page(Group.gerentes)
def relatoriosBase(request):
    messages.add_message(request, messages.SUCCESS, 'Relatorio gerado com sucesso')
    return render(request, "relatorios-base.html")
