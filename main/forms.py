from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet, BooleanField, CheckboxInput
from django.forms.formsets import DELETION_FIELD_NAME

from main.models import Schemas, SchemasColumn, CATEGORY_TYPE, DataSets


class DatasetForm(forms.ModelForm):
    class Meta:
        model = DataSets
        fields = ("rows",)

        widgets = {"rows": forms.NumberInput(attrs={"min": 0, "class": "form-control", "value": 100})}

    def clean_rows(self):
        rows = self.cleaned_data.get("rows")
        if rows < 0:
            raise forms.ValidationError("Please enter value grater than 0")
        else:
            return rows


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

class SchemasColumnFormsetEdit(BaseInlineFormSet):
    def add_fields(self, form, index):
        super(SchemasColumnFormsetEdit, self).add_fields(form, index)
        if self.can_delete:
            form.fields[DELETION_FIELD_NAME] = BooleanField(
                required=False,
                widget=CheckboxInput(attrs={"class": "delete_column"})
            )


SchemasColumnFormset = inlineformset_factory(
    Schemas,
    SchemasColumn,
    can_delete=True,
    extra=1,
    formset=SchemasColumnFormsetEdit,
    fields=("name", "category", "min_integer", "max_integer", "sentence_amount", "order"),
    widgets={
        "name": forms.TextInput(attrs={"class": "form-control text_input", "required": "required"}),
        "category": forms.Select(attrs={"class": "form-select category_input",
                                        "required": "required",
                                        "onchange": "realTimeChanging(this.id)"
                                        }),
        "min_integer": forms.NumberInput(attrs={"min": 0, "class": "form-control integer_type min_integer"}),
        "max_integer": forms.NumberInput(attrs={"min": 0, "class": "form-control integer_type max_integer"}),
        "sentence_amount": forms.NumberInput(attrs={"min": 0, "class": "form-control sentence_type"}),
        "order": forms.NumberInput(attrs={"class": "form-control order_input", "required": "required"}),
    }
)
