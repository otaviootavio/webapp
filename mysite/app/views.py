from django.shortcuts import render

# Create your views here.


def create(request):
    return render(request,"create.html")

def update(request):
    return render(request,"update.html")

def delete(request):
    """ TODO """
    return render(request,"CRUD.html")

def flightData(request):
    return render(request,"flight-data.html")

def crud(request):
    return render(request,"CRUD.html")

def monitoracao(request):
    return render(request,"monitoracao.html")

def olamundo(request):
    return render(request,"ola-mundo.html")

def home(request):
    return render(request,"home.html")

def monitoracao(request):
    if request.method == 'POST':
        if request.POST.get('voo_id') == "7":
            return render(request,"monitoracao_resultado.html")
        return render(request,"monitoracao.html")
    return render(request,"monitoracao.html")

def monitoracao_update(request):
    if request.method == 'POST':
        return render(request,"monitoracao_resultado.html")
    return render(request,"monitoracao_resultado.html")

def login(request):
    if request.method == 'POST':
        # Process the request if posted data are available
        username = request.POST['username']
        password = request.POST['password']
        # Check username and password combination if correct
        #user = authenticate(username=username, password=password)
        if username == 'admin' and password == 'admin':
            # Save session as cookie to login the user
            #login(request, user)
            # Success, now let's login the user.
            return render(request, "home.html")
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, "login.html", {'error_message': 'Incorrect username and / or password.'})
    else:
        # No post data availabe, let's just show the page to the user.
        return render(request, "login.html")

def relatorios(request):
    return render(request, "relatorios.html")

def relatoriosCiaAerea(request):
    if request.method == 'POST':
        if request.POST.get('cia_id') == "Latam":
            return render(request,"relatorios-pdf.html")
        return render(request,"relatorios-cia-aerea.html")
    return render(request, "relatorios-cia-aerea.html")

def relatoriosPeriodo(request):
    if request.method == 'POST':
        if request.POST.get('aeroporto_id') == "Congonhas" and request.POST.get('data_inicial_id') == "2022-10-01" and request.POST.get('data_final_id') == "2022-10-19":
            return render(request,"relatorios-pdf.html")
        return render(request,"relatorios-periodo.html")
    return render(request, "relatorios-periodo.html")

def relatoriosPdf(request):
    return render(request, "relatorios-pdf.html")