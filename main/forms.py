from django import forms


class UploadFileForm(forms.ModelForm):
    file = forms.FileField()
