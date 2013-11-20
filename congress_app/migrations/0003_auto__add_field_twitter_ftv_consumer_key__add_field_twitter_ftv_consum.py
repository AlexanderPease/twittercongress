# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Twitter_FTV.consumer_key'
        db.add_column(u'congress_app_twitter_ftv', 'consumer_key',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Twitter_FTV.consumer_secret'
        db.add_column(u'congress_app_twitter_ftv', 'consumer_secret',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Twitter_FTV.consumer_key'
        db.delete_column(u'congress_app_twitter_ftv', 'consumer_key')

        # Deleting field 'Twitter_FTV.consumer_secret'
        db.delete_column(u'congress_app_twitter_ftv', 'consumer_secret')


    models = {
        u'congress_app.politician': {
            'Meta': {'object_name': 'Politician'},
            'district': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'party': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'portrait_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'congress_app.twitter': {
            'Meta': {'object_name': 'Twitter'},
            'handle': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'politician': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['congress_app.Politician']", 'unique': 'True'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'congress_app.twitter_ftv': {
            'Meta': {'object_name': 'Twitter_FTV'},
            'consumer_key': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'consumer_secret': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'handle': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'politician': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['congress_app.Politician']", 'unique': 'True'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['congress_app']