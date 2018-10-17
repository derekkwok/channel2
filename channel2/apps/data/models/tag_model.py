from django.db import models
from django.utils.text import slugify


def cover_image_upload_to(instance, filename):
    del filename  # Unused.
    return 'cover/{}'.format(instance.slug)


class TagType:

    UNKNOWN = 'unknown'  # Unknown tag type.

    ANIME = 'anime'  # Anime series.
    ANIME_SEASON = 'anime-season'  # Season - e.g. "2018 Q4".
    ANIME_TAG = 'anime-tag'  # Anime tag - e.g. "Action" or "Horror".
    MOVIE = 'movie'  # Movies.
    TV = 'tv'  # TV series.

    choices = (
        (ANIME, 'Anime'),
        (ANIME_SEASON, 'Anime Seasons'),
        (ANIME_TAG, 'Anime Tags'),
        (MOVIE, 'Movies'),
        (TV, 'TV Shows'),
    )

    d = dict(choices)


class Tag(models.Model):

    name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=250, unique=True)
    type = models.CharField(
        max_length=20,
        choices=TagType.choices,
        default=TagType.UNKNOWN)
    description = models.TextField(blank=True)
    metadata = models.TextField(blank=True)
    children = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='parents',
        through='TagChildren',
        through_fields=('parent', 'child'))
    cover_image = models.FileField(upload_to=cover_image_upload_to, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        db_table = 'tag'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        self.slug = slug = slugify(self.name)
        counter = 1
        while Tag.objects.filter(slug=self.slug).exclude(id=self.pk).exists():
            self.slug = '{}-{}'.format(slug, counter)
            counter += 1
        super().save(*args, **kwargs)


class TagChildren(models.Model):

    parent = models.ForeignKey(
        Tag,
        db_column='parent_tag_id',
        on_delete=models.CASCADE,
        related_name='+')
    child = models.ForeignKey(
        Tag,
        db_column='child_tag_id',
        on_delete=models.CASCADE,
        related_name='+')

    objects = models.Manager()

    class Meta:
        db_table = 'tag_children'
