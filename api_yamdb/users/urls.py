from django.urls import include, path
from users.v1.urls import v1_urlpatterns

urlpatterns = [
    path('v1/', include(v1_urlpatterns)),
]
