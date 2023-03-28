"""social_distribution URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers, serializers, viewsets
from users.models import Profile
from stream.models import Post, Comment
from django.conf.urls.static import static
from stream import views

# Author API
class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['type', 'id', 'host', 'displayName', 'url', 'github', 'profileImage']

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = AuthorSerializer

# Comment API
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['type', 'author', 'comment', 'contentType', 'published', 'id']

    def get_author(self, obj):
        author = {
            'type': 'author',
            'id': f'http://127.0.0.1:5454/authors/{obj.author.id}',
            'url': f'http://127.0.0.1:5454/authors/{obj.author.id}',
            'host': 'http://127.0.0.1:5454/',
            'displayName': obj.author.username,
            'github': obj.author.profile.github,
            'profileImage': obj.author.profile.profileImage.url if obj.author.profile.profileImage else '',
        }
        return author
        
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

# Post API
class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'source', 'origin', 'contentType', 'content', 'categories', 'count', 'comments', 'published', 'visibility', 'unlisted')

    def get_author(self, obj):
        author = {
            'type': 'author',
            'id': f'http://127.0.0.1:5454/authors/{obj.author.id}',
            'url': f'http://127.0.0.1:5454/authors/{obj.author.id}',
            'host': 'http://127.0.0.1:5454/',
            'displayName': obj.author.username,
            'github': obj.author.profile.github,
            'profileImage': obj.author.profile.profileImage.url if obj.author.profile.profileImage else '',
        }
        return author
        
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# API router
router = routers.DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", user_views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),
    path('profile/', user_views.profile, name="profile"),
    path("api/", include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace = 'rest_framework')),
    path('login/token/', views.obtain_token, name='token_obtain_pair'),
    
    # Keep this at the bottom
    path("", include('stream.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)