import os
import json
import math
import pandas as pd
import numpy as np

from rest_framework import viewsets
from rest_framework import pagination
from rest_framework.parsers import FileUploadParser, BaseParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

from csv2api.apis.data.serializers import (
    FileUploadSerializer, DatasetSerializer, FileUrlSerializer
)
from csv2api.core.models import Dataset


class FileUrlParser(BaseParser):
    """
    Plain text parser.
    """
    media_type = '*/*'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Simply return a string representing the body of the request.
        """
        import pdb; pdb.set_trace()
        return stream.read()


class FileUploadView(APIView):
    """
    create:
    Uploads a new dataset instance.
    """
    parser_class = (FileUrlParser, FileUploadParser, )
    queryset = Dataset.objects.all()
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        file_name = None

        if isinstance(request.data.get('file'), InMemoryUploadedFile):
            serializer = FileUploadSerializer(data=request.data, context={ 'request': request })
        else:
            serializer = FileUrlSerializer(data=request.data, context={ 'request': request })

        if serializer.is_valid():
            if request.user.is_authenticated:
                serializer.validated_data.update({ 'created_by': request.user })

            if 'file_name' in serializer.validated_data:
                file_name = serializer.validated_data.pop('file_name')
            if 'file_content' in serializer.validated_data:
                file_content = serializer.validated_data.pop('file_content')

            dataset_obj = serializer.save()

            if file_name:
                dataset_obj.file.save(file_name, ContentFile(file_content))

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileDataAPIView(APIView):
    """
    retrieve:
    Return the given uuid data.
    """
    queryset = Dataset.objects.all()
    permission_classes = [AllowAny, ]

    def get(self, request, *args, **kwargs):
        no_of_pages = None
        DEFAULT_PAGE_SIZE = 10
        dataset_id = kwargs.get('id')
        dataset = Dataset.objects.get(id=dataset_id)

        page = int(request.GET.get('page', 1) or 1)
        size = request.GET.get('size', DEFAULT_PAGE_SIZE)

        sort_by = request.GET.get('sort_by')

        is_file_exists = os.path.exists(dataset.file.path)
        if dataset.is_expired or not is_file_exists:
            print("File not found: {}".format(dataset.file.url))
            return Response(
                {
                    'message': 'This data is expired, only registered users data will be maintained!!'
                }, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        df = pd.read_csv(dataset.file.path)
        rows, cols = df.shape

        if sort_by:
            sort_by = sort_by.split(',')
            cleanned_sort_by = [column for column in sort_by if column in df.columns.tolist()]
            if len(cleanned_sort_by) > 0:
                df.sort_values(by=cleanned_sort_by, inplace=True)
            else:
                return Response(
                    {
                        'message': '{} is/are unknown column(s), please provide at least one known column. Available are: {}'.format(
                            ",".join(np.setdiff1d(sort_by, df.columns.tolist()).tolist()),
                            ",".join(df.columns.tolist())
                        )
                    }, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        if not str(size).replace(".", "").isnumeric():
            if size == 'all':
                no_of_pages = 1 if rows > 0 else 0
                page = 1
                size = rows
            else: # If size is not numeric and is not 'all' then set to default page size
                size = DEFAULT_PAGE_SIZE
        else: # If size is numeric then parse it.
            size = int(size)

        if size != rows:
            start_index = (page - 1) * size
            end_index = page * size
            df = df.iloc[start_index: end_index]
            no_of_pages = math.ceil(rows / size)
        
        return Response({
                'no_of_rows': rows,
                'no_of_cols': cols,
                'page': page,
                'size': size,
                'no_of_pages': no_of_pages,
                'data': json.loads(df.to_json(orient='records')),
                'header_names': df.columns.tolist(),
            }, 
            status=status.HTTP_201_CREATED
        )


class DatasetModelViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all().order_by('-created_on')
    serializer_class = DatasetSerializer
    pagination.PageNumberPagination.page_size = 5