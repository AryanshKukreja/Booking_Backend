from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = routers.DefaultRouter()
router.register(r'sports', views.SportViewSet)
router.register(r'timeslots', views.TimeSlotViewSet)

app_name = 'booking'

urlpatterns = [
    # API endpoints only
    path('api/', include(router.urls)),
    path('api/court-status/', views.court_status_api, name='court_status_api'),
    path('api/update-booking/', views.update_booking_api, name='update_booking_api'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

from django.http import JsonResponse

def api_root(request):
    return JsonResponse({"message": "Welcome to the Sports Booking API", "endpoints": ["/api/", "/api/court-status/", "/api/update-booking/"]})

urlpatterns += [
    path('', api_root),
]
