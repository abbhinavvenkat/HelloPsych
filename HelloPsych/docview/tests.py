"""
    This file demonstrates writing tests using the unittest module. These will pass
    when you run "manage.py test".

    Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from login.models import patient, doctor
from docview.models import request_call
import math

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class Req_Call_Test(TestCase):
    def setUp(self):
        self.u1 = User.objects.create(username='user1')
        self.u2 = User.objects.create(username='user2')
        self.pat1 = patient.objects.create(user=self.u2, age="18", sex="M")
        self.doc1 = doctor.objects.create(user=self.u1, \
            address="36 China Town", phone_no=123456789, ug_year=2010, \
            ug_regno=1995, pg_year=2012, pg_regno=23123, pref_time="08:00:00")
        self.req1 = request_call.objects.create(patient=self.pat1, doc=self.doc1)

    def testUserDoctor(self):
        try:
            req1 = request_call.objects.get(patient=self.pat1, doc=self.doc1)
            self.assertEqual(req1.sent, self.req1.sent)
            self.assertEqual(req1.acknowledged, self.req1.acknowledged)
            self.assertEqual(req1.calldone, self.req1.calldone)
            self.assertEqual(req1.prescription_sent, self.req1.prescription_sent)
            self.assertEqual(False, self.req1.sent)
            self.assertEqual(False, self.req1.acknowledged)
            self.assertEqual(False, self.req1.calldone)
            self.assertEqual(False, self.req1.prescription_sent)
            self.assertEqual(req1.date_booked, self.req1.date_booked)
            span = req1.date_booked -  self.req1.date_booked;
            hours = math.floor(((span).seconds) / 3600)
            minutes = math.floor(((span).seconds) / 60)
            self.assertEqual(hours, 0.0)
            self.assertEqual(minutes, 0.0)
            self.assertEqual((span).seconds,0.0)
        except ObjectDoesNotExist:
            raise ObjectDoesNotError('Request_call object not found.')
            #print "request_call object was either not created or could not be extracted"
        
    def tearDown(self):
        self.req1.delete()  
        self.pat1.delete() 
        self.doc1.delete()
        self.u1.delete()
        self.u2.delete()

