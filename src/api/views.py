from django.views.decorators.cache import never_cache
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from database.models import *

@never_cache
@api_view(['GET'])
def test_job(req : Request)->Response:
    clust = req.GET.get('clust')
    print("test route")
    from .queue import queue_test_job
    queue_test_job(clust)
    return Response()