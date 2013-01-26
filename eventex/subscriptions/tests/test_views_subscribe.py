# coding: utf-8
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription

class SubscribeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/inscricao/')

    def test_get(self):
	'Get /inscricao/ must return status code 200.'
	self.assertEqual(200, self.resp.status_code)
    
    def test_template(self):
	'Response should be a rendered template'
	self.assertTemplateUsed(self.resp,
			        'subscriptions/subscription_form.html')
    
    def test_html(self):
	"Html must contain input controls."
	self.assertContains(self.resp, '<form')
	self.assertContains(self.resp, '<input', 6)
	self.assertContains(self.resp, 'type="text"', 4)
	self.assertContains(self.resp, 'type="submit"')
    
    def test_csrf(self):
        "Html must contain csrf token."
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
	"Context must have the subscription form."
	form = self.resp.context['form']
	self.assertIsInstance(form, SubscriptionForm)

class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name='João do Rio', cpf='12332178901',
	                email='joao@rio.com', phone='21-2121-2121')
        self.resp = self.client.post('/inscricao/', data)

    def test_post(self):
        'Valid POST should redirect to /inscricao/1/'
        self.assertEqual(302, self.resp.status_code)

    def test_save(self):
        'Valid POST must be saved.'
        self.assertTrue(Subscription.objects.exists())

class SubscribeInvalidPostTest(TestCase):
    def setUp(self):
        data = dict(name='Vlahdimir Xablau', cpf='0000000000013',
                    email='vlah@xa.com', phone='21-3333-4444')
        self.resp = self.client.post('/inscricao/', data)

    def test_post(self):
        'Invalid POST should not redirect.'
        self.assertEqual(200, self.resp.status_code)
