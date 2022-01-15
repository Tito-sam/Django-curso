from multiprocessing import context
from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import PostCreateForm
from .models import Post

class BlogListView(View):
    def get(self, request, *args, **wkargs):
        context = {}
        return render(request, 'blog_list.html', context)


class BlogCreateView(View):
    def get(self, request, *args,**wkargs):
        form = PostCreateForm()
        context = {
            'form':form
        }
        return render(request, 'blog_create.html', context)

    def post(self, request, *args,**wkargs):
        # revisamos si el metodo que se esta activando en la pagina es post
        if request.method == 'POST':
            #creamos una variable que tenga el formulario de la pagina con metodo post
            form = PostCreateForm(request.POST)
            # revisamos si el formulario es valido
            if form.is_valid():
                # obtenemos y guardamos los datos de el form
                title = form.cleaned_data.get('title')
                content = form.cleaned_data.get('content')
                #creamos en la base de datos el objeto con los datos obtenidos
                p, created = Post.objects.get_or_create(title=title,content=content)
                #guardamos todo
                p.save()
                #redirigimos con redirect a el home del blog
                return redirect('blog:home')
        context = {}
        return render(request, 'blog_create.html', context)