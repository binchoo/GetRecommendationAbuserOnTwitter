from django.http import HttpResponse, JsonResponse, FileResponse
from DirectiveMerger import settings as MergerSettings
import json
# Create your views here.

cache = None

def get_directives_fast(request) :
    global cache
    if cache is None :
        with open(MergerSettings.MERGER_RESULT_PATH, "r") as f :
            cache = json.load(f)
    return JsonResponse(cache, safe=False)

def get_directives_slow(reqeust) :
    json = open(MergerSettings.MERGER_RESULT_PATH, "r")
    return FileResponse(json)