from django.shortcuts import render
import json,redis
from django.conf import settings

def index(request):
 redis_client=redis.Redis(host=settings.REDIS_HOST,port=6379,decode_responses=True)
 
 data=redis_client.get('students:all') or '[]'
 students=json.loads(data)
 
 return render(request, 'index.html', {'students': students})
