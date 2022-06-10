from django.views.decorators.cache import never_cache
from rest_framework.decorators import api_view
from rest_framework.response import Response

from database.models import *

@never_cache
@api_view(['GET'])
def test_job(req)->Response:
    print("test route")
    from .queue import queue_test_job
    queue_test_job()
    return Response()