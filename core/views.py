from multiprocessing import context
from django.views.generic import View
from django.shortcuts import render

class Homeview(View):
    def get(self, request, *args,**kwargs):
        context = {}
        return render(request, 'index.html', context)
