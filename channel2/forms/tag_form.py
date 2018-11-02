from django import forms

from channel2.data.models import tag_model

ERROR_NAME_HAS_COMMA = 'The tag name must not contain a comma.'
ERROR_MISSING_TAGS = 'Unable to find tag(s): {}.'


class TagForm(forms.ModelForm):

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Name',
            'required': 'required',
        })
    )

    children = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Children Tags',
        })
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Description',
        })
    )

    class Meta:
        model = tag_model.Tag
        fields = ('name', 'type', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        self.children_tag_models = set()

        if 'instance' in kwargs:
            instance = kwargs['instance']
            self.initial['children'] = ', '.join(
                instance.children.all().values_list('name', flat=True))

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if ',' in name:
            raise forms.ValidationError(ERROR_NAME_HAS_COMMA)
        return name

    def clean_children(self):
        children = self.cleaned_data.get('children')
        tag_names = set()
        for tag_name in children.split(','):
            tag_name = tag_name.strip()
            if tag_name:
                tag_names.add(tag_name)

        tag_models = tag_model.Tag.objects.filter(name__in=tag_names)
        missing_tag_names = tag_names - set(t.name for t in tag_models)
        if missing_tag_names:
            error_message = ERROR_MISSING_TAGS.format(', '.join(sorted(missing_tag_names)))
            raise forms.ValidationError(error_message)

        self.children_tag_models = tag_models
        return children

    def save(self, commit=True):
        tag = super().save(commit=False)
        if commit:
            tag.save()

        # Update children tags.
        cur_tags = set(tag.children.all())
        new_tags = set(self.children_tag_models)
        for child_tag in cur_tags - new_tags:
            tag_model.TagChildren.objects.get(parent=tag, child=child_tag).delete()
        for child_tag in new_tags - cur_tags:
            tag_model.TagChildren.objects.create(parent=tag, child=child_tag)

        return tag
