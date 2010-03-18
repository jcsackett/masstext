from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from masstext.models import PhoneNumber, CallList

class SimpleTextingTestCase(TestCase):
    fixtures = ['phonenumber.json']
   
    def setUp(self):
        self.post_data = dict(
            From='9195555555',
            Body='This is a message.'
        )
        self.client = Client()
        self.url = reverse('masstext')

    def test_mass_text_get(self):
        #tests that gets return nothing
        r = self.client.get(self.url)
        self.assertEqual(r.content, "You don't get how this works, do you?")

    def test_post_moderated_can_send(self):
        #tests that user with send permissions on a moderated list can send messages
        expected = '''
        <?xmlversion="1.0"encoding="UTF-8"?>
        <Response>
            <Sms to="9195555556">test_one says: This is a message.</Sms>
            <Sms to="9195555557">test_one says: This is a message.</Sms>
        </Response>
        '''
        expected = ''.join(expected.split())
        r = self.client.post(self.url, self.post_data)
        received = ''.join(r.content.split())
        self.assertEqual(received, expected)

    def test_post_moderated_cannot_send(self):
        #tests that a user without send permissions on a moderated list can't send messages
        self.post_data['From'] = '9195555556'
        expected = '''
        <?xmlversion="1.0"encoding="UTF-8"?>
        <Response>
        </Response>
        '''
        expected = ''.join(expected.split())
        r = self.client.post(self.url, self.post_data)
        received = ''.join(r.content.split())
        self.assertEqual(received, expected)

    def test_post_not_moderated_can_send(self):
        #tests that a user on an unmoderated list can send regardless of permission
        #switch calllist to unmoderated
        c = CallList.objects.all()[0]
        c.moderated = False
        c.save()
        
        #first do the test for a user with send permissions
        expected = '''
        <?xmlversion="1.0"encoding="UTF-8"?>
        <Response>
            <Sms to="9195555556">test_one says: This is a message.</Sms>
            <Sms to="9195555557">test_one says: This is a message.</Sms>
        </Response>
        '''
        expected = ''.join(expected.split())
        r = self.client.post(self.url, self.post_data)
        received = ''.join(r.content.split())
        self.assertEqual(received, expected)

        #and now someone who normally can't send messages
        new_number = '9195555556'
        self.post_data['From'] = new_number
        self.assertEqual(PhoneNumber.objects.get(number=new_number).can_send, False)
        expected = '''
        <?xmlversion="1.0"encoding="UTF-8"?>
        <Response>
            <Sms to="9195555555">test_two says: This is a message.</Sms>
            <Sms to="9195555557">test_two says: This is a message.</Sms>
        </Response>
        '''
        expected = ''.join(expected.split())
        r = self.client.post(self.url, self.post_data)
        received = ''.join(r.content.split())
        self.assertEqual(received, expected)
        

class PhoneNumberManagerTestCase(TestCase):
    fixtures = ['phonenumber.json']
    
    def test_get_reply_numbers_with_valid_number(self):
        #tests that a valid reply set is returned for a valid number
        numbers = PhoneNumber.objects.all().values()
        sender = numbers[0]['number']
        receiver = [n['number'] for n in numbers[1:]]
        reply_set = PhoneNumber.objects.get_reply_numbers(sender)
        self.assertEqual(receiver, reply_set)

    def test_get_reply_numbers_with_invalid_number(self):
        #tests that an invalid number gets no reply set
        invalid_number = '9198888888'
        expected_reply = [] 
        reply_set = PhoneNumber.objects.get_reply_numbers(invalid_number)
        self.assertEqual(reply_set, expected_reply)
