from django.shortcuts import render

# Create your views here.

globalAccess = ""

def create(request):
    return render(request,"create.html")

def update(request):
    return render(request,"update.html")

def delete(request):
    """ TODO """
    return render(request,"crud.html")

def flightData(request):
    return render(request,"flight-data.html")

def crud(request):
    global globalAccess
    if globalAccess == 'crud' or globalAccess == 'admin':
      return render(request,"crud.html")
    else:
      return render(request,"home.html", {'error_message': 'You don\'t have permission to access this resource.'})


def olamundo(request):
    return render(request,"ola-mundo.html")

def home(request):
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