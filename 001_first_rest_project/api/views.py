from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timezone
import pytz
from pytz.exceptions import UnknownTimeZoneError
from rest_framework import status

def index(request):
    return HttpResponse('<h1>Hello</h1>')
    # return JsonResponse({'page': 'home'})

# 時間を返す
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def country_datetime(request):
    if request.method == 'POST':
        # print(request.data)
        requested_timezone = request.data.get('timezone')
        if requested_timezone:
            try:
                tz = pytz.timezone(requested_timezone) # requestで指定したタイムゾーン
            except UnknownTimeZoneError as e:
                return Response({"Error POST": "Timezone not exists"}, status=status.HTTP_400_BAD_REQUEST)
            utc_datetime = datetime.now(timezone.utc) # utc時刻
            return Response( # utc → timezone
                {f"DateTime POST: {requested_timezone}": utc_datetime.astimezone(tz)}
            )
    elif request.method == 'PUT':
        print('PUTが呼ばれました')
    elif request.method == 'DELETE':
        print('DELETEが呼ばれました')
    else:
        requested_timezone = request.query_params.get('timezone')
        if requested_timezone:
            try:
                tz = pytz.timezone(requested_timezone) # requestで指定したタイムゾーン
            except UnknownTimeZoneError as e:
                return Response({"Error GET": "Timezone not exists"}, status=status.HTTP_400_BAD_REQUEST)
            
            utc_datetime = datetime.now(timezone.utc) # utc時刻
            return Response( # utc → timezone
                {f"DateTime GET: {requested_timezone}": utc_datetime.astimezone(tz)}
            )
    return Response({"Datetime": datetime.now()})
