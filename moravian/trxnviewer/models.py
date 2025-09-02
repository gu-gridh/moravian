from django.db import models
from django.conf import settings
from django_prose_editor.fields import ProseEditorField
from django.core.exceptions import ValidationError


class EntityMixin(models.Model):
    created = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL, editable=False, null=True, related_name="%(app_label)s_%(class)s_created")
    modified = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.SET_NULL, editable=False, null=True, related_name="%(app_label)s_%(class)s_modified")
    updated = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class DatePrecision(models.TextChoices):
    EXACT = 'exact', 'Exact'
    YEAR = 'year', 'Year only'


class LanguageOptions(models.TextChoices):
    ENGLISH = 'eng', 'English'
    SWEDISH = 'swe', 'Swedish'
    GERMAN = 'deu', 'German'


class Author(EntityMixin):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Memoir(EntityMixin):
    author = models.ForeignKey(Author, on_delete=models.RESTRICT,
                               related_name='authors')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    date_precision = models.CharField(
        max_length=20,
        choices=DatePrecision.choices,
        default=None,
        blank=True,
        null=True,
    )
    language = models.CharField(
        max_length=20,
        choices=LanguageOptions.choices,
        default=LanguageOptions.SWEDISH,
    )
    context_note = models.CharField(max_length=200, null=True, blank=True)

    def clean(self):
        super().clean()
        if (self.start_date or self.end_date) and not self.date_precision:
            raise ValidationError({
                'date_precision': 'Date precision is required if a start or end date is specified.'
            })

    def __str__(self):
        return self.author.name


class MemoirImage(EntityMixin):
    image_url = models.URLField(blank=True)
    thumb_url = models.URLField(blank=True)
    page = models.CharField(max_length=25, null=True, blank=True)
    memoir = models.ForeignKey(Memoir, on_delete=models.CASCADE,
                               null=True, blank=True, related_name='images')

    def __str__(self):
        return self.page


class Transcription(EntityMixin):
    text = ProseEditorField(blank=True,
        extensions={"Bold": True, "Italic": True, "Underline": True,
                    "ListItem": True, "BulletList": True, "OrderedList": True,
                    "Strike": True, "Subscript": True, "Superscript": True
        },
        sanitize=True)
    image = models.OneToOneField(MemoirImage, on_delete=models.CASCADE,
                                 null=True, blank=True, related_name="transcription")

    def __str__(self):
        return self.text[:125]
