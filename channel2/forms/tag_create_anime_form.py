import datetime
import json
from typing import List, Text

from django import forms
from django.core.files.base import ContentFile

from channel2.data.models import tag_model
from channel2.gateways import kitsu_gateway
from channel2.lib import download_lib

ERROR_TAG_EXISTS = '{} already exists.'


class TagCreateAnimeForm(forms.Form):

    kitsu_id = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag: tag_model.Tag = tag_model.Tag(type=tag_model.TagType.ANIME)
        self.cover_data: download_lib.FileData = None
        self.genres: List[tag_model.Tag] = []
        self.seasons: List[tag_model.Tag] = []

    def clean_kitsu_id(self) -> Text:
        kitsu_id = self.cleaned_data.get('kitsu_id')
        data = kitsu_gateway.get_anime_data(kitsu_id)

        # Validate that title does not already exist in the database.
        name = data['attributes']['canonicalTitle']
        if tag_model.Tag.objects.filter(name=name).exists():
            raise forms.ValidationError(ERROR_TAG_EXISTS.format(name))

        # Download the cover image.
        cover_url = data['attributes']['posterImage']['original']
        self.cover_data = download_lib.download_file(cover_url)

        # Set other attributes on the tag.
        self.tag.name = data['attributes']['canonicalTitle']
        self.tag.metadata = json.dumps(data)
        self.tag.description = data['attributes']['synopsis']
        self.genres = create_anime_tags(kitsu_id)
        self.seasons = create_season_tags(data['attributes']['startDate'])
        return kitsu_id

    def save(self, commit=True) -> tag_model.Tag:
        if not commit:
            return self.tag

        self.tag.save()
        cover_name = '{}.{}'.format(self.tag.slug, self.cover_data.extension)
        self.tag.cover_image.save(  # pylint: disable=no-member
            cover_name,
            ContentFile(self.cover_data.bytes))
        for genre in self.genres:
            tag_model.TagChildren.objects.create(parent=genre, child=self.tag)
        for season in self.seasons:
            tag_model.TagChildren.objects.create(parent=season, child=self.tag)
        return self.tag


def create_anime_tags(kitsu_id: Text) -> List[tag_model.Tag]:
    data = kitsu_gateway.get_genre_data(kitsu_id)
    tag_names = set(d['attributes']['name'] for d in data)
    tag_names_in_db = set(
        tag_model.Tag.objects.filter(name__in=tag_names).values_list('name', flat=True))

    # Create tags that don't exist in the DB yet.
    for tag_name in tag_names - tag_names_in_db:
        tag_model.Tag.objects.create(name=tag_name, type=tag_model.TagType.ANIME_TAG)

    # Fetch and return all anime tags.
    return tag_model.Tag.objects.filter(name__in=tag_names)


def create_season_tags(start_date_str: Text) -> List[tag_model.Tag]:
    start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
    tag_name = tag_model.get_anime_season_name(start_date)
    tag = tag_model.Tag.objects.get_or_create(
        name=tag_name,
        type=tag_model.TagType.ANIME_SEASON)[0]
    return [tag]
