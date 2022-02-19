
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),
    path('api/token/gettoken', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/accounts/', include('accounts.urls')),
    path('api/contacts/', include('contacts.urls')),
    path('api/realtors/', include('realtors.urls')),
    path('api/listings/', include('listings.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
