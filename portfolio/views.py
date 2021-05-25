import logging

from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'portfolio/index.html')


from django.views.generic import TemplateView, FormView
from chartjs.views.lines import BaseLineChartView


class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Central", "Eastside", "Westside"]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [[75, 44, 92, 11, 44],
                [41, 92, 18, 3, 73],
                [87, 21, 94, 3, 90]]


line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()

class CalculatorResultView(TemplateView):
    http_method_names = ['get']
    template_name = "portfolio/calculator_result.html"

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'result': kwargs['result']
        }

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CalculatorForm(forms.Form):
    risk = forms.FloatField(
        min_value=0,
        help_text='Possible loss over our capital, '
                  'should be 1% so that we can make 50 lost '
                  'trades and still have half money.'
    )
    buy_price = forms.IntegerField(
        min_value=0,
        help_text="in vnd",
    )
    stop_loss = forms.IntegerField(
        min_value=0,
        help_text="in vnd",
    )
    trading_fee = forms.IntegerField(
        min_value=0,
        help_text="in vnd",
    )


class CalculatorView(FormView):
    http_method_names = ['get', 'post']
    template_name = "portfolio/calculator.html"
    form_class = CalculatorForm

    def form_valid(self, form: CalculatorForm):
        logger.info(form.cleaned_data)
        # todo: computation here
        return redirect(to=reverse_lazy('homie_admin:calculator_result', kwargs={
            'result': 10
        }))
