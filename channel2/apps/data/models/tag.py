from django.db import models


class TagType:

    ANIME = 'anime'  # Anime series.
    COMMON = 'common'  # Common tag - e.g. genres such as "Action" or "Horror".
    MOVIE = 'movie'  # Movies.
    TV = 'tv'  # TV series.
    SEASON = 'season'  # Season - e.g. "2018 Q4".

    choices = (
        (ANIME, ANIME),
        (COMMON, COMMON),
        (MOVIE, MOVIE),
        (TV, TV),
        (SEASON, SEASON),
    )

    d = dict(choices)


class Tag(models.Model):

    name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, unique=True)
    type = models.CharField(
        max_length=20,
        choices=TagType.choices,
        default=TagType.COMMON)
    description = models.TextField(blank=True)
    children = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='parents',
        through='TagChildren',
        through_fields=('parent', 'child'))
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        db_table = 'tag'

    def __str__(self):
        return self.name


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
