import requests

from rest_framework import serializers

from csv2api.core.models import Dataset


# Serializers define the API representation.

class DatasetSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='file-detail', lookup_field="id", read_only=True)
    filename = serializers.SerializerMethodField()

    def get_filename(self, obj):
        return obj.file.name.split("/")[-1] if obj.file.name else None

    class Meta:
        model = Dataset
        fields = (
            'id', 'url', 'filename', 
            'validity', 
        )


class FileUploadSerializer(DatasetSerializer):

    file = serializers.FileField(write_only=True)

    def validate_file(self, file):
        if not file.name.endswith('.csv'):
            raise serializers.ValidationError("Please upload a csv file.")
        return file

    class Meta(DatasetSerializer.Meta):
        model = Dataset
        fields = DatasetSerializer.Meta.fields + (
            "file", 
        )

class FileUrlSerializer(DatasetSerializer):

    file = serializers.URLField(write_only=True)

    def validate(self, validated_data):
        file = self.initial_data.get('file')

        if not file.endswith('.csv'):
            raise serializers.ValidationError("Please upload a csv file.")

        validated_data['file_name'] = file.split('/')[-1]
        try:
            validated_data['file_content'] = requests.get(file).content
        except Exception as e:
            raise serializers.ValidationError(str(e))

        return validated_data

    class Meta(DatasetSerializer.Meta):
        model = Dataset
        fields = DatasetSerializer.Meta.fields + (
            "file", 
        )