# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Car.mileage'
        db.add_column(u'logger_car', 'mileage',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Car.mileage'
        db.delete_column(u'logger_car', 'mileage')


    models = {
        u'logger.car': {
            'Meta': {'object_name': 'Car'},
            'date_purchased': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_cost': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'initial_mileage': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'mileage': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'logger.entry': {
            'Meta': {'object_name': 'Entry'},
            'car': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'car'", 'to': u"orm['logger.Car']"}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'contact_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'cost_of_parts': ('django.db.models.fields.IntegerField', [], {}),
            'cost_of_service': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mileage': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'service_location': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'service_type': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['logger']