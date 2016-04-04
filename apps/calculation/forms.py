# coding: utf-8
from django.utils.safestring import mark_safe
from django.utils.html import format_html, format_html_join
from django import forms
from django.forms import Select
from django.forms.util import ErrorList
from apps.installation.models import Port, Ship, Icebreaker, MilitaryEquipment


class BaseForm(forms.Form):
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None,
                 error_class=ErrorList, label_suffix=None, empty_permitted=False):
        super(BaseForm, self).__init__(data, files, auto_id, prefix, initial, error_class,
                                       label_suffix, empty_permitted)

        ports = [(port.name, port.name) for port in Port.objects.all()]
        ships = [(ship.name, ship.name) for ship in Ship.objects.all()]
        icebreakers = [(icebreaker.name, icebreaker.name) for icebreaker in Icebreaker.objects.all()]
        equipments = [(equipment.name, equipment.name) for equipment in MilitaryEquipment.objects.all()]

        for name, field in self.fields.items():
            if name in ['start', 'finish', 'medium']:
                field.choices = ports
                field.initial = ports[0][0]
            elif name == 'ships':
                field.choices = ships
                field.initial = ships[0][0]
            elif name == 'icebreakers':
                field.choices = icebreakers
                field.initial = icebreakers[0][0]
            elif name == 'ice':
                field.initial = False
            elif name == 'equipments':
                field.choices = equipments
                field.initial = equipments[0][0]


class SelectMultipleWidget(Select):
    allow_multiple_selected = True

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        final_attrs = self.build_attrs(attrs, name=name)
        output = [format_html('<select style="height: 150px;" multiple="multiple"{0}>',
                              format_html_join('', ' {0}="{1}"', sorted(final_attrs.items())))]
        options = self.render_options(choices, value)
        if options:
            output.append(options)

        output.append('</select>')
        return mark_safe('\n'.join(output))


class CirculationDataForm(BaseForm):
    start = forms.ChoiceField()
    finish = forms.ChoiceField()
    # medium = forms.MultipleChoiceField(required=False, widget=SelectMultipleWidget)
    ships = forms.ChoiceField()
    ice = forms.BooleanField()
    icebreakers = forms.ChoiceField()
    equipments = forms.MultipleChoiceField(required=False, widget=SelectMultipleWidget)
