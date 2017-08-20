from django.shortcuts import render
from django.utils import timezone
from .models import Post, Category
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, ContactForm
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.db.models import Q
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages



def post_list(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(name, message, from_email, ['mat.slisz@yahoo.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.success(request, 'Thanks for your reply')
            return redirect('post_list')
    
    post_list = Post.objects.all()
    page = request.GET.get('page')
    forms = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[0:3]
    categories = Category.objects.all()

    query = request.GET.get("q")
    if query:
        post_list = post_list.filter(
                    Q(text__icontains=query)|
                    Q(title__icontains=query)|
                    Q(published_date__icontains=query)|
                    Q(created_date__icontains=query))
                    
    paginator = Paginator(post_list, per_page=3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator(paginator.num_pages)
    
    context = {
        'posts': posts,
        'page': page,
        'forms': forms, 
        'categories': categories,
        'form': form,
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = post
    category = post

    context = {
        'post': post, 
        'form' : form, 
        'category': category,
    }
    return render(request, 'blog/post_detail.html', context)


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    
    context = {
        'form': form,
    }
    return render(request, 'blog/post_edit.html', context)


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
    }
    return render(request, 'blog/post_edit.html', context)


def category_list(request, pk):
    categories = Category.objects.all()
    category = get_object_or_404(Category, pk=pk)
    forms = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[0:3]
    post_numbers =  Post.objects.filter(category=category).count
    
    context = {
        'category': category, 
        'categories': categories,  
        'forms': forms,
        'post_numbers': post_numbers,
    }
    return render(request, 'blog/category_list.html', context)


def about(request):
    return render(request, 'blog/about.html')


def projects(request):
    return render(request, 'blog/projects.html')
