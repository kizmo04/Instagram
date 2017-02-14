from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import LoginForm


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
