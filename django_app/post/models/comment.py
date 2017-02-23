"""
1. Post모델 구현 (like_users빼고)
    photo에 ImageField사용
    pip install Pillow
2. PostLike모델 구현 (중간자 모델로 사용)
3. Post모델의 like_users필드 구현
4. Comment모델 구현
"""
from django.conf import settings
from django.db import models

from .post import Post

__all__ = (
    'Comment',
)


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Post[{}]\'s Comment[{}], Author[{}]'.format(
            self.post_id,
            self.id,
            self.author_id,
        )
