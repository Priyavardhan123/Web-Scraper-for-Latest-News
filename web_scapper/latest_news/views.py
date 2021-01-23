from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html') 
    
def international(request):
    return render(request, 'international.html') 

def national(request):
    return render(request, 'national.html') 

def sports(request):
    return render(request, 'sports.html') 

def finance(request):
    return render(request, 'finance.html') 

def entertainment(request):
    return render(request, 'entertainment.html') 