from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.template import RequestContext
from django.views.generic import TemplateView
from django.shortcuts import render_to_response, get_object_or_404, redirect
from apps.installation.models import Port, Ship, Icebreaker, MilitaryEquipment
from django.views.generic.base import View
from apps.installation.forms import PortForm, ShipForm, IcebreakerForm, MilitaryEquipmentForm


class BasePageView(TemplateView):
    model = None

    @staticmethod
    def get_all_data(model):
        data = []
        for obj in model.objects.all():
            data.append({
                'name': obj.name,
                'id': obj.id,
                'picture_url': obj.get_picture_url()
            })
        return data

    def get_context_data(self, **kwargs):
        model = kwargs.get('model')
        if not model:
            raise Exception(u'Model not found')
        return {model.urlstr(): self.get_all_data(model)}

    def get(self, request, *args, **kwargs):
        return render_to_response(self.template_name,
                                  self.get_context_data(model=self.model),
                                  context_instance=RequestContext(request))


class PortsPageView(BasePageView):
    template_name = 'installation/ports.html'
    model = Port


class ShipsPageView(BasePageView):
    template_name = 'installation/ships.html'
    model = Ship


class IcebreakersPageView(BasePageView):
    template_name = 'installation/icebreakers.html'
    model = Icebreaker


class MilitaryEquipmentsPageView(BasePageView):
    template_name = 'installation/equipments.html'
    model = MilitaryEquipment


ports_page_view = PortsPageView.as_view()
ships_page_view = ShipsPageView.as_view()
icebreakers_page_view = IcebreakersPageView.as_view()
equipments_page_view = MilitaryEquipmentsPageView.as_view()


def get_model_by_url(url):
    if url == 'ports':
        return Port
    if url == 'ships':
        return Ship
    if url == 'icebreakers':
        return Icebreaker
    if url == 'equipments':
        return MilitaryEquipment
    return None


class BaseView(TemplateView):
    form_class = None
    template_name = None
    redirect_url = None

    class Action(object):
        SAVE = 'save'
        DELETE = 'delete'

    def get_context_data(self, **kwargs):
        instance = kwargs['instance']
        return {'form': self.form_class(instance=instance),
                'picture_url': '/static/img/default.jpg' if instance is None else instance.get_picture_url(),
                'id': 0 if instance is None else instance.id}

    def get(self, request, *args, **kwargs):
        sid = int(kwargs.get('sid'))
        if not sid:
            return render_to_response(self.template_name,
                                      self.get_context_data(instance=None),
                                      context_instance=RequestContext(request))

        model = get_model_by_url(kwargs.get('url'))
        obj = model.objects.get(id=sid)
        if obj is None:
            raise Exception(u'port with id = %s do not exists' % str(sid))

        return render_to_response(self.template_name,
                                  self.get_context_data(instance=obj),
                                  context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        sid = int(request.POST['id'])
        instance = None
        if sid:
            instance = get_object_or_404(get_model_by_url(kwargs.get('url')), id=sid)

        if kwargs.get('action') == self.Action.DELETE:
            if instance:
                instance.delete()
            return redirect(reverse('installation:' + self.redirect_url))

        form = self.form_class(request.POST, instance=instance)
        if form.is_valid():
            if kwargs.get('action') == self.Action.SAVE:
                form.save()
            else:
                raise Exception(u'Don\'t know action %s' % kwargs.get('action'))

            return redirect(reverse('installation:' + self.redirect_url))

        return render_to_response(self.template_name,
                                  {'form': form,
                                   'picture_url': '' if instance is None else instance.get_picture_url(),
                                   'id': 0 if instance is None else instance.id},
                                  context_instance=RequestContext(request))


class PortPageView(BaseView):
    template_name = 'installation/port.html'
    form_class = PortForm
    redirect_url = 'ports-page-view'


class ShipPageView(BaseView):
    template_name = 'installation/ship.html'
    form_class = ShipForm
    redirect_url = 'ships-page-view'


class IcebreakerPageView(BaseView):
    template_name = 'installation/icebreaker.html'
    form_class = IcebreakerForm
    redirect_url = 'icebreakers-page-view'


class MilitaryEquipmentPageView(BaseView):
    template_name = 'installation/equipment.html'
    form_class = MilitaryEquipmentForm
    redirect_url = 'equipments-page-view'


port_page_view = PortPageView.as_view()
ship_page_view = ShipPageView.as_view()
icebreaker_page_view = IcebreakerPageView.as_view()
equipment_page_view = MilitaryEquipmentPageView.as_view()
