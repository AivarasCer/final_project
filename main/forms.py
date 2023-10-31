from django import forms


class UploadFileForm(forms.Form):
    LANGUAGE_CHOICES = [
        ('eng', 'English'),
        ('lit', 'Lithuanian')
    ]
    file = forms.FileField()
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES, initial='eng', widget=forms.RadioSelect)
