from pathlib import Path
from django.core.exceptions import ValidationError
MAX_FILE_SIZE = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.pdf'}
def validate_upload(value):
    if value.size > MAX_FILE_SIZE:
        raise ValidationError('File must be 5 MB or smaller.')
    if Path(value.name).suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValidationError('Unsupported file type. Use JPG, JPEG, PNG or PDF.')
