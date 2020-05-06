from rest_framework import serializers

from csv2api.core.models import Dataset

class UploadSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='data', lookup_field="id", read_only=True)
    filename = serializers.SerializerMethodField()
    validity = serializers.SerializerMethodField()
    file = serializers.FileField(write_only=True)
    
    def get_filename(self, obj):
        return obj.file.name.split("/")[-1]
    
    def get_validity(self, obj):
        if obj.created_by:
            return None
        return obj.validity
    
    class Meta:
        model = Dataset
        fields = (
            "url",
            "filename", 
            "validity", 
            "file",
        )
