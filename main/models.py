from django.conf import settings
from django.db import models


COLUMN_SEPARATORS = (
    (",", "Comma (,)"),
    (":", "Colon (:)"),
    ("-", "Hyphen (-)")
)

STRING_CHARACTER = (
    ("\"", "Double-quote (\")"),
    ("'", "Single-quote (')"),
    ("|", "Vertical Line (|)")
)

CATEGORY_TYPE = (
    ("full_name", "Full name"),
    ("email", "Email"),
    ("phone_number", "Phone number"),
    ("integer", "Integer"),
    ("text", "Text")
)


class Schemas(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    name = models.CharField(max_length=30, unique=True)
    last_modified = models.DateTimeField(verbose_name="last modified", auto_now=True)
    column_separator = models.CharField(max_length=1, choices=COLUMN_SEPARATORS, default=",")
    string_character = models.CharField(max_length=1, choices=STRING_CHARACTER, default="\"")

    def __str__(self):
        return f"{self.user.username} - {self.name}"


class SchemasColumn(models.Model):
    schema = models.ForeignKey(Schemas, on_delete=models.CASCADE)

    name = models.CharField(max_length=30)
    category = models.CharField(max_length=12, choices=CATEGORY_TYPE, blank=False, default="full_name")
    min_integer = models.IntegerField(default=18, blank=True)
    max_integer = models.IntegerField(default=60, blank=True)
    sentence_amount = models.IntegerField(default=5, blank=True)
    order = models.IntegerField()

    def __str__(self):
        return f"{self.schema.name} - {self.name}"

