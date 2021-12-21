from django import forms


class InviteParticipantForm(forms.Form):
    email_address = forms.EmailField()
