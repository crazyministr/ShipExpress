# coding=utf-8
from django.shortcuts import render
from django.template import RequestContext
from django.views.generic import View, FormView, TemplateView
from django.shortcuts import render_to_response


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        return render_to_response(self.template_name,
                                  self.get_context_data(),
                                  context_instance=RequestContext(request))

home = HomePageView.as_view()
