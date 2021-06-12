from django.views.generic import TemplateView


class ExpenseReportView(TemplateView):
    template_name = "money/expense_report.html"
