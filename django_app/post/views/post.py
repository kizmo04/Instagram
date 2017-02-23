"""
Post List? ???? ??? ??
1. View? post_list?? ??
2. Template? post_list.html?? ??
3. View?? post_list.html? render? ??? ????? ?
4. instagram/urls.py?
    post/urls.py? ???? (app_name? post)
5. '/post/'? ???? ? post_list View? ?????
    post/urls.py? ??? ??
6. ?? Post? ???? ????
    context? ???? post_list ?? ??
7. post_list.html?? {% for %}??? ???
    post_list? ??? ???? ??
Post Detail (??? Post? ?? ????)
1. View? post_detail?? ??
2~4. ?? ??
5. '/post/<??>/'? ???? ? post_detail View?
    ????? post/urls.py? ?? ??
    ? ?, post_id?? ???? ???? ????? ??
6. url??? ???? post_id? ???? Post???
    context? ?? post_detail??? ??
Post Detail? ?????? ??
1. request.method? ?? ?? ????? if/else?? ??
2. request.method? POST? ??, request.POST?? 'content'?? ?? ???
3. ?? ???? ??? request.user? ????, Post? id?? post_id??? ????? ? ??? ??
4. ? ???? content? ???? Comment?? ?? ? ??
5. ?? ?? ??? (Post Detail)? redirect??
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from post.forms import CommentForm, PostForm
from post.models import Post

__all__ = (
    'post_list',
    'post_detail',
    'post_like_toggle',
    'post_add',
    'post_delete',
)


@login_required
def post_list(request):
    posts = Post.visible.all()
    context = {
        'posts': posts,
    }
    return render(request, 'post/post-list.html', context)


@login_required
def post_detail(request, post_id):
    # ??? ??? post_id? ???? id? ?? Post?? ??? ??
    post = Post.objects.get(id=post_id)
    # Comment? ??? Form??? ??, ??
    comment_form = CommentForm()
    context = {
        'post': post,
        'comment_form': comment_form,
    }
    return render(request, 'post/post-detail.html', context)


@login_required
def post_add(request):
    def create_post_comment(file, comment_content):
        post = Post(
            author=request.user,
            photo=file,
        )
        post.save()

        if comment_content.strip() != '':
            post.add_comment(
                user=request.user,
                content=comment_content
            )

    if request.method == 'POST':
        # form_class = self.get_form_class()
        # form = self.get_form(PostForm)
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('photo')
            comment_content = form.cleaned_data.get('content', '').strip()

            for file in files:
                create_post_comment(file, comment_content)
            # post.comment_set.create(
            #     author=request.user,
            #     content=comment_content,
            # )
            return redirect('post:list')
    else:
        form = PostForm()
    context = {
        'post_add_form': form,
    }
    return render(request, 'post/post-add.html', context)


@login_required
def post_delete(request, post_id, db_delete=False):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        if post.author.id == request.user.id:
            if db_delete:
                post.delete()
            else:
                post.is_visible = False
                post.save()
        return redirect('post:list')


@login_required
def post_like_toggle(request, post_id):
    """
    1. post_detail.html? form? ?? ? ??
    2. ?? view(url)? post_like? ??? ?
    3. ??? ?? ? ??? PostLike??
    4. redirect
    """
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        post.toggle_like(user=request.user)
        return redirect('post:list')
