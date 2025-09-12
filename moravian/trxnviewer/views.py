from pathlib import Path
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Case, When, IntegerField, Q
from django.views.decorators.cache import cache_page
from django.http import FileResponse, Http404
from django.conf import settings
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle
from .models import Memoir, MemoirImage
from .serializers import MemoirSerializer


class MemoirViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Memoir.objects.select_related('author').prefetch_related(
        'images__transcription'
    ).order_by('id')
    serializer_class = MemoirSerializer


class MemoirZipView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'zip'

    def get(self, request, *args, **kwargs):
        zip_path = Path(settings.BASE_DIR) / 'static' / 'zip' \
                        / 'swedish_moravian_data.zip'
        if not zip_path.exists():
            raise Http404("ZIP file not found")

        return FileResponse(zip_path.open('rb'), as_attachment=True,
                            filename='swedish_moravian_data.zip')


def index(request):
    memoir_list = Memoir.objects.all().select_related('author').prefetch_related(
        'images__transcription').annotate(
        image_count=Count('images', distinct=True),
        transcription_count=Count('images__transcription', distinct=True))
    filtered_images = []

    search_query = request.GET.get('query', '')
    selected_type = request.GET.get('type', 'author')

    if search_query:
        if selected_type == 'author':
            memoir_list = memoir_list.filter(author__name__icontains=search_query)
        if selected_type == 'transcription':
            memoir_list = memoir_list.filter(images__transcription__text__icontains=search_query)
            filtered_images = MemoirImage.objects.filter(
                Q(memoir__in=memoir_list),
                Q(transcription__text__icontains=search_query)).prefetch_related('transcription')

    context = {"memoir_list": memoir_list,
               "filtered_images": filtered_images,
               "search_query": search_query,
               "type": selected_type}
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
    context = {"memoir": memoir, "images": images, "trxn_count": trxn_count}
    return render(request, "trxnviewer/detail_memoir.html", context)


def detail_image(request, memoir_id, image_id):
    image = get_object_or_404(MemoirImage, pk=image_id, memoir=memoir_id)
    memoir = get_object_or_404(Memoir, pk=memoir_id)
    search_query = request.GET.get('query', '')

    context = {"memoir": memoir, "image": image, "search_query": search_query}
    return render(request, "trxnviewer/detail_image.html", context)
