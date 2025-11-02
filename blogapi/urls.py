from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi

# schema_view = get_schema_view(
#    openapi.Info(
#       title="My blog API",
#       default_version='v1',
#       description="Some blog API",
#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email="contact@snippets.local"),
#       license=openapi.License(name="BSD License"),
#    ),
#    public=True,
#    permission_classes=(permissions.AllowAny,),
# )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('apiv1/', include(('posts.urls', 'posts'), namespace='posts')),
    path('apiv1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('apiv1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('apiv1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path("apiv1/docs/", SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path("apiv1/redoc/", SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
   #  path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   #  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   #  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),    
]
