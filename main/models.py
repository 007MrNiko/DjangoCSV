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


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f"user_{instance.schema.user.id}/{filename}"


class Schemas(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    name = models.CharField(max_length=30)
    last_modified = models.DateTimeField(verbose_name="last modified", auto_now=True)
    column_separator = models.CharField(max_length=1, choices=COLUMN_SEPARATORS, default=",")
    string_character = models.CharField(max_length=1, choices=STRING_CHARACTER, default="\"")

    def __str__(self):
        return f"{self.user.username} - {self.name}"

    class Meta:
        verbose_name = "Schema"
        verbose_name_plural = "Schemas"
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'],
                name='unique name for every user'
            )
        ]


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

    class Meta:
        verbose_name = "Schemas column"
        verbose_name_plural = "Schemas columns"


class DataSets(models.Model):
    schema = models.ForeignKey(Schemas, on_delete=models.CASCADE)

    date_created = models.DateTimeField(verbose_name="date created", auto_now_add=True)
    rows = models.IntegerField()
    file = models.FileField(upload_to=user_directory_path, blank=True)
    ready = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Data set"
        verbose_name_plural = "Data sets"
