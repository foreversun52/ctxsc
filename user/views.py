from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from main import models

# Create your views here.
def login(request):
    """登录"""
    if request.method == 'POST':
        back_dic = {'code': 1000, 'msg': '', 'url': ''}
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = auth.authenticate(username=username, password=password)
        if user_obj:
            # 保存用户登录状态
            auth.login(request, user_obj)
            back_dic['url'] = '/home/'
        else:
            back_dic['code'] = 2000
            back_dic['msg'] = '用户名或密码错误'
        # return JsonResponse(back_dic)
    return render(request, 'login.html', locals())


@login_required
def set_password(request, username):
    """修改密码"""
    user_obj = models.User.objects.filter(username=username).first()
    if request.is_ajax():
        back_dic = {'code': 1000, 'msg': ''}
        if request.method == 'POST':
            old_password = request.POST.get('oldpass')
            new_password = request.POST.get('newpass')
            confirm_password = request.POST.get('repass')
            # 校验两次密码是否一致
            if new_password == confirm_password:
                # 先校验旧密码是否正确
                is_right = user_obj.check_password(old_password)
                if is_right:
                    user_obj.set_password(new_password)
                    user_obj.save()
                    back_dic['url'] = '/user/login/'
                else:
                    back_dic['code'] = 2000
                    back_dic['msg'] = '原密码错误'
            else:
                back_dic['code'] = 3000
                back_dic['msg'] = '两次密码不一致'
            return JsonResponse(back_dic)
    return render(request, 'member-password.html', locals())


@login_required
def logout(request):
    # 删除用户session信息
    auth.logout(request)
    return redirect('/user/login/')
