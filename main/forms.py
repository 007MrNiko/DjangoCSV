from django import forms
from main.models import Schemas


class SchemasNewForm(forms.ModelForm):
    class Meta:
        model = Schemas
        fields = ("name", "column_separator", "string_character")

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "name",
                    "placeholder": "Schema title",
                    "aria-label": "username"
                }
            ),
            "column_separator": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "column_separator",
                }
            ),
            "string_character": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "string_character",
                }
            ),
        }

