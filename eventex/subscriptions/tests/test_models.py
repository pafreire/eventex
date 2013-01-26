# coding utf-8
from django.test import TestCase
from django.db import IntegrityError
from datetime import datetime
from eventex.subscriptions.models import Subscription


class SubscriptionTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
	    name  = 'Alvares de Azevedo',
	    cpf   = '12345678901',
            email = 'alvedo@poetas.com', 
            phone = '2155555555',
	)

    def test_create(self):
	# Subscription must have name, cpf, email, phone
	self.obj.save()
	self.assertEqual(1, self.obj.id)

    def test_has_created_at(self):
        # Subscription must have automatic created_at
	self.obj.save()
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_unicode(self):
	self.assertEqual(u'Alvares de Azevedo', unicode(self.obj))


class SubscriptionUniqueTest(TestCase):
    def setUp(self):
        # Create a first entry to force the colision
	Subscription.objects.create(name='Peloponeso de Oliveira', cpf='12345678901',
			            email='pelopo@grecia.com', phone='88-5555-5555')

    def test_cpf_unique(self):
        "CPF must unique"
	s = Subscription(name='Gupta Samahandra', cpf='12345678901',
			 email='guptas@Hindustao.com', phone='91-3333-3333')
	self.assertRaises(IntegrityError, s.save)

    def test_email_unique(self):
        "Email must unique"
	s = Subscription(name='Gupta Samahandra', cpf='12345678909',
			 email='pelopo@grecia.com', phone='91-3333-3333')
	self.assertRaises(IntegrityError, s.save)

