from django import test

from channel2.apps.data.models.tag import Tag, TagChildren


class TagTest(test.TestCase):

    def test_relationship(self):
        parent1 = Tag.objects.create(name='p1', slug='p1')
        parent2 = Tag.objects.create(name='p2', slug='p2')
        child1 = Tag.objects.create(name='c1', slug='c1')
        child2 = Tag.objects.create(name='c2', slug='c2')
        child3 = Tag.objects.create(name='c3', slug='c3')

        TagChildren.objects.create(parent=parent1, child=child1)
        TagChildren.objects.create(parent=parent1, child=child2)
        TagChildren.objects.create(parent=parent2, child=child2)
        TagChildren.objects.create(parent=parent2, child=child3)

        self.assertCountEqual(parent1.children.all(), [child1, child2])
        self.assertCountEqual(parent2.children.all(), [child2, child3])
        self.assertCountEqual(child2.parents.all(), [parent1, parent2])
