# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'doctor.credits'
        db.add_column(u'login_doctor', 'credits',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'doctor.credits'
        db.delete_column(u'login_doctor', 'credits')


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
        u'login.logs': {
            'Meta': {'object_name': 'logs'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login_time': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
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
        u'login.profileupdate': {
            'Meta': {'object_name': 'profileupdate'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'login.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'acc_type': ('django.db.models.fields.BooleanField', [], {}),
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '257'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_expires': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'verified': ('django.db.models.fields.BooleanField', [], {})
        }
    }

    complete_apps = ['login']