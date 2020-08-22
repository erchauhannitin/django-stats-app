from django import forms


class ChartTypeForm(forms.Form):
    CHART_CHOICES = (
        ('bar', 'bar'),
        ('pie', 'pie'),
        ('variablepie', 'variablepie'),
        ('bubble', 'bubble'),
    )

    filter_by = forms.ChoiceField(choices=CHART_CHOICES, required=False)
