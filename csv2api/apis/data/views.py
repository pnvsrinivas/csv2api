import json
import pandas as pd

from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User

from csv2api.apis.data.serializers import UploadSerializer
from csv2api.core.models import Dataset


class DatasetUploadView(APIView):
    """
    create:
    Uploads a new dataset instance.
    """
    parser_class = (FileUploadParser,)
    queryset = Dataset.objects.all()
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = UploadSerializer(data=request.data, context={ 'request': request })

        if serializer.is_valid():
            created_by = self.request.user if isinstance(self.request.user, User) else None
            serializer.save(created_by=created_by)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DatasetAPIView(APIView):
    """
    retrieve:
    Return the given uuid data.
    """
    queryset = Dataset.objects.all()
    permission_classes = [AllowAny, ]

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        dataset = Dataset.objects.get(id=id)

        if dataset.is_expired:
            return Response({
                'message': 'This data is expired, only registered users data will be maintained!!'
            }, status=status.HTTP_404_NOT_FOUND)
        
        dataframe = pd.read_csv(dataset.file.path)
        rows, cols = dataframe.shape
        return Response({
                'records': rows,
                'headers': dataframe.columns.tolist(),
                'data': json.loads(dataframe.to_json(orient='records')),
            }, 
            status=status.HTTP_201_CREATED
        )



