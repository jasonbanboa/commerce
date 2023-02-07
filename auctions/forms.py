from django import forms

class CommentForm(forms.Form):
    comment = forms.CharField(label='', max_length=300, widget=forms.TextInput(attrs={'placeholder': 'Add a comment', 'class': 'form-control fifty-percent'}))