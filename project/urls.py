from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework import routers
from bookmark.views import BookmarkViewSet, bookmark_list
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.views.generic import RedirectView

router = routers.DefaultRouter()
router.register(r'bookmarks', BookmarkViewSet, basename='bookmark')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/login/', permanent=False)),
    # ブラウザ画面
    path("bookmarks/", bookmark_list, name="bookmark_list"),
    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # API
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
