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
from users.models import Profile, Inbox
from stream.models import Post, Comment

# Author API
class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['type', 'id', 'host', 'displayName', 'url', 'github', 'profileImage']

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = AuthorSerializer
# Post API
class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        # description, commentsSrc is missing
        fields = ['type', 'title', 'id', 'source', 'origin', 'contentType', 'content', 
                  'author', 'categories', 'count', 'comments', 'published', 'visibility', 'unlisted']
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# Comment API
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['type', 'author', 'comment', 'contentType', 'published', 'id']
        
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

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
    path('profile/update.html', user_views.update, name="update"),
    path('profile/followers.html', user_views.followers, name="followers"),
    path('inbox/', user_views.inbox, name='inbox'),
    path('inbox/accept', user_views.accept, name='accept'),
    path("api/", include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace = 'rest_framework')),
    
    # Keep this at the bottom
    path("", include('stream.urls')),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
