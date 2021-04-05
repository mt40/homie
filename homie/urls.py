from django.urls import include, path
from django.views.generic import RedirectView

from portfolio.admin import portfolio_admin_site

urlpatterns = [
    path('admin/', portfolio_admin_site.urls),
    path('', RedirectView.as_view(url='admin', permanent=True)),
    path('portfolio', include('portfolio.urls'))
]
