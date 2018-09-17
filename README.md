# Auto User Provision

## Description

This is a stand-alone application which can be plugged into any Django app.

The app allows you to easily register users and associate them to groups (or any Django model) by using rotating keys.

Keys automatically rotate after a period specified in your settings.py
You may restrict the number of uses a key is valid for during it's rotation period.

## Installation

1. Drop this parent directory in your django app
2. Add 'auto_user_provision' to your INSTALLED_APPS in settings.py
3. Add the following AUP configuration to your settings.py:


```python
AUP_CURRENT_USE_MAX = 15  # Max uses for a key during it's rotation period. Resets to 0 after rotating.
AUP_ROTATION_EXPIRY_DAYS = 7  # Days after which keys should expire and rotate.
AUP_ROTATION_EXPIRY_HOURS = 0  # ^ but hours
AUP_ROTATION_EXPIRY_MINUTES = 0  # ^ but minutes
```

## How to Use

### Models

Associate a key with your model by utilising the ForeignKey field:



```python
class Company(models.Model):
	...
	invite_key = models.ForeignKey(RotatingProvisionKey,
									on_delete=models.CASCADE,
									blank=True, null=True)
	...

```
### URLs

Include AUP URLs in your project's url configuration and override the input URL to redirect to your own view (Poort example):



```python
urlpatterns = [
	...
	url(r'^aup/input$', PoortProvisionKeyInputView.as_view(), name='provision_key_input'),
    url(r'^aup/', include('auto_user_provision.urls')),
	...
	]
```


To navigate to the key input form, reverse 'provision_key_input'

### Views


Subclass the ProvisionKeyInputView class and override it's `form_valid()` function.

This is where you'll include the logic for your own project, namely associating a user with a group/company by using a key.


```python
class PoortProvisionKeyInputView(ProvisionKeyInputView):

    def form_valid(self, form):
        super(PoortProvisionKeyInputView, self).form_valid(form)
        try:
            key_model = RotatingProvisionKey.objects.get(key=str(form.cleaned_data['key']))
            company = Company.objects.get(invite_key=key_model)
            user = self.request.user.userprofile
            key_model.register_use()
            user.company.add(company)
        except Company.DoesNotExist:
            form.add_error('key', "No Company Matching Key Found")
        except KeyMaxUseExceeded:
            form.add_error('key', "Key Exceeded Maximum Use")
        if form.errors:
            return super(PoortProvisionKeyInputView, self).form_invalid(form)
        return HttpResponseRedirect(self.get_success_url())
```


Please note that some basic validation is already done by the ProvisionKeyInputView class you inherit from.

It is not necessary to duplicate this effort.

*You are only required to extend the class to include your own project-specific functionality*

### Templates

Create a directory called `auto_user_provision` under your project's templates directory to override the app's built in templates.

The following templates may be overridden:


1. key_input_form.html
2. key_input_form_success.html

This is what my key_input_form.html looks like for Poort:



```html
{% extends 'website/base.html' %}

{% block title %}
    Enter Invitation Key
{% endblock %}

{% block payload %}
    <br>
    <p>
        Please enter your invitation key below. You will automatically be assigned to the company that invited you.
    </p>

    <p>Don't have a key? Please contact the company that you would like to join and request an invitation key.</p>

    <form action="" method="post">{% csrf_token %}
        <table class="table">
            {{ form.as_table }}
            <tr>
                <td colspan="2">
                    <input type="submit" value="Save"/>
                </td>
            </tr>
        </table>
    </form>
{% endblock %}

```

And this is my key_input_form_success.html



```html
{% extends 'website/base.html' %}

{% block title %}
    Invitation Successful!
{% endblock %}

{% block payload %}
    <div class="text-center">
        <br>
        <p>Congratulations! The key you entered was successfully loaded.</p>
        <p>Now that you've joined this company, you have read access to it's <a
                href="{% url 'list_devices' %}">devices</a>.
            <br>You are now able to add widgets for these devices on your <a href="{% url 'application' %}">dashboards</a>.</p>
        <p>If you require additional permissions, please contact the admin in your company.</p>
    </div>
{% endblock %}
```

### Crontab

In order to schedule the rotation of keys, it is recommended that you use the built-in management command called `rotate_keys`.

Set up a crontab that runs hourly and calls the `rotate_keys` management command via your project's manage.py script.

