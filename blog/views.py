from django.shortcuts import render
from django.utils import timezone
from .models import Post, Category
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView


def post_list(request):
    post_list = Post.objects.all()
    page = request.GET.get('page')
    forms = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[0:3]
    categories = Category.objects.all()
    paginator = Paginator(post_list, per_page=3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator(paginator.num_pages)
    return render(request, 'blog/post_list.html', {'posts': posts,'page': page, 'forms': forms, 'categories': categories})



def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = post
    category = post
    return render(request, 'blog/post_detail.html', {'post': post, 'form' : form, 'category': category,})


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
    return render(request, 'blog/post_edit.html', {'form': form})


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
    return render(request, 'blog/post_edit.html', {'form': form})


def category_list(request):
    categories = Category.objects.all()
    posts = Post.objects.all().filter('category')
    return render (request, 'blog/category_list.html', {'categories': categories, 'posts': posts}) # blog/category_list.html should be the template that categories are listed.


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)

    return render(request, 'blog/category_detail.html', {'category': category}) 


def about(request):
    return render(request, 'blog/about.html')


def projects(request):
    return render(request, 'blog/projects.html')
