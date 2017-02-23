from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from post.models import Post
from .forms import LoginForm, SignupForm, ProfileImageModelForm, SignUpModelForm


def login_view(request):
    """
    request.method == 'POST'일 때와
    아닐 때의 동작을 구분
    POST일 때는 authenticate, login을 거치는 로직을 실행
    GET일 때는 member/login.html을 render하여 return하도록 함
    :param request:
    :param user:
    :return:
    """

    if request.method == 'POST':
        # LoginForm 을 사용
        form = LoginForm(data=request.POST)
        if form.is_valid():
            # 전달되어온 POST데이터에서 'username'과 'password'키의 값들을 사용
            username = request.POST['username']
            password = request.POST['password']
            # authenticate의 인자로 POST로 전달받은 username, password를 사용
            user = authenticate(username=username, password=password)

            # 만약 인증이 정상적으로 완료되었다면
            # 해당하는 username, password에 일치하는 User객체가 존재할 경우
            if user is not None:
                # Django의 인증관리 시스템을 이용하여 세션을 관리해주기 위해 login()함수 사용
                login(request, user)
                # context = {
                #     'msg': 'Login success',
                # }
                return HttpResponseRedirect('http://www.google.com')
            # 인증에 실패하였다면 (username, password에 일치하는 User객체가 존재하지 않을경우)
            else:
                # context = {
                #     'msg': 'Login failed'
                # }
                # return HttpResponseRedirect('http://www.naver.com')
                form.add_error(None, 'ID or PW incorrect')
    # GET method로 요청이 올 경우
    else:
        # return render(request, 'member/login.html')
        form = LoginForm()

    context = {
        'form': form,
    }

    return render(request, 'member/login.html', context)


def signup_model_form_fbv(request):
    if request.method == 'POST':
        form = SignUpModelForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post:list')
    else:
        form = SignUpModelForm()
    context = {
        'form': form
    }
    return render(request, 'member/signup.html', context)


def signup_fbv(request):
    """
    회원가입 구현

    1. member/signup.html파일 생성
    2. signupForm 클래스 구현
    3. 해당 form을 사용해서 signup.html템플릿구성
    4. postㅎ요청을 받아 myuser객체를 생성 후 로그인
    5. 로그인 완료되면 post_list뷰로 이동
    :param request:
    :return:
    """

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # username = form.cleaned_data['username']
            # # password1 = form.cleaned_data['password1']
            # password2 = form.cleaned_data['password2']
            # email = form.cleaned_data['email']
            # gender = form.cleaned_data['gender']
            # nickname = form.cleaned_data['nickname']

            # if MyUser.objects.filter(username=username).exists():
            #     form.add_error('username', 'username already exists')
            # if password1 != password2:
            #     form.add_error('password1', 'Password1 and Password2 not equal')
            # else:

            # user = MyUser.objects.create_user(
            #     username=username,
            #     password=password2
            # )
            # user.email = email
            # user.gender = gender
            # user.nickname = nickname
            # user.save()

            # login(request, user)
            user = form.create_user()
            login(request, user)
            return redirect('post:list')
            # else:
            #     return render(request, 'member/signup.html', context)

    else:
        form = SignupForm()

        context = {
            'form': form,
        }
        return render(request, 'member/signup.html', context)


@login_required
def profile(request):
    """
    버튼 1개 (로그아웃이 존재하는 member/profile.html을 render 해주는 뷰

    자신의 게시물 수 , 자신의 팔로워 수 자신의 팔로우 수를 context로 전달출력
    :param request:
    :return:
    """
    post_count = Post.objects.filter(author=request.user).count()
    follower_count = request.user.follower_set.count()
    following_count = request.user.following.count()

    context = {
        'post_count': post_count,
        'follower_count': follower_count,
        'following_count': following_count,

    }
    return render(request, 'member/profile.html', context)


@login_required
def logout_fbv(request):
    logout(request)
    return redirect('member:login')


@login_required
def change_profile_image(request):
    """
    해당 유저의 프로필 이미지를 바꾼다
    0. 유저모델에 img_profile필드 추가 mig
    1. change_profile_image.html 작성
    2. profileImageForm생성
    3. 해당 Form을 템플릿에 렌더링
    4. request.method == 'POST'일때 request.FILES의 값을 이용해서 request.user의
    img profile을 변경 저장
    5. 처리 완료 후 member:profile로 이동
    6. profile.html에서 user의 프로필 이미지를 img 태그를 사용해서 보여줌 {{ MEDIA_URL }}
    :param request:
    :return:
    """

    if request.method == 'POST':
        form = ProfileImageModelForm(
            instance=request.user,
            data=request.POST,
            files=request.FILES)
        if form.is_valid():
            form.save()
            # username = request.user.username
            # user = MyUser.objects.get(username=username)
            # user.img_profile = request.FILES['image']
            # user.save()

            return redirect('member:profile')

    else:
        form = ProfileImageModelForm(instance=request.user)
    context = {
        'form': form,
    }

    return render(request, 'member/change-profile-image.html', context)
