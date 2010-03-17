from django.db import models
from django.contrib.auth.models import User, Group


class PhoneNumberManager(models.Manager):
    def get_reply_numbers(self, number):
        """Returns the set of all other numbers in the system,
        excluding the sender.
        @number The number of the sender
        """
        try:
            pn = self.get(number=number)
        except PhoneNumber.DoesNotExist:
            return [] 
        return [pn.number for pn in self.exclude(number=number)]


class PhoneNumber(models.Model):
    """Phone numbers for the mass texting."""
    number = models.CharField(max_length=10)
    owner = models.ForeignKey(User)
    call_list = models.ForeignKey('CallList')
    can_send = models.BooleanField(default=True)
    
    def __unicode__(self):
        return u'%s, for %s' % (self.number, self.owner.username)

    objects = PhoneNumberManager()


class CallList(models.Model):
    """Implements a basic call list for the reflection, with minimal permissions."""
    name = models.CharField(max_length=255)
    moderated = models.BooleanField(default=False)
    