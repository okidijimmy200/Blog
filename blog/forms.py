from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    # make the comments field optional with required=False.
    comments = forms.CharField(required=False,
                                widget=forms.Textarea)

# creating comments section
class CommentForm(forms.ModelForm):
    '''Django introspects the model and builds the form dynamically for us'''
    class Meta:
        model = Comment
        '''django fields is used to show which fields you want to include in your form using a
fields list, u can ignore if u want to include everything, or fields to exclude'''
        fields = ('name', 'email', 'body')

# search form
class searchForm(forms.Form):
    query = forms.CharField()