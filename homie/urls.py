import debug_toolbar
from django.urls import include, path
from django.views.generic import RedirectView

from admin_site.admin import homie_admin_site

urlpatterns = [
    path('admin/', homie_admin_site.urls),
    path('', RedirectView.as_view(url='admin', permanent=True)),
    path('portfolio', include('portfolio.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]
