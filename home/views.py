from django.shortcuts import render
from django.http import HttpResponse
from home.models import NativeTx
# Create your views here.

def index(request):

    # Page from the theme 
    return render(request, 'pages/dashboard.html')
