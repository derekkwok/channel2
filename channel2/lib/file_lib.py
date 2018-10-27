import os

from django.conf import settings
from django.core import files

from channel2.apps.data.models import tag_model, video_model


def create_video(
        file: files.File,
        tag: tag_model.Tag) -> video_model.Video:
    filepath = os.path.join('video', tag.name, file.name)
    abs_filepath = os.path.join(settings.MEDIA_ROOT, filepath)
    os.makedirs(os.path.dirname(abs_filepath), exist_ok=True)
    with open(abs_filepath, 'wb+') as target:
        for chunk in file.chunks():
            target.write(chunk)
    video = video_model.Video(name=file.name, tag=tag)
    video.file.name = filepath
    video.save()
    return video
