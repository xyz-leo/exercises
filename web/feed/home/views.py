from django.shortcuts import render
from .models import Post
from faker import Faker

fake = Faker('pt_BR')

def generate_posts(qtd=10):
    # Delete all posts
    Post.objects.all().delete()

    # Create new fake posts
    for _ in range(qtd):
        Post.objects.create(
            author=fake.user_name(),
            content= fake.catch_phrase()
        )

def home_view(request):
    generate_posts(qtd=20)  # Runs everytime the page is accessed

    posts = Post.objects.order_by('-created_at')
    context = {
        'posts': posts
    }
    return render(request, 'home/home.html', context)
