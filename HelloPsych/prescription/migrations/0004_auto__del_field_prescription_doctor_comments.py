# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'prescription.doctor_comments'
        db.delete_column(u'prescription_prescription', 'doctor_comments')


    def backwards(self, orm):
        # Adding field 'prescription.doctor_comments'
        db.add_column(u'prescription_prescription', 'doctor_comments',
                      self.gf('django.db.models.fields.TextField')(default='NULL', max_length=200, blank=True),
                      keep_default=False)


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'docview.request_call': {
            'Meta': {'object_name': 'request_call'},
            'acknowledged': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'calldone': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'callinprogress': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'callpending': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date_booked': ('django.db.models.fields.DateField', [], {}),
            'doc': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['login.doctor']"}),
            'dts': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_tim': ('django.db.models.fields.TimeField', [], {'default': "'12:15:00'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['login.patient']"}),
            'prescription_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'start_tim': ('django.db.models.fields.TimeField', [], {'default': "'12:00:00'"})
        },
        u'login.doctor': {
            'Meta': {'object_name': 'doctor'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'consultation_fee': ('django.db.models.fields.IntegerField', [], {'default': '9'}),
            'credits': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'current_job': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'expertise': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'memberships': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'others': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pg_college': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pg_council': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pg_degree': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pg_regno': ('django.db.models.fields.BigIntegerField', [], {'max_length': '50'}),
            'pg_year': ('django.db.models.fields.IntegerField', [], {}),
            'phone_no': ('django.db.models.fields.BigIntegerField', [], {'blank': 'True'}),
            'pref_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'prev_exp': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'projects': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'propic': ('django.db.models.fields.files.ImageField', [], {'default': "'static/propics/a.jpg'", 'max_length': '100'}),
            'ug_college': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'ug_council': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'ug_degree': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'ug_regno': ('django.db.models.fields.BigIntegerField', [], {}),
            'ug_year': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'login.patient': {
            'Meta': {'object_name': 'patient'},
            'age': ('django.db.models.fields.IntegerField', [], {}),
            'concern': ('django.db.models.fields.CharField', [], {'default': "'NULL'", 'max_length': '20'}),
            'credits': ('django.db.models.fields.IntegerField', [], {'default': '20'}),
            'first_call': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "'FirstName'", 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'default': "'LastName'", 'max_length': '50'}),
            'marital_status': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'propic': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'prescription.brand': {
            'Meta': {'object_name': 'brand'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prescription.generic']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '500'}),
            'qty': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'unit': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '50'})
        },
        u'prescription.dosage': {
            'Meta': {'object_name': 'dosage'},
            'comment': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'frequency': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'generic': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prescription.generic']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'prescription.generic': {
            'Meta': {'object_name': 'generic'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '500'})
        },
        u'prescription.prescription': {
            'Meta': {'object_name': 'prescription'},
            'appointment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prescribed_for'", 'to': u"orm['docview.request_call']"}),
            'concern': ('django.db.models.fields.TextField', [], {'max_length': '280'}),
            'doc': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'presc_doc'", 'to': u"orm['login.doctor']"}),
            'dts': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medicines': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['prescription.dosage']", 'null': 'True', 'blank': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'presc_pat'", 'to': u"orm['login.patient']"}),
            'symptoms': ('django.db.models.fields.TextField', [], {'default': "''"})
        }
    }

    complete_apps = ['prescription']