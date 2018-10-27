from django.db import models

from channel2.apps.data.models import tag_model


class Video(models.Model):

    name = models.CharField(max_length=1000)
    file = models.FileField()
    tag = models.ForeignKey(tag_model.Tag, on_delete=models.PROTECT)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        db_table = 'video'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        if not self.file:
            raise RuntimeError('The file attribute must be set.')
        return super().save(*args, **kwargs)
