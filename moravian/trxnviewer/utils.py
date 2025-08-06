import json
import zipfile
from pathlib import Path
from django.conf import settings
from django.core.serializers import serialize
from .models import Memoir, Author, MemoirImage, Transcription
from .serializers import MemoirSerializer
from gridh_pages.models import Page


def generate_zip_file():
    output_dir = Path(settings.BASE_DIR) / 'static' / 'zip'
    output_dir.mkdir(parents=True, exist_ok=True)
    zip_path = output_dir / 'swedish_moravian_data.zip'

    queryset = Memoir.objects.all().select_related('author').prefetch_related(
        'images__transcription'
    ).order_by('id')
    serializer = MemoirSerializer(queryset, many=True)
    json_data = json.dumps(serializer.data, indent=2)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr("swedish_moravian_data.json", json_data)

    return zip_path


def dump_related_sample():
    parents = Memoir.objects.all()[:25]
    authors = Author.objects.filter(authors__in=parents)
    images = MemoirImage.objects.filter(memoir__in=parents)
    trxn = Transcription.objects.filter(image__in=images)
    pages = Page.objects.all()

    data = []
    data.extend(json.loads(serialize('json', parents)))
    data.extend(json.loads(serialize('json', authors)))
    data.extend(json.loads(serialize('json', images)))
    data.extend(json.loads(serialize('json', trxn)))
    data.extend(json.loads(serialize('json', pages)))

    with open('trxnviewer/fixtures/sample_fixture.json', 'w') as f:
        json.dump(data, f, indent=4)
