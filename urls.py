from django.urls import path
from . import views
# from .views import SendMessageView
# from .schema import schema



urlpatterns = [
    path('upload_schema/', views.upload_schema, name='upload_schema'),
    path('schemas/', views.get_schemas, name='schemas'),
    path('mappings/', views.get_mappings, name='mappings'),
    path('push_to_erp/', views.push_data_to_erp, name='push_to_erp'),
    path('upload/', views.upload_xml, name='upload_xml'),
    
]
