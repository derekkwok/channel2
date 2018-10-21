import json

from django import forms

from channel2.apps.data.models import tag_model

ERROR_TAG_EXISTS = '{} already exists.'


class TagCreateAnimeForm(forms.Form):

    metadata = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = tag_model.Tag(
            type=tag_model.TagType.ANIME_TAG)

    def clean_metadata(self):
        metadata = self.cleaned_data.get('metadata')
        data = json.loads(metadata)

        name = data['attributes']['canonicalTitle']
        if tag_model.Tag.objects.filter(name=name).exists():
            raise forms.ValidationError(ERROR_TAG_EXISTS.format(name))

        self.tag.name = name
        self.tag.description = data['attributes']['synopsis']
        self.tag.metadata = metadata
        return metadata

    def save(self, commit=True):
        if commit:
            self.tag.save()
        return self.tag
