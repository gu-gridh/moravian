from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Memoir, MemoirImage, Transcription, Author
from .utils import generate_zip_file


@receiver(post_save, sender=Memoir)
@receiver(post_delete, sender=Memoir)
@receiver(post_save, sender=MemoirImage)
@receiver(post_delete, sender=MemoirImage)
@receiver(post_save, sender=Author)
@receiver(post_delete, sender=Author)
@receiver(post_save, sender=Transcription)
@receiver(post_delete, sender=Transcription)
def regenerate_zip_on_change(sender, **kwargs):
    generate_zip_file()
