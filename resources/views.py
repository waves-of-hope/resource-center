from django.shortcuts import render

def index(request):
    context = {'index': True}
    return render(request, 'index.html', context)
