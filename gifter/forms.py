from django import forms
from django.forms import JSONField, ModelForm
from django.template import loader
from django.utils.safestring import mark_safe

from gifter.models import Item


class LinksWidget(forms.Widget):
    template_name = 'multi_link_widget_template.html'

    def get_context(self, name, value, attrs=None):
        return {'widget': {
            'name': name,
            'value': value,
        }}

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)


class MultiLinkJsonField(JSONField):
    widget = LinksWidget


class ItemForm(ModelForm):
    links = MultiLinkJsonField(required=False)

    class Meta:
        model = Item
        fields = ['title', 'description', 'links']


class InviteParticipantForm(forms.Form):
    email_address = forms.EmailField()
