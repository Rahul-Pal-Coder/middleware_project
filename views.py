from django.shortcuts import render
from django.http import HttpResponse

from .models import Tenant, Schema, Mapping
from django.http import JsonResponse
from .serializers import SchemaSerializer, MappingSerializer
import xmltodict
import json
from cryptography.fernet import Fernet
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

# Encryption utility for secure data
def encrypt_data(data):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data, key

def decrypt_data(encrypted_data, key):
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return decrypted_data

# Example of converting XML to JSON format
def convert_xml_to_json(xml_data):
    dict_data = xmltodict.parse(xml_data)
    json_data = json.dumps(dict_data)
    return json_data


# Upload schema view
@login_required
def upload_schema(request):
    if request.method == "POST":
        schema_name = request.POST.get('schema_name')
        schema_data = json.loads(request.POST.get('schema_data'))
        tenant = Tenant.objects.get(id=request.user.id)  # Assuming the logged-in user is a tenant
        schema = Schema(tenant=tenant, name=schema_name, schema_data=schema_data)
        schema.save()
        return JsonResponse({"status": "Schema uploaded successfully"})
    return render(request, 'upload_schema.html')

# API View for Schema Data
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def get_schemas(request):
    if request.method == 'GET':
        schemas = Schema.objects.all()
        serializer = SchemaSerializer(schemas, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        serializer = SchemaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

# Mapping API View
@api_view(['GET', 'POST'])
def get_mappings(request):
    if request.method == 'GET':
        mappings = Mapping.objects.all()
        serializer = MappingSerializer(mappings, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        serializer = MappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

# Function to simulate pushing data to ERP via API
import requests

def push_data_to_erp(api_url, data):
    response = requests.post(api_url, json=data)
    return response.json()


# import requests

# api_url = "http://127.0.0.1:8000/api/push_to_erp/"
# data = {
#     "product_id": 123,
#     "product_name": "Sample Product",
#     "quantity": 10,
#     "price": 99.99
# }

# response = requests.post(api_url, data={'data': str(data)})  # Sending data as a form-encoded POST
# print(response.json())



from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import XMLUploadForm
from .models import XMLData

def upload_xml(request):
    if request.method == 'POST' and 'xml_file' in request.FILES:
        xml_file = request.FILES['xml_file']
        xml_content = xml_file.read().decode('utf-8')  # Read XML file content
        xml_data = XMLData.objects.create(xml_content=xml_content)
        return HttpResponse(f"XML Data saved with ID: {xml_data.id}")
    return render(request, 'upload_xml.html')
