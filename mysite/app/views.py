from django.shortcuts import render

# Create your views here.


def monitoracao(request):
    return render(request,"monitoracao.html")

def olamundo(request):
    return render(request,"ola_mundo.html")

def home(request):
    return render(request,"home.html")

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