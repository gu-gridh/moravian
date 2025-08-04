from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Case, When, IntegerField
from rest_framework import viewsets
from django.views.decorators.cache import cache_page
from .models import Memoir, MemoirImage
from .serializers import MemoirSerializer


class MemoirViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Memoir.objects.select_related('author').prefetch_related(
        'images__transcription'
    ).order_by('id')
    serializer_class = MemoirSerializer


def index(request):
    memoir_list = Memoir.objects.select_related('author').prefetch_related(
        'images__transcription').annotate(
        image_count=Count('images', distinct=True),
        transcription_count=Count('images__transcription', distinct=True))
    context = {"memoir_list": memoir_list}
    return render(request, "trxnviewer/index.html", context)


@cache_page(60 * 15)  # cache view for 15 minutes
def detail_memoir(request, memoir_id):
    memoir = get_object_or_404(Memoir, pk=memoir_id)
    images = MemoirImage.objects.filter(memoir=memoir_id).prefetch_related(
        'transcription').annotate(
        has_transcription=Case(
            When(transcription__isnull=False, then=1),
            default=0,
            output_field=IntegerField()
            )).order_by('page')
    trxn_count = images.aggregate(total=Count('transcription'))
    ['total']
    context = {"memoir": memoir, "images": images, 'trxn_count': trxn_count}
    return render(request, "trxnviewer/detail_memoir.html", context)


def detail_image(request, memoir_id, image_id):
    image = get_object_or_404(MemoirImage, pk=image_id, memoir=memoir_id)
    memoir = get_object_or_404(Memoir, pk=memoir_id)
    context = {"memoir": memoir, "image": image}
    return render(request, "trxnviewer/detail_image.html", context)
