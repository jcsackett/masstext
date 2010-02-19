from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import loader, Context

from myproject.texts.models import PhoneNumber

def build_response(user, new_numbers, body):
    msg = '%s says: %s' % (user.username, body)
    t = loader.get_template('response.xml')
    c = Context({
        'numbers':new_numbers,
        'msg':msg
    })

    xml = t.render(c)

    return HttpResponse(xml, mimetype='text/xml')

def mass_text(request):
    
    if request.method == 'GET':
        return HttpResponse('This is not working.')
    if request.method == 'POST':
        number = request.POST['From']
	user = PhoneNumber.objects.get(number=number).owner
        new_numbers = PhoneNumber.objects.get_reply_numbers(number)   

        body = request.POST['Body']

        return build_response(user, new_numbers, body)

