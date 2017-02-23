from django import forms


class CommentForm(forms.Form):
    content = forms.CharField()
    # created_date = forms.DateTimeField(auto_now_add=True)


# class PostForm(forms.Form):
#     content = forms.CharField(required=False)
#     photo = forms.ImageField()

class PostForm(forms.Form):
    content = forms.CharField(required=False)
    photo = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
