from django.http import HttpResponse
from django.template import loader, Context


def build_response(user, new_numbers, body):
    msg = '%s says: %s' % (user.username, body)
    t = loader.get_template('response.xml')
    c = Context({
        'numbers':new_numbers,
        'msg':msg
    })

    xml = t.render(c)

    return HttpResponse(xml, mimetype='text/xml')


