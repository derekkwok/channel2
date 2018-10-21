import json

from django import test

from channel2.apps.data.models import tag_model
from channel2.apps.web.forms import tag_create_anime_form

DATA = {
    'attributes': {
        'canonicalTitle': 'Cowboy Bepop',
        'synopsis': 'Some description of the show.',
    },
}


class TagCreateAnimeFormTest(test.TestCase):

    def test_save(self):
        form = tag_create_anime_form.TagCreateAnimeForm(data={'metadata': json.dumps(DATA)})

        self.assertTrue(form.is_valid())
        tag = form.save()
        self.assertTrue(tag.pk)
        self.assertEqual(tag.name, 'Cowboy Bepop')
        self.assertEqual(tag.type, tag_model.TagType.ANIME_TAG)
        self.assertEqual(tag.description, 'Some description of the show.')

    def test_clean_metadata_name_unique(self):
        tag_model.Tag.objects.create(name='Cowboy Bepop')
        form = tag_create_anime_form.TagCreateAnimeForm(data={'metadata': json.dumps(DATA)})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['metadata'],
            [tag_create_anime_form.ERROR_TAG_EXISTS.format('Cowboy Bepop')])
