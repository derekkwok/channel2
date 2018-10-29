import datetime

from django import test

from channel2.apps.data.models import tag_model


class TagTest(test.TestCase):

    def test_relationship(self):
        parent1 = tag_model.Tag.objects.create(name='p1', slug='p1')
        parent2 = tag_model.Tag.objects.create(name='p2', slug='p2')
        child1 = tag_model.Tag.objects.create(name='c1', slug='c1')
        child2 = tag_model.Tag.objects.create(name='c2', slug='c2')
        child3 = tag_model.Tag.objects.create(name='c3', slug='c3')

        tag_model.TagChildren.objects.create(parent=parent1, child=child1)
        tag_model.TagChildren.objects.create(parent=parent1, child=child2)
        tag_model.TagChildren.objects.create(parent=parent2, child=child2)
        tag_model.TagChildren.objects.create(parent=parent2, child=child3)

        self.assertCountEqual(parent1.children.all(), [child1, child2])
        self.assertCountEqual(parent2.children.all(), [child2, child3])
        self.assertCountEqual(child2.parents.all(), [parent1, parent2])

    def test_tag_save_slug(self):
        tag1 = tag_model.Tag.objects.create(name='This is a test')
        tag2 = tag_model.Tag.objects.create(name='This is a test$')
        self.assertEqual(tag1.slug, 'this-is-a-test')
        self.assertEqual(tag2.slug, 'this-is-a-test-1')

    def test_get_anime_season_name(self):
        timestamp = datetime.datetime(2018, 10, 28)
        self.assertEqual(
            '2018 Q4',
            tag_model.get_anime_season_name(timestamp))
