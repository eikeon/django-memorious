from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import get_template


def home(request):
    context = RequestContext(request, {})
    template = get_template('home.html')
    return HttpResponse(content=template.render(context))

