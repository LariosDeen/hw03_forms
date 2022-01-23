from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Post, Group, User
from .forms import PostForm


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'title': 'Последние обновления на сайте',
    }
    template = 'posts/index.html'
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    template = 'posts/group_list.html'
    return render(request, template, context)


def profile(request, username):
    user_name = get_object_or_404(User, username=username)
    posts_counter = user_name.posts.count()
    post_list = user_name.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'user_name': user_name,
        'posts_counter': posts_counter,
        'page_obj': page_obj,
    }
    template = 'posts/profile.html'
    return render(request, template, context)


def post_detail(request, post_id):
    one_post = get_object_or_404(Post, id=post_id)
    username = one_post.author
    username_obj = User.objects.get(username=username)
    posts_counter = username_obj.posts.count()
    group_name = one_post.group
    context = {
        'one_post': one_post,
        'posts_counter': posts_counter,
        'group_name': group_name,
        'username': username,
        'post_id': post_id,
    }
    template = 'posts/post_detail.html'
    return render(request, template, context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    author = request.user
    template = 'posts/create_post.html'
    form.instance.author = author
    context = {
        'form': form,
    }
    if not form.is_valid():
        return render(request, template, context)
    form.save()
    return redirect(f'/profile/{author}/')


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect(f'/posts/{post_id}/')
    elif request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect(f'/posts/{post_id}/')
    form = PostForm(initial={'group': post.group, 'text': post.text})
    is_edit = True
    template = 'posts/create_post.html'
    context = {
        'form': form,
        'is_edit': is_edit,
    }
    return render(request, template, context)
