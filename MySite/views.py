from django.shortcuts import render,redirect
from MySite import models

#返回登录页面
def login(request):
    return render(request, 'login.html')

#登录到主页
def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        #验证用户
        try:
            user = models.UserInfo.objects.filter(username__exact=username, password__exact=password,isenable__exact=1)
            if user:
                # 写入cookie
                request.session['IS_LOGIN'] = True
                request.session['USERNAME'] = username
                is_login = request.session.get('IS_LOGIN', False)
                if is_login:
                    # 跳转到角色验证页面
                     return redirect('/index/')
            else:
                # 返回登录页面
                return render(request, 'login.html')
        except:
            pass

#退出登录
def LoginExit(request):
    del request.session["USERNAME"]
    return render(request, 'login.html')

