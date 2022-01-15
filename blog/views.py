from multiprocessing import context
from re import template
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, UpdateView, DeleteView
from .forms import PostCreateForm
from .models import Post
from django.urls import reverse_lazy

#enlistar post
class BlogListView(View):
    def get(self, request, *args, **wkargs):
        # se obtienen los posts de la base de datos
        posts = Post.objects.all()
        #se le pasan los post al contexto para la pagina
        context = {
            'posts':posts
        }
        # renderisamos todo con render
        return render(request, 'blog_list.html', context)

#crear un post
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

#detallar el post
class BlogDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk = pk)
        context = {
            'post':post
        }
        return render(request, 'blog_detail.html', context)

#actualizar el post
class BlogUpdateView(UpdateView):
    model=Post
    fields=['title','content']
    template_name = 'blog_update.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('blog:detail', kwargs={'pk':pk})

#eliminar el post
class BlogDeleteView(DeleteView):
    model=Post
    template_name = 'blog_delete.html'
    success_url = reverse_lazy('blog:hole')