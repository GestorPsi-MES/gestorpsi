# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MaritalStatus'
        db.create_table('person_maritalstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('person', ['MaritalStatus'])

        # Adding model 'Person'
        db.create_table('person_person', (
            ('id', self.gf('gestorpsi.util.uuid_field.UuidField')(max_length=36, primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('photo', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('birthDate', self.gf('django.db.models.fields.DateField')(null=True)),
            ('birthPlace', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['address.City'], null=True)),
            ('birthDateSupposed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('maritalStatus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['person.MaritalStatus'], null=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('salary', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=7, decimal_places=2)),
            ('birthForeignCity', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('birthForeignState', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('birthForeignCountry', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True)),
        ))
        db.send_create_signal('person', ['Person'])

        # Adding M2M table for field organization on 'Person'
        db.create_table('person_person_organization', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm['person.person'], null=False)),
            ('organization', models.ForeignKey(orm['organization.organization'], null=False))
        ))
        db.create_unique('person_person_organization', ['person_id', 'organization_id'])

        # Adding model 'CompanyClient'
        db.create_table('person_companyclient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['client.Client'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['person.Company'])),
            ('responsible', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('person', ['CompanyClient'])

        # Adding unique constraint on 'CompanyClient', fields ['client', 'company']
        db.create_unique('person_companyclient', ['client_id', 'company_id'])

        # Adding model 'Company'
        db.create_table('person_company', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['person.Person'], unique=True, null=True, blank=True)),
            ('size', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('cnae_class', self.gf('django.db.models.fields.CharField')(max_length=9, null=True, blank=True)),
        ))
        db.send_create_signal('person', ['Company'])


    def backwards(self, orm):
        # Removing unique constraint on 'CompanyClient', fields ['client', 'company']
        db.delete_unique('person_companyclient', ['client_id', 'company_id'])

        # Deleting model 'MaritalStatus'
        db.delete_table('person_maritalstatus')

        # Deleting model 'Person'
        db.delete_table('person_person')

        # Removing M2M table for field organization on 'Person'
        db.delete_table('person_person_organization')

        # Deleting model 'CompanyClient'
        db.delete_table('person_companyclient')

        # Deleting model 'Company'
        db.delete_table('person_company')


    models = {
        'address.address': {
            'Meta': {'object_name': 'Address'},
            'addressLine1': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'addressLine2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'addressNumber': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'addressPrefix': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'addressType': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['address.AddressType']"}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['address.City']", 'null': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'foreignCity': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'foreignCountry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['address.Country']", 'null': 'True'}),
            'foreignState': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'id': ('gestorpsi.util.uuid_field.UuidField', [], {'max_length': '36', 'primary_key': 'True'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'zipCode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        'address.addresstype': {
            'Meta': {'ordering': "['weight']", 'object_name': 'AddressType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'address.city': {
            'Meta': {'ordering': "['name']", 'object_name': 'City'},
            'ibge_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['address.State']"})
        },
        'address.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nationality': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'address.state': {
            'Meta': {'ordering': "['name']", 'object_name': 'State'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['address.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'shortName': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'client.client': {
            'Meta': {'ordering': "['person']", 'object_name': 'Client'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'admission_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('gestorpsi.util.uuid_field.UuidField', [], {'max_length': '36', 'primary_key': 'True'}),
            'idRecord': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'legacyRecord': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'payment_condition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['client.PaymentCondition']"}),
            'person': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['person.Person']", 'unique': 'True'})
        },
        'client.paymentcondition': {
            'Meta': {'object_name': 'PaymentCondition'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_condition': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'value_for_payment': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '7', 'decimal_places': '2'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'document.document': {
            'Meta': {'object_name': 'Document'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'document': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('gestorpsi.util.uuid_field.UuidField', [], {'max_length': '36', 'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['document.Issuer']", 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['address.State']", 'null': 'True', 'blank': 'True'}),
            'typeDocument': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['document.TypeDocument']"})
        },
        'document.issuer': {
            'Meta': {'ordering': "['description']", 'object_name': 'Issuer'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'document.typedocument': {
            'Meta': {'ordering': "['description']", 'object_name': 'TypeDocument'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'gcm.paymenttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'PaymentType'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'detail': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'show_to_client': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'time': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'gcm.plan': {
            'Meta': {'ordering': "['weight']", 'object_name': 'Plan'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pagseguro_code': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'staff_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'visible_client': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
        },
        'internet.email': {
            'Meta': {'object_name': 'Email'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'email_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['internet.EmailType']"}),
            'id': ('gestorpsi.util.uuid_field.UuidField', [], {'max_length': '36', 'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '36'})
        },
        'internet.emailtype': {
            'Meta': {'ordering': "['description']", 'object_name': 'EmailType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'internet.imnetwork': {
            'Meta': {'ordering': "['description']", 'object_name': 'IMNetwork'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'internet.instantmessenger': {
            'Meta': {'object_name': 'InstantMessenger'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('gestorpsi.util.uuid_field.UuidField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['internet.IMNetwork']", 'blank': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '36'})
        },
        'internet.site': {
            'Meta': {'object_name': 'Site'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('gestorpsi.util.uuid_field.UuidField', [], {'max_length': '36', 'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'site': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'organization.activitie': {
            'Meta': {'ordering': "['description']", 'object_name': 'Activitie'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'organization.administrationenvironment': {
            'Meta': {'ordering': "['description']", 'object_name': 'AdministrationEnvironment'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'organization.dependence': {
            'Meta': {'ordering': "['description']", 'object_name': 'Dependence'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'organization.management': {
            'Meta': {'ordering': "['description']", 'object_name': 'Management'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'organization.organization': {
            'Meta': {'ordering': "['name']", 'object_name': 'Organization'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.Activitie']", 'null': 'True', 'blank': 'True'}),
            'city_inscription': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'cnes': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'contact_owner': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'contact_owner'", 'null': 'True', 'blank': 'True', 'to': "orm['person.Person']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'default_payment_day': ('django.db.models.fields.PositiveIntegerField', [], {'default': '10'}),
            'dependence': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.Dependence']", 'null': 'True', 'blank': 'True'}),
            'employee_number': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'environment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.AdministrationEnvironment']", 'null': 'True', 'blank': 'True'}),
            'id': ('gestorpsi.util.uuid_field.UuidField', [], {'max_length': '36', 'primary_key': 'True'}),
            'last_id_record': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'management': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.Management']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'organization_related'", 'null': 'True', 'to': "orm['organization.Organization']"}),
            'payment_detail': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'payment_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gcm.PaymentType']", 'null': 'True', 'blank': 'True'}),
            'person_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.PersonType']", 'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'prefered_plan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gcm.Plan']", 'null': 'True', 'blank': 'True'}),
            'provided_type': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['organization.ProvidedType']", 'null': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'register_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'restrict_schedule': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.Source']", 'null': 'True', 'blank': 'True'}),
            'state_inscription': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'suspension': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'suspension_reason': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'time_slot_schedule': ('django.db.models.fields.CharField', [], {'default': '30', 'max_length': '2'}),
            'trade_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'unit_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.UnitType']", 'null': 'True', 'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'organization.persontype': {
            'Meta': {'ordering': "['description']", 'object_name': 'PersonType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'organization.providedtype': {
            'Meta': {'ordering': "['description']", 'object_name': 'ProvidedType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'organization.source': {
            'Meta': {'ordering': "['description']", 'object_name': 'Source'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'organization.unittype': {
            'Meta': {'ordering': "['description']", 'object_name': 'UnitType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'person.company': {
            'Meta': {'object_name': 'Company'},
            'client': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['client.Client']", 'symmetrical': 'False', 'through': "orm['person.CompanyClient']", 'blank': 'True'}),
            'cnae_class': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['person.Person']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'person.companyclient': {
            'Meta': {'ordering': "['-active', '-responsible', 'client']", 'unique_together': "(('client', 'company'),)", 'object_name': 'CompanyClient'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['client.Client']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['person.Company']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'responsible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'person.maritalstatus': {
            'Meta': {'ordering': "['description']", 'object_name': 'MaritalStatus'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'person.person': {
            'Meta': {'ordering': "['name']", 'object_name': 'Person'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'birthDate': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'birthDateSupposed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'birthForeignCity': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'birthForeignCountry': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True'}),
            'birthForeignState': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'birthPlace': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['address.City']", 'null': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('gestorpsi.util.uuid_field.UuidField', [], {'max_length': '36', 'primary_key': 'True'}),
            'maritalStatus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['person.MaritalStatus']", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['organization.Organization']", 'symmetrical': 'False'}),
            'photo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'salary': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '7', 'decimal_places': '2'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['auth.User']"})
        },
        'phone.phone': {
            'Meta': {'object_name': 'Phone'},
            'area': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'ext': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'id': ('gestorpsi.util.uuid_field.UuidField', [], {'max_length': '36', 'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'phoneNumber': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'phoneType': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phone.PhoneType']"})
        },
        'phone.phonetype': {
            'Meta': {'ordering': "['description']", 'object_name': 'PhoneType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['person']