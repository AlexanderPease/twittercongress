# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Politician'
        db.create_table(u'congress_app_politician', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('twitter', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('district', self.gf('django.db.models.fields.IntegerField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('party', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'congress_app', ['Politician'])


    def backwards(self, orm):
        # Deleting model 'Politician'
        db.delete_table(u'congress_app_politician')


    models = {
        u'congress_app.politician': {
            'Meta': {'object_name': 'Politician'},
            'district': ('django.db.models.fields.IntegerField', [], {}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'party': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['congress_app']