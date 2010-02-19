from django.test import TestCase, Client
from django.contrib.auth.models import User

from masstext.models import PhoneNumber

class TextingTestCase(TestCase):
    def setUp(self):
        u1 = User(username='user1')
        u2 = User(username='user2')
        u1.save()
        u2.save()

        pn1 = PhoneNumber(owner=u1, number='9195555555')
        pn2 = PhoneNumber(owner=u2, number='9195555556')
        pn1.save()
        pn2.save()

    def test_mass_text_get(self):
        #tests that gets return nothing
        url = reverse('masstext')
        c = Client()
        r = c.get(url)
        self.assertEqual(r.content, "You don't get how this works, do you?")

    def test_mass_text_post(self):
        #tests that posts work
        url = reverse('masstext')
        c = Client()
        data = dict(
            From='9195555555',
            Body='This is a message.'
        )
        expected = '<Response><Sms to="9195555556">user1 says: This is a message.</Sms><Response>'
        r = c.post(url, data)
        received = ''.join(r.content.split())
        self.assertEqual(received, expected)
