from member.models import MyUser

__all__ = (
    'make_dummy_users',
    'make_user_and_login',
)


def make_dummy_users():
    users = []

    for i in range(10):
        user = MyUser.objects.create_user(
            username='username{}'.format(i + 1),
            password='test_password'
        )
        users.append(user)
    return users
