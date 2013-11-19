# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Twitter.ftv'
        db.delete_column(u'congress_app_twitter', 'ftv')


    def backwards(self, orm):
        # Adding field 'Twitter.ftv'
        db.add_column(u'congress_app_twitter', 'ftv',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


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
            'politician': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['congress_app.Politician']"}),
            'user_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'congress_app.twitter_ftv': {
            'Meta': {'object_name': 'Twitter_FTV', '_ormbases': [u'congress_app.Twitter']},
            u'twitter_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['congress_app.Twitter']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['congress_app']