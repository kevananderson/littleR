from django import forms


class ReqText(forms.Form):
    """Form for editing the content of a requirement."""
    
    choices=[
            ("customer", "Customer"),
            ("service", "Service"),
            ("hardware", "Hardware"),
            ("software", "Software")
            ]

    index = forms.CharField(widget=forms.HiddenInput())
    title = forms.CharField(label="Title", max_length=300)
    type = forms.ChoiceField(label="Type", choices=choices, widget=forms.Select)
    requirement = forms.CharField(label="Requirement", widget=forms.Textarea)
    description = forms.CharField(label="Description", widget=forms.Textarea)
    assumptions = forms.CharField(label="Assumptions", widget=forms.Textarea)
    component = forms.CharField(label="Component", max_length=100, required=False)

class ReqPath(forms.Form):
    """Form for editing the path of a requirement."""
    
    index = forms.CharField(widget=forms.HiddenInput())
    path = forms.ChoiceField(label="Path", widget=forms.Select)

    def __init__(self, *args, **kwargs):
        path_choices = kwargs.pop("path_choices",[])
        super().__init__(*args, **kwargs)
        path = self.fields["path"]
        path.choices = path_choices

class ReqLabel(forms.Form):
        """Form for adding a label to a requirement."""
        
        index = forms.CharField(widget=forms.HiddenInput())
        new_label = forms.CharField(label="New Label", max_length=100, required=False)