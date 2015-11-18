import uuid

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstname = models.CharField(_('First Name'), max_length=55)
    lastname = models.CharField(_('Last Name'), max_length=55)
    date_of_birth = models.DateField(_('Date of Birth'))
    zip_code = models.CharField(_('Zip Code'), max_length=55)

    def __str__(self):
        return " ".join((self.firstname, self.lastname))

    def get_absolute_url(self):
        return reverse('customers:detail', kwargs={'pk': self.pk})
