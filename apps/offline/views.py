# coding=utf-8
from apps.calculation.views import CalculationPageView
from django.shortcuts import render
from django.template import RequestContext
from django.views.generic import View, FormView, TemplateView
from django.shortcuts import render_to_response


class OfflineCalculationPageView(CalculationPageView):
    template_name = 'home.html'

offline_calculation = OfflineCalculationPageView.as_view()
