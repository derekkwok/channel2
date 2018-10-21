import json
from typing import List, Text

from django import forms

from channel2.apps.data.gateways import kitsu_gateway
from channel2.apps.data.models import tag_model

ERROR_TAG_EXISTS = '{} already exists.'


class TagCreateAnimeForm(forms.Form):

    kitsu_id = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag: tag_model.Tag = tag_model.Tag(type=tag_model.TagType.ANIME)
        self.genres: List[tag_model.Tag] = []

    def clean_kitsu_id(self):
        kitsu_id = self.cleaned_data.get('kitsu_id')
        data = kitsu_gateway.get_anime_data(kitsu_id)

        # Validate that title does not already exist in the database.
        name = data['attributes']['canonicalTitle']
        if tag_model.Tag.objects.filter(name=name).exists():
            raise forms.ValidationError(ERROR_TAG_EXISTS.format(name))

        self.tag.name = data['attributes']['canonicalTitle']
        self.tag.metadata = json.dumps(data)
        self.tag.description = data['attributes']['synopsis']
        self.genres = create_anime_tags(kitsu_id)

    def save(self, commit=True):
        if not commit:
            return self.tag

        self.tag.save()
        for genre in self.genres:
            tag_model.TagChildren.objects.create(parent=genre, child=self.tag)
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
