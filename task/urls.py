from django.urls import path
from .views import index,detail, new, update

urlpatterns = [
    
    path('', index, name="index" ),
    path('<int:pk>', detail, name="Detail" ),
    path('new/', new, name="new" ),
    path('<int:pk>/update/', update, name="update" ),
    
]