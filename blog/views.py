from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import BlogPost
from .serializers import BlogPostSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .user_serializers import UserRegistrationSerializer
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponseServerError

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all().order_by('-timestamp')
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def post_detail(request, post_id):
    try:
        post = get_object_or_404(BlogPost, id=post_id, status='published')
        return render(request, 'blog/post_detail.html', {'post': post})
    except Exception as e:
        return render(request, 'blog/post_detail.html', {'post': None, 'error_message': f"Error loading post: {str(e)}"})

def post_list(request):
    try:
        posts = BlogPost.objects.filter(status='published').order_by('-timestamp')
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        user = request.user if request.user.is_authenticated else None
        return render(request, 'blog/post_list.html', {
            'posts': page_obj,
            'user': user,
            'page_obj': page_obj,
        })
    except Exception as e:
        return render(request, 'blog/post_list.html', {
            'posts': [],
            'user': None,
            'page_obj': None,
            'error_message': f"Error loading posts: {str(e)}"
        })

@csrf_exempt
def register(request):
    message = None
    if request.method == 'POST':
        from django.contrib.auth.models import User
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if username and password:
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, email=email, password=password)
                message = 'Registration successful. You can now log in.'
            else:
                message = 'Username already exists.'
        else:
            message = 'Please fill in all required fields.'
    return render(request, 'blog/register.html', {'message': message})

@csrf_exempt
def login_view(request):
    message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            message = 'Login successful.'
        else:
            message = 'Invalid username or password.'
    return render(request, 'blog/login.html', {'message': message})

@csrf_exempt
def logout_view(request):
    auth_logout(request)
    return render(request, 'blog/login.html', {'message': 'You have been logged out.'})

@csrf_exempt
def create_post(request):
    user = request.user if request.user.is_authenticated else None
    message = None
    if not user:
        return render(request, 'blog/create_post.html', {'user': user, 'message': 'You must be logged in to create a post.'})
    try:
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            status_val = request.POST.get('status')
            if title and content and status_val:
                from .models import BlogPost
                BlogPost.objects.create(title=title, content=content, author=user, status=status_val)
                message = 'Post created successfully.'
            else:
                message = 'Please fill in all fields.'
        return render(request, 'blog/create_post.html', {'user': user, 'message': message})
    except Exception as e:
        return render(request, 'blog/create_post.html', {'user': user, 'message': f"Error creating post: {str(e)}"})

@csrf_exempt
def edit_post(request, post_id):
    user = request.user if request.user.is_authenticated else None
    from .models import BlogPost
    post = BlogPost.objects.filter(id=post_id, author=user).first()
    message = None
    if not user or not post:
        return render(request, 'blog/edit_post.html', {'user': user, 'post': post, 'message': 'You do not have permission to edit this post.'})
    try:
        if request.method == 'POST':
            if request.POST.get('delete'):
                post.delete()
                return render(request, 'blog/edit_post.html', {'user': user, 'post': None, 'message': 'Post deleted successfully.'})
            title = request.POST.get('title')
            content = request.POST.get('content')
            status_val = request.POST.get('status')
            if title and content and status_val:
                post.title = title
                post.content = content
                post.status = status_val
                post.save()
                message = 'Post updated successfully.'
            else:
                message = 'Please fill in all fields.'
        return render(request, 'blog/edit_post.html', {'user': user, 'post': post, 'message': message})
    except Exception as e:
        return render(request, 'blog/edit_post.html', {'user': user, 'post': post, 'message': f"Error updating post: {str(e)}"})
