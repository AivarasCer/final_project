from django import forms


class UploadFileForm(forms.ModelForm):
    LANGUAGE_CHOICES = [
        ('eng', 'English'),
        ('lit', 'Lithuanian')
    ]
    file = forms.FileField()
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES, initial='lit', widget=forms.RadioSelect)
