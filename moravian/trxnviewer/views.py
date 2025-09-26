from pathlib import Path
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Case, When, IntegerField, Q, Prefetch
from django.views.decorators.cache import cache_page
from django.http import FileResponse, Http404, HttpResponse
from django.conf import settings
from django.utils.text import slugify
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from .models import Memoir, MemoirImage
from .serializers import MemoirSerializer, MemoirImageSerializer


class MemoirViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MemoirSerializer

    def get_queryset(self):
        visible_images = Prefetch(
            "images",
            queryset=MemoirImage.objects.filter(visibility=True)
                                .select_related("transcription"),
            to_attr="visible_images",
        )
        return (Memoir.objects
                .select_related("author")
                .prefetch_related(visible_images)
                .order_by("id"))


class TranscriptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MemoirImage.objects.filter(visibility=True).select_related("memoir")
    serializer_class = MemoirImageSerializer

    # get transcription as simple txt file
    @action(detail=True, methods=["get"], url_path="transcription.txt")
    def transcription_txt(self, request, pk=None):
        image = self.get_object()  # respects visibility=True
        text = getattr(image, "transcription", "")

        if not text:
            return HttpResponse(status=404)

        filename = f"{slugify('memoir')}-{slugify(image.page or f'image-{image.pk}')}-transcription.txt"
        resp = HttpResponse(str(image.memoir) + "\n" + str(image.page) + "\n\n" + text.text, content_type="text/plain; charset=utf-8")
        resp["Content-Disposition"] = f'attachment; filename="{filename}"'
        return resp


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
            memoir_list = memoir_list.filter(
                Q(images__visibility=True),
                Q(images__transcription__text__icontains=search_query)
                )
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
    images = MemoirImage.objects.filter(memoir=memoir_id, visibility=True).prefetch_related(
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
    prev_id = (MemoirImage.objects
               .filter(memoir=memoir, visibility=True,
                       position__lt=image.position)
               .order_by("-position", "-pk")
               .values_list("pk", flat=True).first())
    next_id = (MemoirImage.objects
               .filter(memoir=memoir, visibility=True,
                       position__gt=image.position)
               .order_by("position", "pk")
               .values_list("pk", flat=True).first())
    search_query = request.GET.get('query', '')

    context = {"memoir": memoir, "image": image, "prev_id": prev_id,
               "next_id": next_id, "search_query": search_query}
    return render(request, "trxnviewer/detail_image.html", context)
