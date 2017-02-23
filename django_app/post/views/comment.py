from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from post.forms import CommentForm
from post.models import Comment, Post

__all__ = (
    'comment_delete',
    'comment_add',
)


@login_required
def comment_delete(request, comment_id, post_id):
    """
    1. post_detail.html? Comment?? loop??? form? ??
    2. ?? view(url)? comment_delete? ??? ?
    3. ??? ?? ? ??? ????
    4. redirect
    """
    if request.method == 'POST':
        comment = Comment.objects.get(id=comment_id)
        if comment.author.id == request.user.id:
            comment.delete()
        return redirect('post:list')


@login_required
def comment_add(request, post_id):
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            # HttpRequest?? ?? User??? ????
            user = request.user
            # URL??? ??? post_id?? ??
            post = Post.objects.get(id=post_id)
            # post? ???? ???? Comment?? ??
            post.add_comment(user, content)

        # ?? ???? post_detail? ?????
        return redirect('post:list')
