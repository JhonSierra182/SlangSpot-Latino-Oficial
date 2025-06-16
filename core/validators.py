from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import os

def validate_file_size(value):
    filesize = value.size
    if filesize > 10 * 1024 * 1024:  # 10MB
        raise ValidationError(_("El archivo no puede ser mayor a 10MB"))

def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    if ext.lower() not in valid_extensions:
        raise ValidationError(_('Formato de imagen no soportado. Use: jpg, jpeg, png o gif'))

def validate_audio_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp3', '.wav', '.ogg']
    if ext.lower() not in valid_extensions:
        raise ValidationError(_('Formato de audio no soportado. Use: mp3, wav u ogg')) 