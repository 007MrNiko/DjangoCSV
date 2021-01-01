from django import forms
from django.forms import inlineformset_factory
from main.models import Schemas, SchemasColumn, CATEGORY_TYPE


class SchemasNewForm(forms.ModelForm):
    class Meta:
        model = Schemas
        fields = ("name", "column_separator", "string_character")

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Schema title",
                    "aria-label": "username"
                }
            ),
            "column_separator": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "string_character": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }


class SchemasNewCategories(forms.Form):
    column_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    category_type = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "form-select"}),
        choices=CATEGORY_TYPE
    )
    order = forms.IntegerField(
        min_value=0, initial=0,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )


SchemasColumnFormset = inlineformset_factory(
    Schemas,
    SchemasColumn,
    can_delete=False,
    extra=1,
    fields=("name", "category", "min_integer", "max_integer", "sentence_amount", "order"),
    widgets={
        "name": forms.TextInput(attrs={"class": "form-control", "required": "required"}),
        "category": forms.Select(attrs={"class": "form-select", "required": "required"}),
        "min_integer": forms.NumberInput(attrs={"class": "form-control integer_type"}),
        "max_integer": forms.NumberInput(attrs={"class": "form-control integer_type"}),
        "sentence_amount": forms.NumberInput(attrs={"class": "form-control sentence_type"}),
        "order": forms.NumberInput(attrs={"class": "form-control", "required": "required"}),
    }
)
