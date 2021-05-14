import logging

from django.http import HttpResponse
from django.shortcuts import render


logger = logging.getLogger(__name__)


def index(request):
    logger.info("hello world!")
    logger.warning("shit!")
    return HttpResponse('ok')
    # return render(request, 'portfolio/index.html')


from django.views.generic import TemplateView
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
