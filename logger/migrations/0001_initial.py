# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Car'
        db.create_table(u'logger_car', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('date_purchased', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('initial_cost', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('mileage', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'logger', ['Car'])

        # Adding model 'Entry'
        db.create_table(u'logger_entry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('car', self.gf('django.db.models.fields.related.ForeignKey')(related_name='car', to=orm['logger.Car'])),
            ('mileage', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('service_type', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('service_location', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('contact_name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('contact_number', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('cost_of_parts', self.gf('django.db.models.fields.IntegerField')()),
            ('cost_of_service', self.gf('django.db.models.fields.IntegerField')()),
            ('comments', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'logger', ['Entry'])


    def backwards(self, orm):
        # Deleting model 'Car'
        db.delete_table(u'logger_car')

        # Deleting model 'Entry'
        db.delete_table(u'logger_entry')


    models = {
        u'logger.car': {
            'Meta': {'object_name': 'Car'},
            'date_purchased': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_cost': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'mileage': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'logger.entry': {
            'Meta': {'object_name': 'Entry'},
            'car': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'car'", 'to': u"orm['logger.Car']"}),
            'comments': ('django.db.models.fields.TextField', [], {}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'contact_number': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'cost_of_parts': ('django.db.models.fields.IntegerField', [], {}),
            'cost_of_service': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mileage': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'service_location': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'service_type': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['logger']