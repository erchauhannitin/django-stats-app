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


class InputStatsFileForm(forms.Form):
    input_Stats_File = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['txt']), validate_file_size])
