
from rest_framework.decorators import api_view
from rest_framework.response import Response
from celery.result import AsyncResult
import json

# Create your views here.
import time
from .tasks import my_task, test_send_mail

@api_view(['POST'])
def my_vieww(request):
    result = my_task(3, 5)
    test_send_mail.apply_async(countdown=20)
    return Response({'hi':result})