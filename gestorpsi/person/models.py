from django.db import models
from django.contrib.contenttypes import generic
from gestorpsi.phone.models import Phone
from gestorpsi.address.models import Country, City, Address
from gestorpsi.document.models import Document
from gestorpsi.internet.models import Email, Site, InstantMessenger

class Gender(models.Model):
    description = models.CharField(max_length=15)
    def __unicode__(self):
        return u"%s" % self.description
    class Admin: pass

class MaritalStatus(models.Model):
    description = models.CharField(max_length=20)
    def __unicode__(self):
        return u"%s" % self.description
    class Admin: pass

class Person(models.Model):
    name = models.CharField('Name', max_length=60)
    #lastName = models.CharField('Name', max_length=30)
    nickname = models.CharField('Nickname', max_length=20, null=True)
    photo = models.ImageField('Photo', upload_to="client_photos", null=True)
    birthDate = models.DateField('Birthdate', null=True)
    birthPlace = models.ForeignKey(City, null=True)
    gender = models.ForeignKey(Gender, null=True)
    maritalStatus = models.ForeignKey(MaritalStatus, null=True)   
    # Reduntante pois ja temos birthPlace
    # nationality = models.ForeignKey(Country)
    active = models.BooleanField(default=True)
    
    phones = generic.GenericRelation(Phone, null=True)
    address = generic.GenericRelation(Address, null=True)
    document = generic.GenericRelation(Document, null=True)
    emails  = generic.GenericRelation(Email, null=True)
    sites = generic.GenericRelation(Site, null=True)
    instantMessengers =generic.GenericRelation(InstantMessenger, null=True)
    def __unicode__(self):
        return u"%s" % self.name
    class Meta:
        ordering = ['name']
        
"""
Teste do Models no shell de Pessoa e suas ligacoes

from gestorpsi.person.models import Person, MaritalStatus, Gender
from gestorpsi.phone.models import PhoneType, Phone
from gestorpsi.address.models import Address, AddressType, City, Country, State
from gestorpsi.document.models import Document, Issuer
from gestorpsi.internet.models import Email, Site, InstantMessenger, IMNetwork

p = Person()
#p.firstName = "Fulano"
#p.lastName = "da Silva"
p.firstName = "Fulano da Silva"
p.nickname = "Fulaninho"
p.birthPlace = City.objects.get(pk=44085)
p.gender = Gender.objects.get(pk=1)
p.maritalStatus = MaritalStatus.objects.get(pk=1)
p.nationality = Country.objects.get(pk=33)
p.save()

p.phones.create(area='11',phoneNumber='33442211',ext='123',phoneType=PhoneType.objects.get(pk=1))
p.phones.create(area='11',phoneNumber='98761234',ext='',phoneType=PhoneType.objects.get(pk=2))

address = Address()
address.addressPrefix = "Rua"
address.addressLine1 = "Rui Barbosa, 1234"
address.addressLine2 = "Anexo II - Sala 4"
address.neighborhood = "Centro"
address.zipCode = "12345-123"
address.addressType = AddressType.objects.get(pk=1)
address.city = City.objects.get(pk=44085)
address.content_object = p
address.save()

p.document.create(identityCard='23.232.232-2',issuer=Issuer.objects.get(pk=1),state=State.objects.get(pk=24),cpf='434.343.343-34')

p.emails.create(email='bla@uol.com.br')
p.emails.create(email='ble@uol.com.br')
p.emails.create(email='bli@uol.com.br')
p.emails.create(email='blo@uol.com.br')
p.emails.create(email='blu@uol.com.br')

p.sites.create(description='Meu site',site='http://www.uol.com.br')
p.sites.create(description='Meu blog',site='http://bla.blog.uol.com.br')
p.sites.create(description='Meu orkut',site='http://www.orkut.com/747463636')

p.instantMessengers.create(identity='7373234',network=IMNetwork.objects.get(pk=1))
"""