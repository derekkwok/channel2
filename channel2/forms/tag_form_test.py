from django import forms, test

from channel2.data.models import tag_model
from channel2.forms import tag_form


class TagFormTest(test.TestCase):

    def test_clean_name(self):
        form = tag_form.TagForm()
        form.cleaned_data = {'name': 'Hello, World!'}
        with self.assertRaises(forms.ValidationError) as context_manager:
            form.clean_name()
        self.assertEqual(context_manager.exception.message, tag_form.ERROR_NAME_HAS_COMMA)

    def test_clean_children(self):
        tag1 = tag_model.Tag.objects.create(name='tag 1')
        tag2 = tag_model.Tag.objects.create(name='tag 2')
        form = tag_form.TagForm()
        form.cleaned_data = {'children': 'tag 1 , tag 2,'}
        form.clean_children()
        self.assertCountEqual(form.children_tag_models, [tag1, tag2])

    def test_clean_children_missing_tag(self):
        tag_model.Tag.objects.create(name='tag 1')
        form = tag_form.TagForm()
        form.cleaned_data = {'children': 'tag 1 , tag 2, tag 3'}
        with self.assertRaises(forms.ValidationError) as context_manager:
            form.clean_children()
        self.assertEqual(
            context_manager.exception.message,
            tag_form.ERROR_MISSING_TAGS.format('tag 2, tag 3'))

    def test_save_create(self):
        tag1 = tag_model.Tag.objects.create(name='tag 1')
        tag2 = tag_model.Tag.objects.create(name='tag 2')

        form = tag_form.TagForm(data={
            'name': 'tag 0',
            'type': tag_model.TagType.ANIME,
            'children': 'tag 1, tag 2',
            'description': 'Tag 0 description.',
        })

        self.assertTrue(form.is_valid(), form.errors)
        tag = form.save()
        self.assertEqual(tag.name, 'tag 0')
        self.assertEqual(tag.description, 'Tag 0 description.')
        self.assertCountEqual(tag.children.all(), [tag1, tag2])

    def test_save_edit(self):
        child_tag1 = tag_model.Tag.objects.create(name='child tag 1')
        child_tag2 = tag_model.Tag.objects.create(name='child tag 2')
        parent_tag = tag_model.Tag.objects.create(name='parent tag')
        tag_model.TagChildren.objects.create(parent=parent_tag, child=child_tag1)

        form = tag_form.TagForm(instance=parent_tag, data={
            'name': 'parent tag updated',
            'type': tag_model.TagType.ANIME,
            'children': 'child tag 2',
            'description': '',
        })

        self.assertTrue(form.is_valid())
        parent_tag = form.save()
        self.assertEqual(parent_tag.name, 'parent tag updated')
        self.assertCountEqual(parent_tag.children.all(), [child_tag2])
