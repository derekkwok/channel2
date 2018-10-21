from unittest import mock

from django import test

from channel2.apps.data.gateways import kitsu_gateway
from channel2.apps.data.models import tag_model
from channel2.apps.web.forms import tag_create_anime_form


class TagCreateAnimeFormTest(test.TestCase):

    def setUp(self):
        super().setUp()
        self.get_anime_data = mock.patch.object(
            kitsu_gateway, 'get_anime_data', autospec=True).start()
        self.get_anime_data.return_value = {
            'attributes': {
                'canonicalTitle': 'Cowboy Bepop',
                'synopsis': 'Some description of the show.',
            },
        }
        self.get_genre_data = mock.patch.object(
            kitsu_gateway, 'get_genre_data', autospec=True).start()
        self.get_genre_data.return_value = [
            {'attributes': {'name': 'Comedy'}},
            {'attributes': {'name': 'Sci-Fi'}},
        ]
        self.addCleanup(mock.patch.stopall)

    def test_save(self):
        kitsu_id = '101'
        form = tag_create_anime_form.TagCreateAnimeForm(data={'kitsu_id': kitsu_id})
        self.assertTrue(form.is_valid(), form.errors)
        tag = form.save()
        self.assertTrue(tag.pk)
        self.assertEqual(tag.name, 'Cowboy Bepop')
        self.assertEqual(tag.type, tag_model.TagType.ANIME)
        self.assertEqual(tag.description, 'Some description of the show.')
        self.get_anime_data.assert_called_once_with(kitsu_id)
        self.get_genre_data.assert_called_once_with(kitsu_id)

    def test_save_tag_already_exists(self):
        tag_model.Tag.objects.create(name='Cowboy Bepop')
        kitsu_id = '102'
        form = tag_create_anime_form.TagCreateAnimeForm(data={'kitsu_id': kitsu_id})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['kitsu_id'],
            [tag_create_anime_form.ERROR_TAG_EXISTS.format('Cowboy Bepop')])
        self.get_anime_data.assert_called_once_with(kitsu_id)
        self.get_genre_data.assert_not_called()

    def test_create_anime_tags(self):
        tag_model.Tag.objects.create(name='Comedy')
        self.assertFalse(tag_model.Tag.objects.filter(name='Sci-Fi').exists())

        kitsu_id = '103'
        tags = tag_create_anime_form.create_anime_tags(kitsu_id)
        self.assertCountEqual(tag_model.Tag.objects.filter(name__in=['Comedy', 'Sci-Fi']), tags)
        self.get_genre_data.assert_called_once_with(kitsu_id)
