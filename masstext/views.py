from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import loader, Context

from masstext.models import PhoneNumber
from masstext.utils import build_response 

def mass_text(request):
    """The core (and currently only) view. Takes a POST from twilio and returns the sms
    commands.
    @request The HttpRequest
    """
    if request.method == 'GET':
        return HttpResponse("You don't get how this works, do you?")
    if request.method == 'POST':
        number = request.POST['From']
        user = PhoneNumber.objects.get(number=number).owner
        new_numbers = PhoneNumber.objects.get_reply_numbers(number)   

        body = request.POST['Body']

        return build_response(user, new_numbers, body)

