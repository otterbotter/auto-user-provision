from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic.edit import FormView

from auto_user_provision.forms import ProvisionKeyInputForm
from auto_user_provision.models import RotatingProvisionKey, KeyDoesNotMatchException


def index(request):
    return HttpResponse("Hello, world. You're at the auto user provision index.")


class ProvisionKeyInputView(FormView):
    template_name = 'auto_user_provision/key_input_form.html'
    form_class = ProvisionKeyInputForm
    success_url = 'success/'
