from __future__ import absolute_import, unicode_literals

from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models.fields import Field, FieldDoesNotExist
from django.test import TestCase, skipIfDBFeature, skipUnlessDBFeature
from django.utils import six
from django.utils.translation import ugettext_lazy

from .models import Article
from django.db.utils import OptimisticLockingError


class ModelTest(TestCase):

    def test_locking_detect(self):
        # No articles are in the system yet.
        self.assertQuerysetEqual(Article.objects.all(), [])

        # Create an Article.
        a = Article(
            id=None,
            headline='Area man programs in Python',
            pub_date=datetime(2005, 7, 28),
        )

        # Save it into the database. You have to call save() explicitly.
        a.save()

        a1 = Article.objects.get()
        a2 = Article.objects.get()

        a1.save()
        self.assertRaises(OptimisticLockingError, a2.save)


    def test_lookup(self):
        # No articles are in the system yet.
        self.assertQuerysetEqual(Article.objects.all(), [])

        # Create an Article.
        a = Article(
            id=None,
            headline='Area man programs in Python',
            pub_date=datetime(2005, 7, 28),
        )

        # Save it into the database. You have to call save() explicitly.
        a.save()

        self.assertEqual(a.version, 1)
        self.assertEqual(Article.objects.get(pk=a.pk).version, 1)

        a.save()

        self.assertEqual(a.version, 2)
        self.assertEqual(Article.objects.get(pk=a.pk).version, 2)

        a.save()

        self.assertEqual(a.version, 3)
        self.assertEqual(Article.objects.get(pk=a.pk).version, 3)
