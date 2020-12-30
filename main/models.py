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


class Schemas(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    name = models.CharField(max_length=30, unique=True)
    last_modified = models.DateTimeField(verbose_name="last modified", auto_now=True)
    column_separator = models.CharField(max_length=1, choices=COLUMN_SEPARATORS, default=",")
    string_character = models.CharField(max_length=1, choices=STRING_CHARACTER, default="\"")

