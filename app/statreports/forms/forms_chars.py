from django import forms
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize = value.size

    if filesize > 1048576:
        raise ValidationError(
            "The maximum file size that can be uploaded is 1MB")
    else:
        return value


class InputCharsFileForm(forms.Form):
    input_Chars_File = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),
                                       validators=[FileExtensionValidator(allowed_extensions=['txt']), validate_file_size])
