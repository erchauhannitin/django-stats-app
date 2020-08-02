from django import forms


class InputFileForm(forms.Form):
    inputFile = forms.FileField()
