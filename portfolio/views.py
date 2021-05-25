import logging

import pydantic
from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from admin_site.const import UrlName
from portfolio.models import Holding

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


class CalculatorComputeResult(pydantic.BaseModel):
    # current situation
    fund: int
    risking_cash: int
    stop_loss_percent: float

    # suggestions
    suggested_buy_amount: int
    total_buy_value: int
    suggested_sell_prices: str


# todo: add constraints
class CalculatorResultForm(forms.Form):
    fund = forms.IntegerField(
        help_text=(
            'in vnd<br/>'
            'Available fund for buying'
        )
    )
    risking_cash = forms.IntegerField(
        help_text=(
            'in vnd<br/>'
            'The cash that we are risking in this '
            'transaction a.k.a our max possible loss.'
        )
    )
    stop_loss_percent = forms.FloatField(
        min_value=3,
        max_value=8,
        help_text=(
            'in vnd<br/>'
            'Percentage of the input stop loss. '
            'This is the diff between Stop Loss and Buy Price, '
            'should be <b>3% - 8%</b> only'
        )
    )
    suggested_buy_amount = forms.IntegerField()
    total_buy_value = forms.IntegerField(
        help_text='in vnd'
    )
    suggested_sell_prices = forms.CharField(
        help_text=(
            'in vnd<br/>'
            'Sell from <b>3R - 10R</b>, protect our profit, <b>DON’T BE GREEDY!</b>'
        )
    )


class CalculatorResultView(FormView):
    http_method_names = ['get']
    template_name = "portfolio/calculator_result.html"
    form_class = CalculatorResultForm

    def get_form(self, form_class=None):
        return self.get_form_class()(self.get_initial())

    def get_initial(self):
        fields = CalculatorComputeResult.schema()['properties'].keys()
        return {
            **super().get_initial(),
            **{
                field: self.kwargs[field]
                for field in fields
            }
        }


class CalculatorForm(forms.Form):
    risk = forms.FloatField(
        min_value=0,
        initial=1,
        help_text='Possible loss over our capital, '
                  'should be <b>1%</b> so that we can make 50 lost '
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
        result = self.compute(
            risk=float(form.cleaned_data['risk']),
            buy_price=int(form.cleaned_data['buy_price']),
            stop_loss=int(form.cleaned_data['stop_loss']),
            trading_fee=int(form.cleaned_data['trading_fee']),
        )

        return redirect(
            to=reverse_lazy(UrlName.CALCULATOR_RESULT.value, kwargs=result.dict())
        )

    # testme
    @staticmethod
    def compute(risk: float, buy_price: int, stop_loss: int, trading_fee: int) -> CalculatorComputeResult:
        fund = Holding.get_fund()
        risking_cash = fund * risk / 100
        loss = buy_price - stop_loss
        stop_loss_percent = loss / buy_price * 100
        amount = int((risking_cash - 2 * trading_fee) / loss)
        total_value = amount * buy_price
        sell_price_min = buy_price + loss * 3
        sell_price_max = buy_price + loss * 10

        return CalculatorComputeResult(
            fund=fund,
            risking_cash=risking_cash,
            stop_loss_percent=stop_loss_percent,
            suggested_buy_amount=amount,
            total_buy_value=total_value,
            suggested_sell_prices=f'{sell_price_min} - {sell_price_max}',
        )
