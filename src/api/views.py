from django.views.decorators.cache import never_cache
from rest_framework.decorators import api_view
from rest_framework.response import Response

from database.models import *

@never_cache
@api_view(['GET'])
def test_job(req)->Response:
    clust = req.GET.get('clust')
    print("test route")
    from .queue import queue_test_job
    queue_test_job(clust)
    return Response()


@api_view(['POST'])
def upload_matrix(req)->Response:
    print(req)
    print("done")
    return Response({})