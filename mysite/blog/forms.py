from django import forms

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    # make the comments field optional with required=False.
    comments = forms.CharField(required=False,
                                widget=forms.Textarea)