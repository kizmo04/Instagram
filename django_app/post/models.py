from django.db import models

from member.models_backup import MyUser


class Post(models.Model):
    author = models.ForeignKey(MyUser)
    photo = models.ImageField(
        upload_to='post', blank=True)
    like_users = models.ManyToManyField(
        MyUser,
        through='PostLike',
        related_name='like_post_set',  # user에서 post로 역참조할때 씀

    )
    content = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Post{}'.format(self.id)

    def toggle_like(self, user):
        # 현재 인자로 전달된 user가 해당 Post(self)를 좋아요 한 적이 있는지 검사
        # pl_list = PostLike.objects.filter(post=self, user=user)
        pl_list = self.postlike_set.filter(user=user)
        # if pl_list.exists():
        #     # 중간자모델을 사용하기 때문에 remove나 create를 못 쓴다! 대신 아래 매서드 사용
        #     # 만약에 이미 좋아요를 했을 경우 해당 내역을 삭제
        #     pl_list.delete()
        # else:
        #     # 아직 내역이 없을 경우 생성해준다
        #     # 중간자모델을 사용하기 때문에 PostLike중간자 모델 매니저를 사용한다 create()대신
        #     PostLike.objects.create(post=self, user=user)

        # 파이썬 삼항연산자를 사용 ( True일경우 실행 구문 if 조건문 else False일경우 실행 구문)
        return self.postlike_set.create(user=user) if not pl_list.exists() else pl_list.delete()

    def add_comment(self, user, content):
        # 자신에게 연결된 comment객체의 역참조 매니저 (comment_set)로부터
        # create메서드 사용해 comment객체 생성
        return self.comment_set.create(
            user=user,
            content=content
        )

    @property
    def like_count(self):
        return self.like_users.count()

    @property
    def comment_count(self):
        return self.comment_set.count()


class Comment(models.Model):
    author = models.ForeignKey(MyUser)
    post = models.ForeignKey(Post)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Post[{}]\'s Comment[{}], Author[{}]'.format(
            self.post_id,
            self.id,
            self.author_id,
        )


class PostLike(models.Model):
    user = models.ForeignKey(MyUser)
    post = models.ForeignKey(Post)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('user', 'post'),
        )

    def __str__(self):
        return 'Post[{}]\'s Like[{}], User[{}]'.format(
            self.post_id,  # post_id는 Post모델을 역참조,PostLike.id와의 차이! -갔다오는것과 그냥가져오는것 db테이블에 post_id로 컬럼이 생긴다
            self.id,
            self.user_id,
        )
