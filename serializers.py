from rest_framework import serializers
from .models import Schema, Mapping

class SchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schema
        fields = ['id', 'name', 'schema_data']

class MappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mapping
        fields = ['id', 'source_field', 'target_field']
