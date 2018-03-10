from django.urls import reverse
from django.http import HttpResponseRedirect

def frontpage(request):
    return HttpResponseRedirect(reverse('categories'))
