from django.shortcuts import render

from django.http import HttpResponse

def home(request, param):
    return HttpResponse("<h1>Hello " + param + " </h1>")

def homevide(request):
    return HttpResponse("<h1>Hello toi </h1>")

def about_us(request):
    return HttpResponse("<h1>About Us</h1>")

def contact_us(request):
    return HttpResponse("<h1>Contact Us</h1>")