# -*- coding: utf-8 -*-

"""
Copyright (C) 2008 GestorPsi

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator
from django.utils import simplejson
from django.db.models import Q
from django.utils.translation import ugettext as _
from gestorpsi.device.models import DeviceDetails, Device
from gestorpsi.careprofessional.views import Profession
from gestorpsi.place.models import Place, Room
from gestorpsi.util.decorators import permission_required_with_403

@permission_required_with_403('device.device_list')
def index(request):
    """
    Returns details about all currently existing devices.
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    """
    return render_to_response( "device/device_list.html", context_instance=RequestContext(request))


@permission_required_with_403('device.device_list')
def list(request, page = 1):
    user = request.user
    object = DeviceDetails.objects.filter(device__organization=request.user.get_profile().org_active)
    
    object_length = len(object)
    paginator = Paginator(object, settings.PAGE_RESULTS)
    object = paginator.page(page)

    array = {} #json
    i = 0

    array['util'] = {
        'has_perm_read': user.has_perm('device.device_read'),
        'paginator_has_previous': object.has_previous().real,
        'paginator_has_next': object.has_next().real,
        'paginator_previous_page_number': object.previous_page_number().real,
        'paginator_next_page_number': object.next_page_number().real,
        'paginator_actual_page': object.number,
        'paginator_num_pages': paginator.num_pages,
        'object_length': object_length,
    }

    
    array['paginator'] = {}
    for p in paginator.page_range:
        array['paginator'][p] = p
    
    for o in object.object_list:
        array[i] = {
            'id': o.id,
            'name': o.brand,
            'model': o.model,
            'type': o.device.description,
        }
        i = i + 1

    return HttpResponse(simplejson.dumps(array), mimetype='application/json')

@permission_required_with_403('device.device_list')
def list_types(request, page = 1):
    user = request.user
    object = Device.objects.filter(organization=user.get_profile().org_active)
    
    object_length = len(object)
    paginator = Paginator(object, settings.PAGE_RESULTS)
    object = paginator.page(page)

    array = {} #json
    i = 0

    array['util'] = {
        'has_perm_read': user.has_perm('device.device_read'),
        'paginator_has_previous': object.has_previous().real,
        'paginator_has_next': object.has_next().real,
        'paginator_previous_page_number': object.previous_page_number().real,
        'paginator_next_page_number': object.next_page_number().real,
        'paginator_actual_page': object.number,
        'paginator_num_pages': paginator.num_pages,
        'object_length': object_length,
    }

    
    array['paginator'] = {}
    for p in paginator.page_range:
        array['paginator'][p] = p
    
    for o in object.object_list:
        array[i] = {
            'id': o.id,
            'name': o.description,
        }
        i = i + 1

    return HttpResponse(simplejson.dumps(array), mimetype='application/json')


@permission_required_with_403('device.device_read')
def form(request, object_id= ''):
    user = request.user
    try:
        object = get_object_or_404( DeviceDetails, pk= object_id )
    except Http404:
        object= DeviceDetails()
    return render_to_response('device/device_form.html', {
                                                          'object': object,  
                                                          'device_type': Device.objects.filter(organization=user.get_profile().org_active),
                                                          'places': Place.objects.filter(organization=user.get_profile().org_active.id),                                                          
                                                          'PROFESSIONAL_AREAS': Profession.objects.all(), },
                                                          context_instance=RequestContext(request))


@permission_required_with_403('device.device_list')
def index_type(request):
    return render_to_response( "device/device_type_list.html", 
        #{'object': Device.objects.filter(organization=user.get_profile().org_active), }, 
        context_instance=RequestContext(request))

@permission_required_with_403('device.device_read')
def form_type(request, object_id= ''):
    return render_to_response('device/device_type_form.html', {'object': get_object_or_404( Device, pk=object_id) }, context_instance=RequestContext(request) )

@permission_required_with_403('device.device_write')
def save_device(request, object_id= ''):
    try:
        device= get_object_or_404( Device, pk=object_id)
    except Http404:
        device = Device()

    user = request.user
    device.description = request.POST.get('label')
    device.organization = user.get_profile().org_active
    device.save()
    request.user.message_set.create(message=_('Device type saved successfully'))

    return HttpResponseRedirect('/device/type/%s/' % device.id)

@permission_required_with_403('device.device_write')
def save(request, object_id='' ):
    """
    This function view creates an instance of the class C{DeviceDetails} with id equals to I{object_id} and
    uses the I{request} object to set the newly created class attributes. If there is some C{DeviceDetails}
    with id equals to I{object_id} then this instance is updated with the I{request} information.
    @param request: this is a request sent by the browser.
    @type request: an instance of the class C{HttpRequest} created by the framework Django.
    @param object_id: the id of the C{DeviceDetails} instance to be saved or updated.
    @type object_id: an instance of the built-in class c{int}.
    """
    
    try:
        device_details= get_object_or_404( DeviceDetails, pk=object_id)
    except Http404:
        device_details = DeviceDetails()

    device_details.device = get_object_or_404(Device, pk=request.POST.get('select_device'))
    device_details.brand = request.POST.get('brand')
    device_details.model = request.POST.get('model')
    device_details.part_number = request.POST.get('part_number')
    device_details.comments = request.POST.get('comments')
    device_details.lendable = get_visible(request, request.POST.get('lendable'))
    device_details.device = get_object_or_404(Device, pk=request.POST.get('select_device'))
    
    """ Device Durability """
    device_details.durability = request.POST.get('select_durability_type')

    """ Device Restriction """
    if request.POST['select_restriction_type'] == '2':
        device_details.prof_restriction = Profession.objects.get(pk = request.POST.get('professional_area'))

    """ Device Mobility """
    mobility = request.POST.get('select_mobility_type')
    device_details.mobility = mobility
    device_details.place = get_object_or_404(Place, pk=request.POST.get('place_associated'))
    device_details.room = get_object_or_404(Room, pk=request.POST.get('room_associated'))
    device_details.save()

    request.user.message_set.create(message=_('Device saved successfully'))

    return HttpResponseRedirect('/device/%s/' % device_details.id)

@permission_required_with_403('device.device_read')
def get_visible(request, value):
    if (value == 'on'):
        return True
    else:
        return False
     
@permission_required_with_403('device.device_write')
def delete(request, object_id= ''):
    pass

def list_device(request, object_id):

    array = {} # JSON
    devices_from_room = DeviceDetails.objects.filter(room = object_id)  # ALL FIXED DEVICES FROM THE ROOM
    list = DeviceDetails.objects.filter(Q(room = object_id) | Q(lendable=True) | Q(room = object_id, mobility="2"))

    c = 0
    for device in list:
        array[c] = {
            'id': device.id,
            'name': '%s' % device,
        }
        c = c + 1

    return HttpResponse(simplejson.dumps(array), mimetype='application/json')


def order(request, object_id = ''):
    object = DeviceDetails.objects.get(pk = object_id)

    if object.active == True:
        object.active = False
    else:
        object.active = True

    object.save(force_update = True)
    return HttpResponseRedirect('/device/%s/' % object.id)
