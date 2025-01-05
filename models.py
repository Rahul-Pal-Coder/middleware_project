from django.db import models
from django.contrib.auth.models import User

# Multi-tenancy: Define a Tenant Model
class Tenant(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Admin user for tenant
    
    def __str__(self):
        return self.name

# Schema Model to store schema information
class Schema(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    schema_data = models.JSONField()  # Store schema in JSON format

    def __str__(self):
        return self.name

# Mapping Model for schema to map fields between source and target
class Mapping(models.Model):
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    source_field = models.CharField(max_length=255)
    target_field = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.source_field} -> {self.target_field}"



# adding new model

# from django.db import models

# class TellyData(models.Model):
#     id = models.CharField(max_length=100, primary_key=True)
#     name = models.CharField(max_length=200)
#     description = models.TextField()
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField()

#     def __str__(self):
#         return self.name


# cargowise

from django.db import models

class XMLData(models.Model):
    xml_content = models.TextField()  # Store raw XML data
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"XMLData {self.id}"
