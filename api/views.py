from django.shortcuts import render

from django.http import JsonResponse

def WarmMe(request):
    return JsonResponse({"message": "WarmMe endpoint is working"})