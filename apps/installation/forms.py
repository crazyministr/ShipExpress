# -*- coding: utf-8 -*-
from django import forms
from apps.installation.models import Port, Ship, Icebreaker, MilitaryEquipment


class PortForm(forms.ModelForm):
    class Meta:
        model = Port
        fields = '__all__'
        exclude = ['picture']


class ShipForm(forms.ModelForm):
    class Meta:
        model = Ship
        fields = '__all__'
        exclude = ['picture']


class IcebreakerForm(forms.ModelForm):
    class Meta:
        model = Icebreaker
        fields = '__all__'
        exclude = ['picture']


class MilitaryEquipmentForm(forms.ModelForm):
    class Meta:
        model = MilitaryEquipment
        fields = '__all__'
        exclude = ['picture']
