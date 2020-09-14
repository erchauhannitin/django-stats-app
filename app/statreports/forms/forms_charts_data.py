from django import forms


class ChartTypeForm(forms.Form):
    CHART_CHOICES = (
        ('bar', 'bar'),
        ('pie', 'pie'),
        ('variablepie', 'variablepie'),
        ('bubble', 'bubble'),
        ('scatter', 'scatter'),
        ('pyramid', 'pyramid'),
        ('area', 'area'),
        ('line', 'line'),
        ('spline', 'spline'),
        ('column', 'column'),
        ('cylinder', 'cylinder'),
        ('funnel3d', 'funnel3d'),
        ('pyramid3d', 'pyramid3d'),
        ('scatter3d', 'scatter3d'),

    )

    filter_by = forms.ChoiceField(choices=CHART_CHOICES, required=False)
