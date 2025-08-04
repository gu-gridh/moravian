import json
import zipfile
from pathlib import Path
from django.conf import settings
from .models import Memoir
from .serializers import MemoirSerializer


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
