# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse("SmartList is live ✅")

