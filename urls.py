from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^input$', views.ProvisionKeyInputView.as_view(), name='provision_key_input'),
    url(r'^success/$', TemplateView.as_view(template_name="auto_user_provision/key_input_form_success.html"),
        name='provision_key_input_success'),

]
