from django import forms
from .models import Section, Post, Comment
from tinymce.widgets import TinyMCE


class SectionForm(forms.ModelForm):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'name your new section'}))

    class Meta:
        model = Section
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            try:
                Section.objects.get(name=name).id
                raise forms.ValidationError('this section already exists.')
            except Section.DoesNotExist:
                return name

class PostForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'title'}))
    # text = forms.CharField(label='', widget = forms.Textarea(attrs={'placeholder': 'share your knowledge', 'rows': 5, 'cols': 10}))
    text = forms.CharField(label='', widget=TinyMCE(attrs={'cols': 10, 'rows': 30}))

    class Meta:
        model = Post
        fields= ['title', 'text']


class CommentForm(forms.Form):
    text = forms.CharField(label='', widget = forms.Textarea(attrs={'rows': 2, 'cols': 10, 'placeholder': 'add your thoughts'}))
