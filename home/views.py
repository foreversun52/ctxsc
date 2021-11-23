from django.shortcuts import render

# Create your views here.
from datetime import datetime
from main import models
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from utils.mypage import Pagination,UserPagination,IssuePagination
from django.http import JsonResponse, HttpResponse, FileResponse
from utils.common import more_month, getDay
from openpyxl import Workbook
import xlrd
import xlwt
from xlrd import xldate_as_tuple
from django.db.models import Sum
from xlutils.copy import copy
from django.conf import settings
import os
import time
from utils.common import getYesterday, getToday, getMouth, getMonth, zdrang, getYear, more_month


@login_required
def home(request):
    """首页"""
    username = request.user.username
    user = models.User.objects.filter(username=username).first()
    user_count = models.User.objects.count()
    member_count = models.Customer.objects.count()
    product_count = models.ProductInfo.objects.count()
    packing_count = models.Packing.objects.count()
    material_count = models.Material.objects.count()
    date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return render(request, 'index.html', locals())


@login_required
def welcome(request):
    """欢迎页"""
    username = request.user.username
    user = models.User.objects.filter(username=username).first()
    user_count = models.User.objects.count()
    member_count = models.Customer.objects.count()
    product_count = models.ProductInfo.objects.count()
    packing_count = models.Packing.objects.count()
    material_count = models.Material.objects.count()
    date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return render(request, 'new/welcome.html', locals())


@login_required
def member_list(request):
    """客户列表"""
    user = models.User.objects.filter(username=request.user.username).first()

    if user.user_type == 1:
        user_list = models.Customer.objects.all()
        user_count = user_list.count()
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')
    # user_obj = Pagination(current_page=request.GET.get('page', 1), all_count=user_list.count())
    # page_queryset = user_list[user_obj.start:user_obj.end]

    return render(request, 'member_list.html', locals())


@login_required
def add_member(request):
    """添加新员工"""
    user = models.User.objects.filter(username=request.user.username).first()
    if user.user_type == 1:
        if request.is_ajax():
            back_dic = {'code': 1000, 'msg': ''}
            if request.method == 'POST':
                name = request.POST.get('name')
                mobile = request.POST.get('mobile')
                info = request.POST.get('mobile')
                member_obj = models.Customer.objects
                # 校验两次密码是否一致
                if not member_obj.filter(name=name):
                    day = datetime.today().date()
                    member_obj.create(name=name, mobile=mobile, customer_info=info, create_date=day)
                    back_dic['msg'] = '添加成功'
                else:
                    back_dic['code'] = 2000
                    back_dic['msg'] = '系统中已有同名的客户了，请起别名。'
            return JsonResponse(back_dic)
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')


@login_required
def add_material(request):
    """添加新材料 """
    user = models.User.objects.filter(username=request.user.username).first()
    if user.user_type == 1:
        if request.is_ajax():
            back_dic = {'code': 1000, 'msg': ''}
            if request.method == 'POST':
                name = request.POST.get('name')
                price = request.POST.get('price')
                material_obj = models.Material.objects
                if not material_obj.filter(material_name=name):
                    material_obj.create(material_name=name, material_price=price)
                    back_dic['msg'] = '添加成功'
                else:
                    back_dic['code'] = 2000
                    back_dic['msg'] = '系统中已有相同的材料了，请勿重复添加。'
            return JsonResponse(back_dic)
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')


@login_required
def edit_material(request, pk):
    """编辑材料信息 """
    user = models.User.objects.filter(username=request.user.username).first()
    if user.user_type == 1:
        if request.is_ajax():
            back_dic = {'code': 1000, 'msg': ''}
            if request.method == 'POST':
                name = request.POST.get('name')
                price = request.POST.get('price')
                material_obj = models.Material.objects.filter(pk=pk)
                if material_obj:
                    material_obj.update(material_name=name, material_price=price)
                    finish_list = models.FinishedProduct.objects.filter(productinfo__one_floor__material_type_id=pk)
                    print(finish_list)
                    for finish in finish_list:
                        ma_price = finish.material_price
                        gross_profit = finish.gross_profit
                        up_price = float(gross_profit) + float(ma_price) - float(price)
                        finish.gross_profit=up_price

                        finish.save()
                    back_dic['msg'] = '修改成功'
                else:
                    back_dic['code'] = 2000
                    back_dic['msg'] = "修改失败"
            return JsonResponse(back_dic)
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')


@login_required
def add_packing(request):
    """添加新包装 """
    user = models.User.objects.filter(username=request.user.username).first()
    if user.user_type == 1:
        if request.is_ajax():
            back_dic = {'code': 1000, 'msg': ''}
            if request.method == 'POST':
                name = request.POST.get('name')
                material_obj = models.Packing.objects
                # 校验两次密码是否一致
                if not material_obj.filter(packing_name=name):
                    material_obj.create(packing_name=name)
                    back_dic['msg'] = '添加成功'
                else:
                    back_dic['code'] = 2000
                    back_dic['msg'] = '系统中已有相同的规格了，请勿重复添加。'
            return JsonResponse(back_dic)
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')
    return render(request, 'packing-add.html', locals())


@login_required
def edit_member(request, pk):
    """编辑业务员信息"""
    user = models.User.objects.filter(username=request.user.username).first()
    member_obj = models.Customer.objects.filter(id=pk)

    memeber_info = member_obj.first()
    if user.user_type == 1:
        if request.is_ajax():
            back_dic = {'code': 1000, 'msg': ''}
            if request.method == 'POST':
                name = request.POST.get('name')
                mobile = request.POST.get('mobile')
                info = request.POST.get('info')
                # 校验两次密码是否一致
                if not member_obj:
                    back_dic['code'] = 2000
                    back_dic['msg'] = '修改失败，客户不存在！'
                else:
                    member_obj.update(name=name, mobile=mobile, customer_info=info)
                    back_dic['msg'] = '修改成功'
            return JsonResponse(back_dic)
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')


@login_required
def del_member(request, pk):
    """删除用户信息"""
    user = models.User.objects.filter(username=request.user.username).first()
    if user.user_type == 1:
        if request.is_ajax():
            back_dic = {'code': 1000, 'msg': ''}
            if request.method == 'POST':
                models.Customer.objects.filter(pk=pk).delete()
                back_dic['msg'] = '删除成功'
            else:
                back_dic['code'] = 2000
                back_dic['msg'] = '删除失败'
            return JsonResponse(back_dic)
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')


@login_required
def del_material(request, pk):
    """删除材料信息"""
    user = models.User.objects.filter(username=request.user.username).first()
    if user.user_type == 1:
        if request.is_ajax():
            back_dic = {'code': 1000, 'msg': ''}
            if request.method == 'POST':
                models.Material.objects.filter(pk=pk).delete()
                back_dic['msg'] = '删除成功'
            else:
                back_dic['code'] = 2000
                back_dic['msg'] = '删除失败'
            return JsonResponse(back_dic)
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')


@login_required
def del_packing(request, pk):
    """删除材料信息"""
    user = models.User.objects.filter(username=request.user.username).first()
    if user.user_type == 1:
        if request.is_ajax():
            back_dic = {'code': 1000, 'msg': ''}
            if request.method == 'POST':
                models.Packing.objects.filter(pk=pk).delete()
                back_dic['msg'] = '删除成功'
            else:
                back_dic['code'] = 2000
                back_dic['msg'] = '删除失败'
            return JsonResponse(back_dic)
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')



@login_required
def product_list(request):
    """产品信息列表"""
    user = models.User.objects.filter(username=request.user.username).first()
    user_obj_list = models.User.objects.all()
    customer_obj_list = models.Customer.objects.all()
    if user.user_type == 1:
        product_obj_list = models.ProductInfo.objects.all()
        packing_list = models.Packing.objects.filter()
        material_list = models.Material.objects.filter()
        product_obj_count = product_obj_list.count()
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')
    product_obj = Pagination(current_page=request.GET.get('page', 1), all_count=product_obj_count)
    page_queryset = product_obj_list[product_obj.start:product_obj.end]

    return render(request, 'product_list.html', locals())


@login_required
def add_product(request):
    """添加新的产品信息"""
    user = models.User.objects.filter(username=request.user.username).first()
    customer_obj_list = models.Customer.objects.all()
    user_obj_list = models.User.objects.all()
    if user.user_type == 1:
        if request.is_ajax():
            back_dic = {'code': 1000, 'msg': ''}
            if request.method == 'POST':
                print(request.POST)
                name = request.POST.get('name')
                product_name = request.POST.get('product_name')
                one_floor = request.POST.get('one_floor')
                two_floor = request.POST.get('two_floor')
                three_floor = request.POST.get('three_floor')
                finished = request.POST.get('finished')
                product_status = request.POST.get('product_status')
                product_img = request.FILES.get('file')
                create_date = request.POST.get('create_date')
                if not create_date:
                    create_date = '2020-10-01'
                file_path = os.path.join(settings.MEDIA_ROOT, 'product',)
                product_obj = models.ProductInfo.objects
                if not product_obj.filter(product_name=product_name):
                    one_floor_obj = models.OneFloor.objects.create(one_floor_user_id=one_floor)
                    two_floor_obj = models.TowFloor.objects.create(two_floor_user_id=two_floor)
                    three_floor_obj = models.ThreeFloor.objects.create(three_floor_user_id=three_floor)
                    finished_floor_obj = models.FinishedProduct.objects.create(finished_user_id=finished)

                    product_obj_status = product_obj.create(product_name=product_name, customer_name_id=int(name), one_floor_id=one_floor_obj.id, two_floor_id=two_floor_obj.id, three_floor_id=three_floor_obj.id, finished_product_id=finished_floor_obj.id, product_img=product_img, product_status=int(product_status), p_create_date=create_date)

                    if product_obj_status:
                        back_dic['msg'] = '添加成功'
                    else:
                        back_dic['code'] = 2000
                        back_dic['msg'] = '添加失败'
                else:
                    back_dic['code'] = 2000
                    back_dic['msg'] = '添加失败,该产品名已经存在'

            return JsonResponse(back_dic)
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");window.location.href="/home"</script>')


@login_required
def site(request):
    user = models.User.objects.filter(username=request.user.username).first()
    if user.user_type == 1:
        site_path = os.path.join(settings.BASE_DIR, 'utils', 'site.txt')
        with open(site_path, 'r') as fr:
            data = fr.read()
        site_dic = eval(data)
        txcb = site_dic['txcb']
        kjdfrg = site_dic['kjdfrg']
        if request.is_ajax():
            back_dic = {'code': 1000, 'msg': ''}
            if request.method == 'POST':
                txcb = request.POST.get('txcb')
                kjdfrg = request.POST.get('kjdfrg')
                new_dict = {'txcb':float(txcb),'kjdfrg':float(kjdfrg)}
                with open(site_path, 'w') as fw:
                    fw.write(str(new_dict))
                back_dic['msg'] = "修改完成"
                return JsonResponse(back_dic)
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')
    return render(request, 'site.html', locals())



@login_required
def edit_product(request, pk):
    """编辑已有的产品信息"""
    user = models.User.objects.filter(username=request.user.username).first()
    customer_obj_list = models.Customer.objects.all()
    user_obj_list = models.User.objects.all()
    product_info = models.ProductInfo.objects.filter(id=pk).first()
    if user.user_type == 1:
        if request.is_ajax():
            back_dic = {'code': 1000, 'msg': ''}
            if request.method == 'POST':

                name = request.POST.get('name', product_info.customer_name_id)
                product_name = request.POST.get('product_name', product_info.product_name)
                product_status = request.POST.get('product_status', product_info.product_status)
                product_img = request.FILES.get('file', product_info.product_img)
                create_date = request.POST.get('create_date', product_info.p_create_date)
                file_path = os.path.join(settings.MEDIA_ROOT, 'product')
                try:
                    product_obj = models.ProductInfo.objects
                    product_info.product_name = product_name
                    product_info.customer_name_id = int(name)
                    product_info.product_img = product_img
                    product_info.product_status = int(product_status)

                    if not create_date:
                        create_date = '2020-10-01'
                    product_info.p_create_date = create_date
                    product_info.save()

                    back_dic['msg'] = '修改成功'
                except Exception as e:
                    print(e)
                    back_dic['code'] = 2000
                    back_dic['msg'] = '修改失败'
            else:
                back_dic['code'] = 2000
                back_dic['msg'] = '非法请求'
            return JsonResponse(back_dic)
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')
    return render(request, 'order-edit.html', locals())


@login_required
def edit_product_info(request, pk):
    """编辑已有的产品信息"""
    user = models.User.objects.filter(username=request.user.username).first()
    material_list = models.Material.objects.filter()
    product_info = models.ProductInfo.objects.filter(id=pk).first()
    if user.user_type == 1:
        if request.is_ajax():
            back_dic = {'code': 1000, 'msg': ''}
            if request.method == 'POST':

                site_path = os.path.join(settings.BASE_DIR, 'utils', 'site.txt')
                with open(site_path, 'r') as fr:
                    data = fr.read()
                site_dic = eval(data)
                one_floor = request.POST.get('one_floor', product_info.one_floor.one_floor_user_id)

                material_height = request.POST.get('material_height', product_info.one_floor.material_height)
                material_thickness = request.POST.get('material_thickness', product_info.one_floor.material_thickness)
                material_id = request.POST.get('material_id', product_info.one_floor.material_type_id)
                power_time = request.POST.get('power_time', product_info.one_floor.power_time)
                pulling_long = request.POST.get('pulling_long', product_info.one_floor.pulling_long)
                shipment_num = request.POST.get('shipment_num', product_info.one_floor.shipment_num)
                slice_company = request.POST.get('slice_company', product_info.one_floor.slice_company)

                if material_thickness and material_height and pulling_long and shipment_num and power_time:
                    ton_num = int(1000000 / (float(material_height) / 10 * float(pulling_long) * 1.4 * float(
                        material_thickness) / 1000))
                    ton_nums = ton_num * float(shipment_num)
                    ton_slice_time = round(ton_num * float(power_time) / 3600, 2)
                    update_one = models.OneFloor.objects.filter(pk=product_info.one_floor_id).update(
                        one_floor_user_id=one_floor, material_height=material_height,
                        material_thickness=material_thickness, material_type_id=material_id, power_time=power_time,
                        pulling_long=pulling_long, shipment_num=shipment_num, slice_company=int(slice_company),
                        ton_num=ton_num, ton_nums=ton_nums, ton_slice_time=ton_slice_time)
                else:
                    update_one = False
                    back_dic['code'] = 2000
                    back_dic['msg'] = '修改失败，一楼参数有误'
                two_floor = request.POST.get('two_floor', product_info.two_floor.two_floor_user_id)
                knife_num = request.POST.get('knife_num', product_info.two_floor.knife_num)
                bed_num = request.POST.get('bed_num', product_info.two_floor.bed_num)
                bed_yield = request.POST.get('bed_yield', product_info.two_floor.bed_yield)
                bed_yield_comany = request.POST.get('bed_yield_comany', product_info.two_floor.bed_yield_comany)
                bed_price = request.POST.get('bed_price', product_info.two_floor.bed_price)

                two_packing_type = request.POST.get('two_packing_type', product_info.two_floor.two_packing_type)
                packing_num_choices = request.POST.get('packing_num_choices',
                                                       product_info.two_floor.packing_num_choices)
                two_packing_num_one = request.POST.get('two_packing_num_one',
                                                       product_info.two_floor.two_packing_num_one)
                two_packing_num_two = request.POST.get('two_packing_num_two',
                                                       product_info.two_floor.two_packing_num_two)
                two_packing_num_three = request.POST.get('two_packing_num_three',
                                                         product_info.two_floor.two_packing_num_three)
                two_packing_num_four = request.POST.get('two_packing_num_four',
                                                        product_info.two_floor.two_packing_num_four)
                packing_weight = request.POST.get('packing_weight', product_info.two_floor.packing_weight)
                two_packing_price = request.POST.get('two_packing_price', product_info.two_floor.two_packing_price)
                two_packing_nums = 0
                if int(packing_num_choices) == 1:
                    if two_packing_num_one and two_packing_num_two and two_packing_num_three and two_packing_num_four:
                        two_packing_nums = float(two_packing_num_one) * float(two_packing_num_two) * float(
                            two_packing_num_three) * float(two_packing_num_four)
                    else:
                        back_dic['code'] = 2000
                        back_dic['msg'] = '包装数量参数不可为空'

                update_two = models.TowFloor.objects.filter(pk=product_info.two_floor_id).update(
                    two_floor_user=two_floor, knife_num=knife_num, bed_num=bed_num, bed_yield=bed_yield,
                    bed_price=bed_price, bed_yield_comany=bed_yield_comany, two_packing_type_id = two_packing_type,
                    packing_num_choices=packing_num_choices, two_packing_num_one=two_packing_num_one,
                    two_packing_num_two=two_packing_num_two, two_packing_num_three=two_packing_num_three,
                    two_packing_num_four=two_packing_num_four, two_packing_nums=two_packing_nums,
                    packing_weight=packing_weight, two_packing_price=two_packing_price)
                three_floor = request.POST.get('three_floor', product_info.three_floor.three_floor_user_id)

                edge_price = request.POST.get('edge_price', product_info.three_floor.edge_price)

                three_packing_type = request.POST.get('three_packing_type', product_info.three_floor.three_packing_type)

                three_packing_num_one = request.POST.get('three_packing_num_one',
                                                         product_info.three_floor.three_packing_num_one)
                three_packing_num_two = request.POST.get('three_packing_num_two',
                                                         product_info.three_floor.three_packing_num_two)
                three_packing_num_three = request.POST.get('three_packing_num_three',
                                                           product_info.three_floor.three_packing_num_three)
                three_packing_num_four = request.POST.get('three_packing_num_four',
                                                          product_info.three_floor.three_packing_num_four)
                three_packing_price = request.POST.get('three_packing_price',
                                                       product_info.three_floor.three_packing_price)
                three_packing_nums = 0
                if three_packing_num_one and three_packing_num_two and three_packing_num_three and three_packing_num_four:
                    three_packing_nums = float(three_packing_num_one) * float(three_packing_num_two) * float(
                        three_packing_num_three) * float(three_packing_num_four)
                else:
                    back_dic['code'] = 2000
                    back_dic['msg'] = '包装数量参数不可为空'

                update_three = models.ThreeFloor.objects.filter(pk=product_info.three_floor_id).update(
                    three_floor_user=three_floor,
                    three_packing_type_id=int(three_packing_type),
                    edge_price=edge_price,
                    three_packing_num_one=three_packing_num_one,
                    three_packing_num_three=three_packing_num_three,
                    three_packing_num_two=three_packing_num_two,
                    three_packing_num_four=three_packing_num_four,
                    three_packing_nums=three_packing_nums,
                    three_packing_price=three_packing_price)
                finished_user_id = request.POST.get('finished_user', product_info.finished_product.finished_user_id)
                sheet_weight = request.POST.get('sheet_weight', product_info.finished_product.sheet_weight)
                slice_weight = request.POST.get('slice_weight', product_info.finished_product.slice_weight)
                individual_weight = request.POST.get('individual_weight',
                                                     product_info.finished_product.individual_weight)
                leftovers_weight = request.POST.get('leftovers_weight', product_info.finished_product.leftovers_weight)
                # leftovers_percentage = request.POST.get('leftovers_percentage', product_info.finished_product.leftovers_percentage)
                product_price = request.POST.get('product_price', product_info.finished_product.product_price)
                product_price_choices = request.POST.get('product_price_choices',
                                                         product_info.finished_product.product_price_choices)
                material_price = request.POST.get('material_price', product_info.finished_product.material_price)
                # gross_profit = request.POST.get('gross_profit', product_info.finished_product.gross_profit)
                if sheet_weight and leftovers_weight:
                    leftovers_percentage = round(float(leftovers_weight) * 100 / float(sheet_weight), 2)
                    txcb = site_dic.get('txcb')
                    kjdfrg = site_dic.get('kjdfrg')
                    kjcb = round(float(ton_slice_time) * kjdfrg, 2)
                    ccgz = round(float(ton_nums) / float(knife_num) / float(bed_num) * float(bed_price), 2)
                    bzgz = round(float(ton_nums) / float(three_packing_nums) * float(three_packing_price), 2)
                    cbgz = round(float(ton_nums) * float(edge_price), 2)
                    fl = round(1000000 * float(leftovers_percentage) * 0.005 / 100, 2)
                    zcb = round(float(material_price) + txcb + kjcb + ccgz + bzgz + cbgz - fl, 2)
                    dgcpcb = zcb / float(ton_nums)
                    cpgjcb = 1000 / float(slice_weight) * dgcpcb
                    product_price = float(product_price)
                    gross_profit = round((float(product_price) - dgcpcb) * float(ton_nums), 2)
                    finished = models.FinishedProduct.objects.filter(pk=product_info.finished_product_id).update(
                        finished_user_id=finished_user_id, sheet_weight=sheet_weight, slice_weight=slice_weight,
                        individual_weight=individual_weight, leftovers_weight=leftovers_weight,
                        leftovers_percentage=leftovers_percentage, product_price=product_price,
                        product_price_choices=product_price_choices, material_price=material_price,
                        gross_profit=gross_profit)
                else:
                    finished = False
                    back_dic['code'] = 2000
                    back_dic['msg'] = '修改失败，成品数据有误'
                if update_one and update_two and update_three and finished:
                    back_dic['msg'] = '修改成功'
                else:
                    back_dic['code'] = 2000
                    back_dic['msg'] = '修改失败'
            else:
                back_dic['code'] = 2000
                back_dic['msg'] = '非法请求'
            return JsonResponse(back_dic)
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')


@login_required
def del_product(request, pk):
    """删除产品信息"""
    user = models.User.objects.filter(username=request.user.username).first()
    if user.user_type == 1:
        if request.is_ajax():
            back_dic = {'code': 1000, 'msg': ''}
            if request.method == 'POST':
                product = models.ProductInfo.objects.filter(pk=pk)
                product_obj = product.first()
                models.OneFloor.objects.filter(id = product_obj.one_floor_id).delete()
                models.TowFloor.objects.filter(id = product_obj.two_floor_id).delete()
                models.ThreeFloor.objects.filter(id = product_obj.three_floor_id).delete()
                models.FinishedProduct.objects.filter(id = product_obj.finished_product_id).delete()
                product.delete()
                back_dic['msg'] = '删除成功'
            else:
                back_dic['code'] = 2000
                back_dic['msg'] = '删除失败'
            return JsonResponse(back_dic)
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')


@login_required
def one_floor_info_list(request):
    user = models.User.objects.filter(username=request.user.username).first()
    if user.user_type == 1:
        product_obj_list = models.ProductInfo.objects.all()
        customer_obj_list = models.Customer.objects.all()
        user_obj_list = models.User.objects.all()
        material_list = models.Material.objects.filter()
        product_obj_count = product_obj_list.count()
    elif user.user_type == 2:
        product_obj_list = models.ProductInfo.objects.filter(one_floor__one_floor_user_id=user.id)
        customer_obj_list = models.Customer.objects.all()
        user_obj_list = models.User.objects.all()
        material_list = models.Material.objects.filter()
        product_obj_count = product_obj_list.count()
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')
    product_obj = Pagination(current_page=request.GET.get('page', 1), all_count=product_obj_count)
    page_queryset = product_obj_list[product_obj.start:product_obj.end]

    return render(request, 'one_floor_list.html', locals())


@login_required
def two_floor_info_list(request):
    user = models.User.objects.filter(username=request.user.username).first()

    if user.user_type == 1:
        product_obj_list = models.ProductInfo.objects.all()
        product_obj_count = product_obj_list.count()
        customer_obj_list = models.Customer.objects.all()
        user_obj_list = models.User.objects.all()
        packing_list = models.Packing.objects.filter()
    elif user.user_type == 2:
        product_obj_list = models.ProductInfo.objects.filter(two_floor__two_floor_user_id=user.id)
        product_obj_count = product_obj_list.count()
        customer_obj_list = models.Customer.objects.all()
        user_obj_list = models.User.objects.all()
        packing_list = models.Packing.objects.filter()
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')
    product_obj = Pagination(current_page=request.GET.get('page', 1), all_count=product_obj_count)
    page_queryset = product_obj_list[product_obj.start:product_obj.end]

    return render(request, 'two_floor_list.html', locals())


@login_required
def three_floor_info_list(request):
    user = models.User.objects.filter(username=request.user.username).first()

    if user.user_type == 1:
        product_obj_list = models.ProductInfo.objects.all()
        customer_obj_list = models.Customer.objects.all()
        user_obj_list = models.User.objects.all()
        packing_list = models.Packing.objects.filter()
        product_obj_count = product_obj_list.count()
    elif user.user_type == 2:
        product_obj_list = models.ProductInfo.objects.filter(three_floor__three_floor_user_id=user.id)
        product_obj_count = product_obj_list.count()
        customer_obj_list = models.Customer.objects.all()
        user_obj_list = models.User.objects.all()
        packing_list = models.Packing.objects.filter()
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')
    product_obj = Pagination(current_page=request.GET.get('page', 1), all_count=product_obj_count)
    page_queryset = product_obj_list[product_obj.start:product_obj.end]

    return render(request, 'three_floor_list.html', locals())


@login_required
def finished_info_list(request):
    user = models.User.objects.filter(username=request.user.username).first()
    if user.user_type == 1:
        product_obj_list = models.ProductInfo.objects.all()
        product_obj_count = product_obj_list.count()
        customer_obj_list = models.Customer.objects.all()
        user_obj_list = models.User.objects.all()
        packing_list = models.Packing.objects.filter()
    elif user.user_type == 2:
        product_obj_list = models.ProductInfo.objects.filter(finished_product__finished_user_id=user.id)
        product_obj_count = product_obj_list.count()
        customer_obj_list = models.Customer.objects.all()
        user_obj_list = models.User.objects.all()
        packing_list = models.Packing.objects.filter()
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')
    product_obj = Pagination(current_page=request.GET.get('page', 1), all_count=product_obj_count)
    page_queryset = product_obj_list[product_obj.start:product_obj.end]

    return render(request, 'finished_list.html', locals())


@login_required
def edit_one_floor_info(request, pk):
    """编辑已有的产品信息"""
    user = models.User.objects.filter(username=request.user.username).first()

    product_info = models.ProductInfo.objects.filter(id=pk).first()
    if user.user_type == 1 or user.user_type == 2:
        if request.is_ajax():
            back_dic = {'code': 1000, 'msg': ''}
            if request.method == 'POST':
                print(request.POST)
                # one_floor = request.POST.get('one_floor', product_info.one_floor.one_floor_user_id)
                # product_name = request.POST.get('product_name', product_info.product_name)
                material_height = request.POST.get('material_height', product_info.one_floor.material_height)
                material_thickness = request.POST.get('material_thickness', product_info.one_floor.material_thickness)
                material_id = request.POST.get('material_id', product_info.one_floor.material_type_id)
                power_time = request.POST.get('power_time', product_info.one_floor.power_time)
                pulling_long = request.POST.get('pulling_long', product_info.one_floor.pulling_long)
                shipment_num = request.POST.get('shipment_num', product_info.one_floor.shipment_num)
                slice_company = request.POST.get('slice_company', product_info.one_floor.slice_company)

                if material_thickness and material_height and pulling_long and shipment_num and power_time:
                    ton_num = int(1000000 / (float(material_height) / 10 * float(pulling_long) * 1.4 * float(material_thickness) / 1000))
                    ton_nums = ton_num * float(shipment_num)
                    ton_slice_time = round(ton_num * float(power_time) / 3600, 2)
                    update_one = models.OneFloor.objects.filter(pk=product_info.one_floor_id).update(material_height=material_height, material_thickness=material_thickness, material_type_id=material_id, power_time=power_time, pulling_long=pulling_long, shipment_num=shipment_num,slice_company=int(slice_company), ton_num=ton_num, ton_nums=ton_nums,ton_slice_time=ton_slice_time)
                    if update_one:
                        back_dic['msg'] = '修改成功'
                    else:
                        back_dic['code'] = 2000
                        back_dic['msg'] = '修改失败'
                else:
                    back_dic['code'] = 2000
                    back_dic['msg'] = '必要参数不能为空'
            else:
                back_dic['code'] = 2000
                back_dic['msg'] = '非法请求'
            return JsonResponse(back_dic)
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')


@login_required
def edit_two_floor_info(request, pk):
    """编辑已有的产品信息"""
    user = models.User.objects.filter(username=request.user.username).first()
    customer_obj_list = models.Customer.objects.all()
    user_obj_list = models.User.objects.all()
    packing_list = models.Packing.objects.filter()
    product_info = models.ProductInfo.objects.filter(id=pk).first()
    if user.user_type == 1 or user.user_type == 2:
        if request.is_ajax():
            back_dic = {'code': 1000, 'msg': ''}
            if request.method == 'POST':
                print(request.POST)
                # two_floor = request.POST.get('two_floor', product_info.two_floor.two_floor_user_id)
                # product_name = request.POST.get('product_name', product_info.product_name)
                knife_num = request.POST.get('knife_num', product_info.two_floor.knife_num)
                bed_num = request.POST.get('bed_num', product_info.two_floor.bed_num)
                bed_yield = request.POST.get('bed_yield', product_info.two_floor.bed_yield)
                bed_yield_comany = request.POST.get('bed_yield_comany', product_info.two_floor.bed_yield_comany)
                bed_price = request.POST.get('bed_price', product_info.two_floor.bed_price)
                two_packing_type = request.POST.get('two_packing_type', product_info.two_floor.two_packing_type)
                packing_num_choices = request.POST.get('packing_num_choices', product_info.two_floor.packing_num_choices)
                two_packing_num_one = request.POST.get('two_packing_num_one', product_info.two_floor.two_packing_num_one)
                two_packing_num_two = request.POST.get('two_packing_num_two', product_info.two_floor.two_packing_num_two)
                two_packing_num_three = request.POST.get('two_packing_num_three', product_info.two_floor.two_packing_num_three)
                two_packing_num_four = request.POST.get('two_packing_num_four', product_info.two_floor.two_packing_num_four)
                packing_weight = request.POST.get('packing_weight', product_info.two_floor.packing_weight)
                two_packing_price = request.POST.get('two_packing_price', product_info.two_floor.two_packing_price)
                two_packing_nums = 0
                if int(packing_num_choices) == 1:
                    if two_packing_num_one and two_packing_num_two and two_packing_num_three and two_packing_num_four:
                        two_packing_nums = float(two_packing_num_one) * float(two_packing_num_two) * float(two_packing_num_three) * float(two_packing_num_four)
                    else:
                        back_dic['code'] = 2000
                        back_dic['msg'] = '包装数量参数不可为空'

                update_two = models.TowFloor.objects.filter(id=product_info.two_floor_id).update(knife_num=knife_num, bed_num=bed_num, bed_yield=bed_yield, bed_price=bed_price, bed_yield_comany=bed_yield_comany, two_packing_type_id = two_packing_type, packing_num_choices=packing_num_choices, two_packing_num_one=two_packing_num_one,two_packing_num_two=two_packing_num_two,two_packing_num_three=two_packing_num_three,two_packing_num_four=two_packing_num_four,two_packing_nums=two_packing_nums, packing_weight=packing_weight, two_packing_price=two_packing_price)
                if update_two:
                    back_dic['msg'] = '修改成功'
                else:
                    back_dic['code'] = 2000
                    back_dic['msg'] = '修改失败'
            else:
                back_dic['code'] = 2000
                back_dic['msg'] = '非法请求'
            return JsonResponse(back_dic)
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')
    return render(request, 'two_floor_list.html', locals())


@login_required
def edit_three_floor_info(request, pk):
    """编辑已有的产品信息"""
    user = models.User.objects.filter(username=request.user.username).first()
    product_info = models.ProductInfo.objects.filter(id=pk).first()
    if user.user_type == 1 or user.user_type == 2:
        if request.is_ajax():
            back_dic = {'code': 1000, 'msg': ''}
            if request.method == 'POST':
                edge_price = request.POST.get('edge_price', product_info.three_floor.edge_price)
                three_packing_type = request.POST.get('three_packing_type', product_info.three_floor.three_packing_type)
                three_packing_num_one = request.POST.get('three_packing_num_one',product_info.three_floor.three_packing_num_one)
                three_packing_num_two = request.POST.get('three_packing_num_two', product_info.three_floor.three_packing_num_two)
                three_packing_num_three = request.POST.get('three_packing_num_three', product_info.three_floor.three_packing_num_three)
                three_packing_num_four = request.POST.get('three_packing_num_four', product_info.three_floor.three_packing_num_four)
                three_packing_price = request.POST.get('three_packing_price',product_info.three_floor.three_packing_price)
                three_packing_nums = 0
                if three_packing_num_one and three_packing_num_two and three_packing_num_three and three_packing_num_four:
                    three_packing_nums = float(three_packing_num_one) * float(three_packing_num_two) * float(three_packing_num_three) * float(three_packing_num_four)
                else:
                    back_dic['code'] = 2000
                    back_dic['msg'] = '包装数量参数不可为空'

                update_three = models.ThreeFloor.objects.filter(pk=product_info.three_floor_id).update(
                    three_packing_type_id=three_packing_type,
                    edge_price=edge_price,
                    three_packing_num_one=three_packing_num_one,
                    three_packing_num_three=three_packing_num_three,
                    three_packing_num_two=three_packing_num_two,
                    three_packing_num_four=three_packing_num_four,
                    three_packing_nums=three_packing_nums,
                    three_packing_price=three_packing_price)
                if update_three:
                    back_dic['msg'] = '修改成功'
                else:
                    back_dic['code'] = 2000
                    back_dic['msg'] = '修改失败'
            else:
                back_dic['code'] = 2000
                back_dic['msg'] = '非法请求'
            return JsonResponse(back_dic)
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')


@login_required
def edit_finished_info(request, pk):
    """编辑已有的产品信息"""
    user = models.User.objects.filter(username=request.user.username).first()
    product_info = models.ProductInfo.objects.filter(id=pk).first()
    site_path = os.path.join(settings.BASE_DIR, 'utils', 'site.txt')
    with open(site_path, 'r') as fr:
        data = fr.read()
    site_dic = eval(data)
    if user.user_type == 1 or user.user_type == 2:
        if request.is_ajax():
            back_dic = {'code': 1000, 'msg': ''}
            if request.method == 'POST':
                # finished_user_id = request.POST.get('finished_user', product_info.finished_product.finished_user_id)
                sheet_weight = request.POST.get('sheet_weight', product_info.finished_product.sheet_weight)
                slice_weight = request.POST.get('slice_weight', product_info.finished_product.slice_weight)
                individual_weight = request.POST.get('individual_weight', product_info.finished_product.individual_weight)
                leftovers_weight = request.POST.get('leftovers_weight', product_info.finished_product.leftovers_weight)
                # leftovers_percentage = request.POST.get('leftovers_percentage', product_info.finished_product.leftovers_percentage)
                product_price = request.POST.get('product_price', product_info.finished_product.product_price)
                product_price_choices = request.POST.get('product_price_choices', product_info.finished_product.product_price_choices)
                material_price = request.POST.get('material_price', product_info.one_floor.material_type.material_price)
                # gross_profit = request.POST.get('gross_profit', product_info.finished_product.gross_profit)
                if sheet_weight and leftovers_weight:
                    leftovers_percentage = round(float(leftovers_weight)*100/float(sheet_weight), 2)
                    txcb = site_dic.get('txcb')
                    kjdfrg = site_dic.get('kjdfrg')
                    kjcb = round(float(product_info.one_floor.ton_slice_time) * kjdfrg, 2)
                    ccgz = round(float(product_info.one_floor.ton_nums) / float(product_info.two_floor.knife_num)  / float(product_info.two_floor.bed_num) * float(product_info.two_floor.bed_price), 2)
                    bzgz = round(float(product_info.one_floor.ton_nums) / float(product_info.three_floor.three_packing_nums) * float(product_info.three_floor.three_packing_price), 2)
                    cbgz = round(float(product_info.one_floor.ton_nums) * float(product_info.three_floor.edge_price), 2)
                    fl = round(1000000 * float(leftovers_percentage) * 0.005 / 100, 2)
                    zcb = float(material_price)+txcb+kjcb+ccgz+bzgz+cbgz-fl
                    dgcpcb = zcb / float(product_info.one_floor.ton_nums)
                    cpgjcb = 1000 / float(slice_weight) * dgcpcb
                    product_price = float(product_price)
                    gross_profit = round((float(product_price)-dgcpcb)*float(product_info.one_floor.ton_nums), 2)
                    finished = models.FinishedProduct.objects.filter(pk=product_info.finished_product_id).update(sheet_weight=sheet_weight, slice_weight=slice_weight, individual_weight=individual_weight, leftovers_weight=leftovers_weight, leftovers_percentage=leftovers_percentage, product_price=product_price, product_price_choices=product_price_choices, material_price=material_price, gross_profit=gross_profit)
                    if finished:
                        back_dic['msg'] = '修改成功'
                    else:
                        back_dic['code'] = 2000
                        back_dic['msg'] = '修改失败'
                else:
                    back_dic['code'] = 2000
                    back_dic['msg'] = '必要参数不可为空'
                    back_dic['msg'] = '修改失败'
            else:
                back_dic['code'] = 2000
                back_dic['msg'] = '非法请求'
            return JsonResponse(back_dic)
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')


@login_required
def material_info(request):
    user = models.User.objects.filter(username=request.user.username).first()

    if user.user_type == 1:
        material_obj_list = models.Material.objects.all()
        material_obj_count = material_obj_list.count()
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')
    material_obj = Pagination(current_page=request.GET.get('page', 1), all_count=material_obj_count)
    page_queryset = material_obj_list[material_obj.start:material_obj.end]

    return render(request, 'material_list.html', locals())


@login_required
def user_info(request):
    user = models.User.objects.filter(username=request.user.username).first()

    if user.user_type == 1:
        user_obj_list = models.User.objects.all()
        user_obj_count = user_obj_list.count()
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')
    user_obj = Pagination(current_page=request.GET.get('page', 1), all_count=user_obj_count)
    page_queryset = user_obj_list[user_obj.start:user_obj.end]

    return render(request, 'user_list.html', locals())


@login_required
def add_user(request):
    """添加新员工"""
    user = models.User.objects.filter(username=request.user.username).first()
    if user.user_type == 1:
        if request.is_ajax():
            back_dic = {'code': 1000, 'msg': ''}
            if request.method == 'POST':
                username = request.POST.get('username')
                password = request.POST.get('password')
                user_type = request.POST.get('user_type')
                userr_obj = models.User.objects

                if not userr_obj.filter(username=username):
                    day = datetime.now()
                    userr_obj.create_user(username=username, password=password, user_type=user_type, date_joined=day)
                    back_dic['msg'] = '添加成功'
                else:
                    back_dic['code'] = 2000
                    back_dic['msg'] = '系统中已有同名员工。'
            return JsonResponse(back_dic)
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')


@login_required
def edit_user(request, pk):
    """编辑员工信息"""
    user = models.User.objects.filter(username=request.user.username).first()
    member_obj = models.User.objects.filter(id=pk).first()
    if user.user_type == 1:
        if request.is_ajax():
            back_dic = {'code': 1000, 'msg': ''}
            if request.method == 'POST':
                password = request.POST.get('password')
                re_password = request.POST.get('re_password')
                user_type = request.POST.get('user_type')
                # 校验两次密码是否一致
                if not member_obj:
                    back_dic['code'] = 2000
                    back_dic['msg'] = '修改失败，用户不存在！'
                else:
                    member_obj.set_password(password)
                    member_obj.user_type = user_type
                    member_obj.save()
                    back_dic['msg'] = '修改成功'
            return JsonResponse(back_dic)
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')


@login_required
def del_user(request, pk):
    """删除用户信息"""
    user = models.User.objects.filter(username=request.user.username).first()
    if user.user_type == 1:
        if request.is_ajax():
            back_dic = {'code': 1000, 'msg': ''}
            if request.method == 'POST':
                models.User.objects.filter(pk=pk).delete()
                back_dic['msg'] = '删除成功'
            else:
                back_dic['code'] = 2000
                back_dic['msg'] = '删除失败'
            return JsonResponse(back_dic)
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')


@login_required
def packing_info(request):
    user = models.User.objects.filter(username=request.user.username).first()

    if user.user_type == 1:
        packing_obj_list = models.Packing.objects.all()
        packing_obj_count = packing_obj_list.count()
    else:
        return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')
    packing_obj = Pagination(current_page=request.GET.get('page', 1), all_count=packing_obj_count)
    page_queryset = packing_obj_list[packing_obj.start:packing_obj.end]

    return render(request, 'packing_list.html', locals())

#
# @login_required
# def set_password(request, username):
#     """修改员工密码"""
#     user = models.User.objects.filter(username=request.user.username).first()
#     if user.user_type == 1 or user.user_type == 2:
#         user_obj = models.User.objects.filter(username=username).first()
#         if request.is_ajax():
#             back_dic = {'code': 1000, 'msg': ''}
#             if request.method == 'POST':
#                 new_password = request.POST.get('new_pwd')
#                 confirm_password = request.POST.get('new_repwd')
#                 # 校验两次密码是否一致
#                 if new_password == confirm_password:
#                     user_obj.set_password(new_password)
#                     user_obj.save()
#                     back_dic['url'] = '/user/login/'
#                     back_dic['msg'] = '密码修改成功'
#                 else:
#                     back_dic['code'] = 3000
#                     back_dic['msg'] = '两次密码不一致'
#             return JsonResponse(back_dic)
#     else:
#         return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')
#     return render(request, 'home/set_password.html', locals())


# @login_required
# def branch(request):
#     """机构管理"""
#     user = models.User.objects.filter(username=request.user.username).first()
#     branch = request.GET.get('branch')
#     if user.user_type == 1:
#         if branch:
#             page_queryset = models.Branch.objects.filter(is_delete=0, name__contains=branch).order_by('sort')
#         else:
#             page_queryset = models.Branch.objects.filter(is_delete=0).order_by('sort')
#     else:
#         return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')
#     return render(request, 'home/branch_list.html', locals())
#
#
# @login_required
# def branch_data_list(request):
#     """机构数据"""
#     user = models.User.objects.filter(username=request.user.username).first()
#     if user.user_type == 1:
#         data_type = request.GET.get('data_type', 'issue')
#         date_frame = request.GET.get('date_frame', 'yesterday')
#         tag = request.GET.get('tag')
#         start = request.GET.get('date_frame')
#         branch_list = models.Branch.objects.filter(is_show=True)
#         branch_data_dict = {}
#         year = getYear()
#         now_month = getMonth()
#         before_month = getMonth() - 1
#         data = {}
#         re_type = ''
#         if tag:
#             date_frame = 'search'
#         if date_frame == 'search':
#             if data_type == 'issue':
#                 re_type = 'yesterday_issue'
#                 for branch in branch_list:
#                     data = {}
#                     if branch.id != branch.parent_id:
#                         user_branch = models.User.objects.filter(branch_name_id=branch.id)
#
#                         issue_date = start
#                         issue_num = models.Issue.objects.filter(user__in=user_branch,
#                                                                 created_time=issue_date).count()
#
#                         data['date'] = issue_date
#                         data['num'] = issue_num
#                         branch_data_dict[branch.name] = data
#             elif data_type == 'reissue':
#                 re_type = 'yesterday_reissue'
#                 for branch in branch_list:
#                     data = {}
#                     if branch.id != branch.parent_id:
#                         user_branch = models.User.objects.filter(branch_name_id=branch.id)
#                         reissue_date = start
#                         reissue_num = models.Reissue.objects.filter(user_re_id__in=user_branch,
#                                                                         cjsj=reissue_date).count()
#
#                         data['date'] = reissue_date
#                         data['num'] = reissue_num
#                         branch_data_dict[branch.name] = data
#             elif data_type == 'machine':
#                 re_type = 'yesterday_machine'
#                 for branch in branch_list:
#                     data = {}
#                     if branch.id != branch.parent_id:
#                         user_branch = models.User.objects.filter(branch_name_id=branch.id)
#
#                         machine_date = start
#                         machine_num = models.Activate.objects.filter(machine_id__machine_num__user__in=user_branch,
#                                                                          cash_state='已返现',
#                                                                          activate_date=machine_date).count()
#
#                         data['date'] = machine_date
#                         data['num'] = machine_num
#                         branch_data_dict[branch.name] = data
#             elif data_type == 'order':
#                 re_type = 'yesterday_order'
#                 for branch in branch_list:
#                     data = {}
#                     if branch.id != branch.parent_id:
#                         user_branch = models.User.objects.filter(branch_name_id=branch.id)
#                         order_obj = models.Order.objects.filter(
#                             terminal_num__machine_num__user__in=user_branch).order_by('-transaction_time')
#                         if order_obj:
#                             order_date = start
#                             order_num = order_obj.filter(transaction_time=order_date).aggregate(money_sum=Sum('money'))[
#                                 'money_sum']
#                             ordernum_num = order_obj.filter(transaction_time=order_date).count()
#                         data['date'] = order_date
#                         data['num'] = order_num
#                         data['ordernum_num'] = ordernum_num
#                         branch_data_dict[branch.name] = data
#         if date_frame == 'yesterday':
#             if data_type == 'issue':
#                 re_type = 'yesterday_issue'
#                 for branch in branch_list:
#                     data = {}
#                     if branch.id != branch.parent_id:
#                         user_branch = models.User.objects.filter(branch_name_id=branch.id)
#                         issue_date = models.Issue.objects.filter(user__in=user_branch).order_by('-created_time')
#                         if issue_date:
#                             issue_date = issue_date.first().created_time
#                             issue_num = models.Issue.objects.filter(user__in=user_branch,
#                                                                     created_time=issue_date).count()
#                         else:
#                             issue_num = 0
#                         data['date'] = issue_date
#                         data['num'] = issue_num
#                         branch_data_dict[branch.name] = data
#             elif data_type == 'reissue':
#                 re_type = 'yesterday_reissue'
#                 for branch in branch_list:
#                     data = {}
#                     if branch.id != branch.parent_id:
#                         user_branch = models.User.objects.filter(branch_name_id=branch.id)
#                         reissue_date = models.Reissue.objects.filter(user_re_id__in=user_branch).order_by('-cjsj')
#                         if reissue_date:
#                             reissue_date = reissue_date.first().cjsj
#                             reissue_num = models.Reissue.objects.filter(user_re_id__in=user_branch,
#                                                                         cjsj=reissue_date).count()
#                         else:
#                             reissue_date = '无'
#                             reissue_num = 0
#                         data['date'] = reissue_date
#                         data['num'] = reissue_num
#                         branch_data_dict[branch.name] = data
#             elif data_type == 'machine':
#                 re_type = 'yesterday_machine'
#                 for branch in branch_list:
#                     data = {}
#                     if branch.id != branch.parent_id:
#                         user_branch = models.User.objects.filter(branch_name_id=branch.id)
#                         machine_date = models.Activate.objects.filter(
#                             machine_id__machine_num__user__in=user_branch).order_by('-activate_date')
#                         if machine_date:
#                             machine_date = machine_date.first().activate_date
#                             machine_num = models.Activate.objects.filter(machine_id__machine_num__user__in=user_branch,
#                                                                          cash_state='已返现',
#                                                                          activate_date=machine_date).count()
#                         else:
#                             machine_num = 0
#                         data['date'] = machine_date
#                         data['num'] = machine_num
#                         branch_data_dict[branch.name] = data
#             elif data_type == 'order':
#                 re_type = 'yesterday_order'
#                 for branch in branch_list:
#                     data = {}
#                     if branch.id != branch.parent_id:
#                         user_branch = models.User.objects.filter(branch_name_id=branch.id)
#                         order_obj = models.Order.objects.filter(
#                             terminal_num__machine_num__user__in=user_branch).order_by('-transaction_time')
#                         if order_obj:
#                             order_date = order_obj.first().transaction_time
#                             order_num = order_obj.filter(transaction_time=order_date).aggregate(money_sum=Sum('money'))[
#                                 'money_sum']
#                             ordernum_num = order_obj.filter(transaction_time=order_date).count()
#                         else:
#                             order_num = 0
#                             ordernum_num = 0
#                         data['date'] = order_date
#                         data['num'] = order_num
#                         data['ordernum_num'] = ordernum_num
#                         branch_data_dict[branch.name] = data
#         elif date_frame == 'month':
#             if data_type == 'issue':
#                 re_type = 'month_issue'
#                 for branch in branch_list:
#                     data = {}
#                     if branch.id != branch.parent_id:
#                         user_branch = models.User.objects.filter(branch_name_id=branch.id)
#                         issue_num = models.Issue.objects.filter(user_id__in=user_branch, created_time__year=year,
#                                                                 created_time__month=now_month).count()
#                         data['date'] = f'{year}年{now_month}月'
#                         data['num'] = issue_num
#                         branch_data_dict[branch.name] = data
#             elif data_type == 'reissue':
#                 re_type = 'month_reissue'
#                 for branch in branch_list:
#                     data = {}
#                     if branch.id != branch.parent_id:
#                         user_branch = models.User.objects.filter(branch_name_id=branch.id)
#                         reissue_num = models.Reissue.objects.filter(user_re_id__in=user_branch, cjsj__year=year,
#                                                                     cjsj__month=now_month).count()
#                         qs_num = models.Reissue.objects.filter(user_re_id__in=user_branch, cjsj__year=year,
#                                                                cjsj__month=now_month, kdh_s__in=['已签收', '妥投']).count()
#                         jq_num = models.Reissue.objects.filter(user_re_id__in=user_branch, cjsj__year=year,
#                                                                cjsj__month=now_month, kdh_s__in=['拒签', '拒收']).count()
#                         if qs_num != 0 and reissue_num != 0:
#                             qs_rate = round(qs_num * 100 / reissue_num, 2)
#                         else:
#                             qs_rate = 0
#                         if reissue_num != 0 and jq_num != 0:
#                             jq_rate = round(jq_num * 100 / reissue_num, 2)
#                         else:
#                             jq_rate = 0
#
#                         data['date'] = f'{year}年{now_month}月'
#                         data['num'] = reissue_num
#                         data['qs_num'] = qs_num
#                         data['jq_num'] = jq_num
#                         data['qs_rate'] = f'{qs_rate}%'
#                         data['jq_rate'] = f'{jq_rate}%'
#                         branch_data_dict[branch.name] = data
#             elif data_type == 'machine':
#                 re_type = 'month_machine'
#                 for branch in branch_list:
#                     data = {}
#                     if branch.id != branch.parent_id:
#                         user_branch = models.User.objects.filter(branch_name_id=branch.id)
#                         machine_num = models.Activate.objects.filter(machine_id__machine_num__user__in=user_branch,
#                                                                      cash_state='已返现', activate_date__year=year,
#                                                                      activate_date__month=now_month).count()
#                         issue_num = models.Issue.objects.filter(user_id__in=user_branch, created_time__year=year,
#                                                                 created_time__month=now_month).count()
#                         if machine_num != 0 and issue_num != 0:
#                             jh_rate = round(machine_num * 100 / issue_num, 2)
#                         else:
#                             jh_rate = 0
#                         data['date'] = f'{year}年{now_month}月'
#                         data['issue_num'] = issue_num
#                         data['num'] = machine_num
#                         data['jh_rate'] = f'{jh_rate}%'
#                         branch_data_dict[branch.name] = data
#             elif data_type == 'order':
#                 re_type = 'month_order'
#                 for branch in branch_list:
#                     data = {}
#                     if branch.id != branch.parent_id:
#                         user_branch = models.User.objects.filter(branch_name_id=branch.id)
#                         order_obj = models.Order.objects.filter(
#                             terminal_num__machine_num__user__in=user_branch).order_by('-transaction_time')
#                         order_num = \
#                         order_obj.filter(transaction_time__year=year, transaction_time__month=now_month).aggregate(
#                             money_sum=Sum('money'))['money_sum']
#                         ordernum_num = order_obj.filter(transaction_time__year=year,
#                                                         transaction_time__month=now_month).count()
#                         data['date'] = f'{year}年{now_month}月'
#                         data['num'] = order_num
#                         data['ordernum_num'] = ordernum_num
#                         branch_data_dict[branch.name] = data
#         elif date_frame == 'before_month':
#             if data_type == 'issue':
#                 re_type = 'before_month_issue'
#                 for branch in branch_list:
#                     data = {}
#                     if branch.id != branch.parent_id:
#                         user_branch = models.User.objects.filter(branch_name_id=branch.id)
#                         issue_num = models.Issue.objects.filter(user_id__in=user_branch, created_time__year=year,
#                                                                 created_time__month=before_month).count()
#                         data['date'] = f'{year}年{before_month}月'
#                         data['num'] = issue_num
#                         branch_data_dict[branch.name] = data
#             elif data_type == 'reissue':
#                 re_type = 'before_month_reissue'
#                 for branch in branch_list:
#                     data = {}
#                     if branch.id != branch.parent_id:
#                         user_branch = models.User.objects.filter(branch_name_id=branch.id)
#                         reissue_num = models.Reissue.objects.filter(user_re_id__in=user_branch, cjsj__year=year,
#                                                                     cjsj__month=before_month).count()
#                         qs_num = models.Reissue.objects.filter(user_re_id__in=user_branch, cjsj__year=year,
#                                                                cjsj__month=before_month,
#                                                                kdh_s__in=['已签收', '妥投']).count()
#                         jq_num = models.Reissue.objects.filter(user_re_id__in=user_branch, cjsj__year=year,
#                                                                cjsj__month=before_month, kdh_s__in=['拒签', '拒收']).count()
#                         if qs_num != 0 and reissue_num != 0:
#                             qs_rate = round(qs_num * 100 / reissue_num, 2)
#                         else:
#                             qs_rate = 0
#                         if reissue_num != 0 and jq_num != 0:
#                             jq_rate = round(jq_num * 100 / reissue_num, 2)
#                         else:
#                             jq_rate = 0
#
#                         data['date'] = f'{year}年{before_month}月'
#                         data['num'] = reissue_num
#                         data['qs_num'] = qs_num
#                         data['jq_num'] = jq_num
#                         data['qs_rate'] = f'{qs_rate}%'
#                         data['jq_rate'] = f'{jq_rate}%'
#                         branch_data_dict[branch.name] = data
#             elif data_type == 'machine':
#                 re_type = 'before_month_machine'
#                 for branch in branch_list:
#                     data = {}
#                     if branch.id != branch.parent_id:
#                         user_branch = models.User.objects.filter(branch_name_id=branch.id)
#                         machine_num = models.Activate.objects.filter(machine_id__machine_num__user__in=user_branch,
#                                                                      cash_state='已返现', activate_date__year=year,
#                                                                      activate_date__month=before_month).count()
#                         issue_num = models.Issue.objects.filter(user_id__in=user_branch, created_time__year=year,
#                                                                 created_time__month=before_month).count()
#                         if machine_num != 0 and issue_num != 0:
#                             jh_rate = round(machine_num * 100 / issue_num, 2)
#                         else:
#                             jh_rate = 0
#                         data['date'] = f'{year}年{before_month}月'
#                         data['issue_num'] = issue_num
#                         data['num'] = machine_num
#                         data['jh_rate'] = f'{jh_rate}%'
#                         branch_data_dict[branch.name] = data
#             elif data_type == 'order':
#                 re_type = 'before_month_order'
#                 for branch in branch_list:
#                     data = {}
#                     if branch.id != branch.parent_id:
#                         user_branch = models.User.objects.filter(branch_name_id=branch.id)
#                         order_obj = models.Order.objects.filter(
#                             terminal_num__machine_num__user__in=user_branch).order_by('-transaction_time')
#                         order_num = \
#                         order_obj.filter(transaction_time__year=year, transaction_time__month=before_month).aggregate(
#                             money_sum=Sum('money'))['money_sum']
#                         ordernum_num = order_obj.filter(transaction_time__year=year,
#                                                         transaction_time__month=before_month).count()
#                         data['date'] = f'{year}年{before_month}月'
#                         data['num'] = order_num
#                         data['ordernum_num'] = ordernum_num
#                         branch_data_dict[branch.name] = data
#         elif date_frame == 'total':
#             if data_type == 'issue':
#                 re_type = 'total_issue'
#                 for branch in branch_list:
#                     data = {}
#                     if branch.id != branch.parent_id:
#                         user_branch = models.User.objects.filter(branch_name_id=branch.id)
#                         issue_obj = models.Issue.objects.filter(user__in=user_branch)
#                         issue_date = issue_obj.order_by('created_time').first().created_time
#                         issue_num = issue_obj.count()
#                         data['date'] = f'{issue_date}至今的数据'
#                         data['num'] = issue_num
#                         branch_data_dict[branch.name] = data
#             elif data_type == 'reissue':
#                 re_type = 'total_reissue'
#                 for branch in branch_list:
#                     data = {}
#                     if branch.id != branch.parent_id:
#                         user_branch = models.User.objects.filter(branch_name_id=branch.id)
#                         reissue_num = models.Reissue.objects.filter(user_re_id__in=user_branch).count()
#                         qs_num = models.Reissue.objects.filter(user_re_id__in=user_branch,
#                                                                kdh_s__in=['已签收', '妥投']).count()
#                         jq_num = models.Reissue.objects.filter(user_re_id__in=user_branch,
#                                                                kdh_s__in=['拒签', '拒收']).count()
#                         if qs_num != 0 and reissue_num != 0:
#                             qs_rate = round(qs_num * 100 / reissue_num, 2)
#                         else:
#                             qs_rate = 0
#                         if reissue_num != 0 and jq_num != 0:
#                             jq_rate = round(jq_num * 100 / reissue_num, 2)
#                         else:
#                             jq_rate = 0
#
#                         data['date'] = '2020年1月至今'
#                         data['num'] = reissue_num
#                         data['qs_num'] = qs_num
#                         data['jq_num'] = jq_num
#                         data['qs_rate'] = f'{qs_rate}%'
#                         data['jq_rate'] = f'{jq_rate}%'
#                         branch_data_dict[branch.name] = data
#             elif data_type == 'machine':
#                 re_type = 'total_machine'
#                 for branch in branch_list:
#                     data = {}
#                     if branch.id != branch.parent_id:
#                         user_branch = models.User.objects.filter(branch_name_id=branch.id)
#                         machine_obj = models.Activate.objects.filter(machine_id__machine_num__user__in=user_branch,
#                                                                      cash_state='已返现')
#                         machine_date = machine_obj.order_by('activate_date').first()
#                         if machine_date:
#                             machine_date = machine_date.activate_date
#                         else:
#                             machine_date = '2020年01月01日'
#                         machine_num = machine_obj.count()
#                         issue_num = models.Issue.objects.filter(user_id__in=user_branch).count()
#                         if machine_num != 0 and issue_num != 0:
#                             jh_rate = round(machine_num * 100 / issue_num, 2)
#                         else:
#                             jh_rate = 0
#                         data['date'] = f'{machine_date}至今'
#                         data['issue_num'] = issue_num
#                         data['num'] = machine_num
#                         data['jh_rate'] = f'{jh_rate}%'
#                         branch_data_dict[branch.name] = data
#             elif data_type == 'order':
#                 re_type = 'total_order'
#                 for branch in branch_list:
#                     data = {}
#                     if branch.id != branch.parent_id:
#                         user_branch = models.User.objects.filter(branch_name_id=branch.id)
#                         order_obj = models.Order.objects.filter(
#                             terminal_num__machine_num__user__in=user_branch).order_by('transaction_time')
#                         if order_obj:
#                             order_date = order_obj.first().transaction_time
#                         else:
#                             order_date = '2020年1月1日'
#                         order_num = order_obj.aggregate(money_sum=Sum('money'))['money_sum']
#                         ordernum_num = order_obj.count()
#                         data['date'] = f'{order_date}至今'
#                         data['num'] = order_num
#                         data['ordernum_num'] = ordernum_num
#                         branch_data_dict[branch.name] = data
#     else:
#         return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')
#     return render(request, 'home/branch_date_list.html', locals())
#
#
# @login_required
# def add_branch(request):
#     """添加机构"""
#     user = models.User.objects.filter(username=request.user.username).first()
#     if user.user_type == 1:
#         user_list = models.User.objects.filter(is_show=1, is_delete=0)
#         if request.is_ajax():
#             back_dic = {'code': 1000, 'msg': ''}
#             if request.method == 'POST':
#                 name = request.POST.get('name')
#                 admin = request.POST.get('admin')
#                 name = name.strip()
#                 if len(name):
#                     if models.Branch.objects.filter(name=name):
#                         back_dic['code'] = 2000
#                         back_dic['msg'] = '机构名已存在'
#                     else:
#                         if admin:
#                             branch_obj = models.Branch.objects.create(name=name, admin_id=admin)
#                             models.User.objects.filter(username=admin).update(user_type=2, branch_name_id=branch_obj.id)
#                             back_dic['msg'] = '机构创建成功'
#                         else:
#                             back_dic['code'] = 2000
#                             back_dic['msg'] = '请选择管理员'
#                 else:
#                     back_dic['code'] = 2000
#                     back_dic['msg'] = '机构名不能为空'
#             return JsonResponse(back_dic)
#     else:
#         return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')
#     return render(request, 'home/branch_add.html', locals())
#
#
# @login_required
# def issue(request):
#     """送机列表"""
#     user = models.User.objects.filter(username=request.user.username).first()
#     start = request.GET.get('start')
#     end = request.GET.get('end')
#     data_type = request.GET.get('data_type')
#     keywords = request.GET.get('keywords')
#
#
#     if user.user_type == 1:
#         issue_list = models.Issue.objects.all().order_by('-created_time', 'machine_num')
#     elif user.user_type == 2:
#         admin_obj = models.Branch.objects.filter(admin_id=user.username).first()
#         have_ch = models.Branch.objects.filter(parent_id=admin_obj.id)
#         if have_ch:
#             issue_list = models.Issue.objects.filter(user__branch_name__parent_id=user.branch_name_id).order_by(
#                 '-created_time', 'machine_num')
#
#         else:
#             issue_list = models.Issue.objects.filter(user__branch_name_id=user.branch_name_id).order_by('-created_time',
#                                                                                                         'machine_num')
#
#     elif user.user_type == 3:
#         issue_list = models.Issue.objects.filter(user_id=user.username).order_by('-created_time', 'machine_num')
#
#     else:
#         return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')
#     if start and end:
#
#         if keywords:
#             if data_type == 'username':
#                 issue_list = issue_list.filter(created_time__range=[start,end],user__username__contains=keywords)
#             elif data_type == 'consignee':
#                 issue_list = issue_list.filter(created_time__range=[start,end], consignee__contains=keywords)
#             elif data_type == 'machine_num':
#                 issue_list = issue_list.filter(created_time__range=[start,end], machine_num__contains=keywords)
#             elif data_type == 'phone_num':
#                 issue_list = issue_list.filter(created_time__range=[start,end], phone_num__contains=keywords)
#             elif data_type == 'courier_num':
#                 issue_list = issue_list.filter(created_time__range=[start,end], courier_num__contains=keywords)
#             elif data_type == 'courier_status':
#                 issue_list = issue_list.filter(created_time__range=[start,end], courier_status__contains=keywords)
#             elif data_type == 'remarks':
#                 issue_list = issue_list.filter(created_time__range=[start,end], remarks__contains=keywords)
#             elif data_type == 'branch':
#                 issue_list = issue_list.filter(created_time__range=[start,end], user__branch_name__name__contains=keywords)
#         else:
#             issue_list = issue_list.filter(created_time__range=[start,end])
#     else:
#         if keywords:
#             if data_type == 'username':
#                 issue_list = issue_list.filter(user__username__contains=keywords)
#             elif data_type == 'consignee':
#                 issue_list = issue_list.filter(consignee__contains=keywords)
#             elif data_type == 'machine_num':
#                 issue_list = issue_list.filter(machine_num__contains=keywords)
#             elif data_type == 'phone_num':
#                 issue_list = issue_list.filter(phone_num__contains=keywords)
#             elif data_type == 'courier_num':
#                 issue_list = issue_list.filter(courier_num__contains=keywords)
#             elif data_type == 'courier_status':
#                 issue_list = issue_list.filter(courier_status__contains=keywords)
#             elif data_type == 'remarks':
#                 issue_list = issue_list.filter(remarks__contains=keywords)
#             elif data_type == 'branch':
#                 issue_list = issue_list.filter(user__branch_name__name__contains=keywords)
#         else:
#             issue_list = issue_list
#
#     issue_obj = IssuePagination(current_page=request.GET.get('page', 1), start_date=request.GET.get('start'),end_date=request.GET.get('end'),data_type=request.GET.get('data_type'),keywords=request.GET.get('keywords'), all_count=issue_list.count())
#     page_queryset = issue_list[issue_obj.start:issue_obj.end]
#     if request.method == 'POST':
#         back_dic = {'code': 1000, 'url': "", 'msg': ''}
#         start = request.POST.get('start')
#         end = request.POST.get('end')
#         data_type = request.POST.get('data_type')
#         keywords = request.POST.get('keywords')
#         if user.user_type == 1:
#             issue_list = models.Issue.objects.all().order_by('-created_time', 'machine_num')
#         elif user.user_type == 2:
#             admin_obj = models.Branch.objects.filter(admin_id=user.username).first()
#             have_ch = models.Branch.objects.filter(parent_id=admin_obj.id)
#             if have_ch:
#                 issue_list = models.Issue.objects.filter(user__branch_name__parent_id=user.branch_name_id).order_by(
#                     '-created_time', 'machine_num')
#
#             else:
#                 issue_list = models.Issue.objects.filter(user__branch_name_id=user.branch_name_id).order_by(
#                     '-created_time',
#                     'machine_num')
#         else:
#             return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')
#         if start and end:
#
#             if keywords:
#                 if data_type == 'username':
#                     issue_list = issue_list.filter(created_time__range=[start, end], user__username__contains=keywords)
#                 elif data_type == 'consignee':
#                     issue_list = issue_list.filter(created_time__range=[start, end], consignee__contains=keywords)
#                 elif data_type == 'machine_num':
#                     issue_list = issue_list.filter(created_time__range=[start, end], machine_num__contains=keywords)
#                 elif data_type == 'phone_num':
#                     issue_list = issue_list.filter(created_time__range=[start, end], phone_num__contains=keywords)
#                 elif data_type == 'courier_num':
#                     issue_list = issue_list.filter(created_time__range=[start, end], courier_num__contains=keywords)
#                 elif data_type == 'courier_status':
#                     issue_list = issue_list.filter(created_time__range=[start, end], courier_status__contains=keywords)
#                 elif data_type == 'remarks':
#                     issue_list = issue_list.filter(created_time__range=[start, end], remarks__contains=keywords)
#                 elif data_type == 'branch':
#                     issue_list = issue_list.filter(created_time__range=[start, end],
#                                                    user__branch_name__name__contains=keywords)
#             else:
#                 issue_list = issue_list.filter(created_time__range=[start, end])
#         else:
#             if keywords:
#                 if data_type == 'username':
#                     issue_list = issue_list.filter(user__username__contains=keywords)
#                 elif data_type == 'consignee':
#                     issue_list = issue_list.filter(consignee__contains=keywords)
#                 elif data_type == 'machine_num':
#                     issue_list = issue_list.filter(machine_num__contains=keywords)
#                 elif data_type == 'phone_num':
#                     issue_list = issue_list.filter(phone_num__contains=keywords)
#                 elif data_type == 'courier_num':
#                     issue_list = issue_list.filter(courier_num__contains=keywords)
#                 elif data_type == 'courier_status':
#                     issue_list = issue_list.filter(courier_status__contains=keywords)
#                 elif data_type == 'remarks':
#                     issue_list = issue_list.filter(remarks__contains=keywords)
#                 elif data_type == 'branch':
#                     issue_list = issue_list.filter(user__branch_name__name__contains=keywords)
#             else:
#                 issue_list = issue_list
#         if issue_list:
#             """将数据写入excel"""
#             file_dir = os.path.join(settings.BASE_DIR, 'media', 'sreach_data')
#             work_book = xlwt.Workbook(encoding='utf-8')
#             date = getDay()
#             date = datetime.strftime(date, "%Y-%m-%d")
#             sheet = work_book.add_sheet(f'筛选的送机结果')
#             sheet.write(0, 0, '日期')
#             sheet.write(0, 1, '组别')
#             sheet.write(0, 2, '业务员')
#             sheet.write(0, 3, '客户')
#             sheet.write(0, 4, '电话号码')
#
#             sheet.write(0, 5, '序列号')
#             sheet.write(0, 6, '地址')
#             sheet.write(0, 7, '快递单号')
#             sheet.write(0, 8, '机型')
#             sheet.write(0, 9, '快递状态')
#             sheet.write(0, 10, '备注')
#
#             a = 1
#             for issue in issue_list:
#                 issue_date = issue.created_time
#                 issue_date = datetime.strftime(issue_date, "%Y-%m-%d")
#                 sheet.write(a, 0, issue_date)
#                 sheet.write(a, 1, issue.user.branch_name.name)
#                 sheet.write(a, 2, issue.user.username)
#                 sheet.write(a, 3, issue.consignee)
#                 sheet.write(a, 4, issue.phone_num)
#                 sheet.write(a, 5, issue.machine_num)
#                 sheet.write(a, 6, issue.address)
#                 sheet.write(a, 7, issue.courier_num)
#                 sheet.write(a, 8, issue.machine_type)
#                 sheet.write(a, 9, issue.courier_status)
#                 sheet.write(a, 10, issue.remarks)
#                 a = a + 1
#             sheet.col(0).width = 256 * 13
#             sheet.col(1).width = 256 * 15
#             sheet.col(2).width = 256 * 12
#             sheet.col(3).width = 256 * 12
#             sheet.col(4).width = 256 * 15
#             sheet.col(5).width = 256 * 28
#             sheet.col(6).width = 256 * 70
#             sheet.col(7).width = 256 * 15
#             sheet.col(8).width = 256 * 15
#             sheet.col(9).width = 256 * 15
#             sheet.col(10).width = 256 * 15
#             new_name = f'serach_issue.xls'
#             file_path = os.path.join(file_dir, new_name)  # 拼接文件路径
#             work_book.save(file_path)
#             back_dic['msg'] = new_name
#         else:
#             back_dic['code'] = 1002
#             back_dic['msg'] = '当前无符合条件的记录'
#         return JsonResponse(back_dic)
#     return render(request, 'home/issue_list.html', locals())
#
#
# @login_required
# def issue_today(request):
#     """今日送机"""
#     user = models.User.objects.filter(username=request.user.username).first()
#     if request.method == "POST":
#         back_dic = {'code': 1000, 'url': "", 'msg': ''}
#         start = request.POST.get('start')
#         end = request.POST.get('end')
#         branch = request.POST.get('branch')
#         if user.user_type == 1 or user.user_type == 4:
#             if branch == 'all':
#                 issue_list = models.Issue.objects.filter(created_time__range=[start, end]).order_by('created_time',
#                                                                                                     'user__branch_name')
#             else:
#                 issue_list = models.Issue.objects.filter(created_time__range=[start, end],
#                                                          user__branch_name_id=branch).order_by('created_time',
#                                                                                                'user__branch_name')
#         elif user.user_type == 2:
#             admin_obj = models.Branch.objects.filter(admin_id=user.username).first()
#             have_ch = models.Branch.objects.filter(parent_id=admin_obj.id)
#             if have_ch:
#                 if branch == 'all':
#                     issue_list = models.Issue.objects.filter(created_time__range=[start, end],
#                                                              user__branch_name__parent_id=user.branch_name_id).order_by(
#                         'created_time',
#                         'user__branch_name')
#                 else:
#                     issue_list = models.Issue.objects.filter(created_time__range=[start, end],
#                                                              user__branch_name_id=branch).order_by('created_time',
#                                                                                                    'user__branch_name')
#             else:
#                 if branch == 'all':
#                     issue_list = models.Issue.objects.filter(created_time__range=[start, end],
#                                                              user__branch_name_id=user.branch_name_id).order_by(
#                         'created_time')
#                 else:
#                     issue_list = models.Issue.objects.filter(created_time__range=[start, end],
#                                                              user__branch_name_id=branch).order_by('created_time')
#         else:
#             return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')
#         if issue_list:
#             """将数据写入excel"""
#             file_dir = os.path.join(settings.BASE_DIR, 'media', 'sreach_data')
#             work_book = xlwt.Workbook(encoding='utf-8')
#             date = getDay()
#             date = datetime.strftime(date, "%Y-%m-%d")
#             sheet = work_book.add_sheet(f'筛选的送机结果')
#             sheet.write(0, 0, '日期')
#             sheet.write(0, 1, '组别')
#             sheet.write(0, 2, '业务员')
#             sheet.write(0, 3, '客户')
#             sheet.write(0, 4, '电话号码')
#
#             sheet.write(0, 5, '序列号')
#             sheet.write(0, 6, '地址')
#             sheet.write(0, 7, '快递单号')
#             sheet.write(0, 8, '机型')
#             sheet.write(0, 9, '快递状态')
#             sheet.write(0, 10, '备注')
#
#             a = 1
#             for issue in issue_list:
#                 issue_date = issue.created_time
#                 issue_date = datetime.strftime(issue_date, "%Y-%m-%d")
#                 sheet.write(a, 0, issue_date)
#                 sheet.write(a, 1, issue.user.branch_name.name)
#                 sheet.write(a, 2, issue.user.username)
#                 sheet.write(a, 3, issue.consignee)
#                 sheet.write(a, 4, issue.phone_num)
#                 sheet.write(a, 5, issue.machine_num)
#                 sheet.write(a, 6, issue.address)
#                 sheet.write(a, 7, issue.courier_num)
#                 sheet.write(a, 8, issue.machine_type)
#                 sheet.write(a, 9, issue.courier_status)
#                 sheet.write(a, 10, issue.remarks)
#                 a = a + 1
#             sheet.col(0).width = 256 * 13
#             sheet.col(1).width = 256 * 15
#             sheet.col(2).width = 256 * 12
#             sheet.col(3).width = 256 * 12
#             sheet.col(4).width = 256 * 15
#             sheet.col(5).width = 256 * 28
#             sheet.col(6).width = 256 * 70
#             sheet.col(7).width = 256 * 15
#             sheet.col(8).width = 256 * 15
#             sheet.col(9).width = 256 * 15
#             sheet.col(10).width = 256 * 15
#             new_name = f'serach_data.xls'
#             file_path = os.path.join(file_dir, new_name)  # 拼接文件路径
#             work_book.save(file_path)
#             back_dic['msg'] = new_name
#         else:
#             back_dic['code'] = 1002
#             back_dic['msg'] = '当前无符合条件的记录'
#         return JsonResponse(back_dic)
#     else:
#         if user.user_type == 1 or user.user_type == 4:
#             branch_list = models.Branch.objects.filter(is_show=True)
#             issue_list = models.Issue.objects.filter(created_time=getDay()).order_by('-id')
#             issue_obj = Pagination(current_page=request.GET.get('page', 1), all_count=issue_list.count())
#             page_queryset = issue_list[issue_obj.start:issue_obj.end]
#         elif user.user_type == 2:
#             admin_obj = models.Branch.objects.filter(admin_id=user.username).first()
#             have_ch = models.Branch.objects.filter(parent_id=admin_obj.id)
#             if have_ch:
#                 branch_list = have_ch
#                 issue_list = models.Issue.objects.filter(user__branch_name__parent_id=user.branch_name_id,
#                                                          created_time=getDay()).order_by('id')
#                 issue_obj = Pagination(current_page=request.GET.get('page', 1), all_count=issue_list.count())
#                 page_queryset = issue_list[issue_obj.start:issue_obj.end]
#             else:
#                 branch_list = models.Branch.objects.filter(admin_id=user.username)
#                 issue_list = models.Issue.objects.filter(user__branch_name_id=user.branch_name_id,
#                                                          created_time=getDay())
#                 issue_obj = Pagination(current_page=request.GET.get('page', 1), all_count=issue_list.count())
#                 page_queryset = issue_list[issue_obj.start:issue_obj.end]
#         elif user.user_type == 3:
#             issue_list = models.Issue.objects.filter(user_id=user.username, created_time=getDay())
#             issue_obj = Pagination(current_page=request.GET.get('page', 1), all_count=issue_list.count())
#             page_queryset = issue_list[issue_obj.start:issue_obj.end]
#         else:
#             return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')
#     return render(request, 'home/issue_today.html', locals())
#
#
# @login_required
# def issue_add(request):
#     """手动添加送机数据"""
#     user = models.User.objects.filter(username=request.user.username).first()
#     if user.user_type == 1 or user.user_type == 2 or user.user_type == 4:
#         user_list = models.User.objects.all()
#         brand_list = models.BrandTable.objects.filter(show_type=2)
#         if request.is_ajax():
#             back_dic = {'code': 1000, 'msg': ''}
#             if request.method == 'POST':
#                 username = request.POST.get('username')
#                 phone = request.POST.get('phone')
#                 address = request.POST.get('address')
#                 machine_type = request.POST.get('machine_type')
#                 machine_num = request.POST.get('machine_num')
#                 courier_num = request.POST.get('courier_num')
#                 bz = request.POST.get('bz')
#                 users = request.POST.get('user')
#
#                 if machine_num and courier_num:
#                     machine_obj = models.Issue.objects.filter(machine_num=machine_num)
#                     if machine_obj:
#                         machine_obj.update(machine_num=time.time())
#                     new_iss = models.Issue.objects.create(user_id=users, consignee=username, courier_num=courier_num,
#                                                           courier_status='单号已出', phone_num=phone, address=address,
#                                                           machine_num=machine_num, machine_type=machine_type,
#                                                           remarks=bz, created_time=getDay())
#                 elif machine_num:
#                     machine_obj = models.Issue.objects.filter(machine_num=machine_num)
#                     if machine_obj:
#                         machine_obj.update(machine_num=time.time())
#                     new_iss = models.Issue.objects.create(user_id=users, consignee=username,
#                                                           courier_status='未打单', phone_num=phone, address=address,
#                                                           machine_num=machine_num, machine_type=machine_type,
#                                                           remarks=bz, created_time=getDay())
#                 elif courier_num:
#                     new_iss = models.Issue.objects.create(user_id=users, consignee=username, courier_num=courier_num,
#                                                           courier_status='单号已出', phone_num=phone, address=address,
#                                                           machine_type=machine_type, remarks=bz, created_time=getDay())
#                 else:
#                     new_iss = models.Issue.objects.create(user_id=users, consignee=username, courier_status='未打单',
#                                                           phone_num=phone, address=address,
#                                                           machine_type=machine_type, remarks=bz, created_time=getDay())
#                 if new_iss:
#                     back_dic['msg'] = '添加成功'
#                 else:
#                     back_dic['code'] = 1002
#                     back_dic['msg'] = '添加失败请重新尝试'
#             return JsonResponse(back_dic)
#     else:
#         return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')
#     return render(request, 'home/issue_add.html', locals())
#
#
# @login_required
# def issue_edit(request, pk):
#     user = models.User.objects.filter(username=request.user.username).first()
#     if user.user_type == 1 or user.user_type == 2 or user.user_type == 4:
#         user_list = models.User.objects.all()
#         brand_list = models.BrandTable.objects.filter(show_type=2)
#         issue_obj = models.Issue.objects.filter(pk=pk).first()
#         if request.is_ajax():
#             back_dic = {'code': 1000, 'msg': ''}
#             if request.method == 'POST':
#                 username = request.POST.get('username')
#                 phone = request.POST.get('phone')
#                 address = request.POST.get('address')
#                 machine_type = request.POST.get('machine_type')
#                 machine_num = request.POST.get('machine_num')
#                 courier_num = request.POST.get('courier_num')
#                 bz = request.POST.get('bz')
#                 users = request.POST.get('user')
#
#                 if machine_num and courier_num:
#                     machine_obj = models.Issue.objects.filter(machine_num=machine_num)
#                     if machine_obj:
#                         machine_obj.update(machine_num=time.time())
#                     new_iss = models.Issue.objects.filter(pk=pk).update(user_id=users, consignee=username,
#                                                                         courier_num=courier_num,
#                                                                         courier_status='单号已出', phone_num=phone,
#                                                                         address=address,
#                                                                         machine_num=machine_num,
#                                                                         machine_type=machine_type,
#                                                                         remarks=bz)
#                 elif machine_num:
#                     machine_obj = models.Issue.objects.filter(machine_num=machine_num)
#                     if machine_obj:
#                         machine_obj.update(machine_num=time.time())
#                     new_iss = models.Issue.objects.filter(pk=pk).update(user_id=users, consignee=username,
#                                                                          phone_num=phone,
#                                                                         address=address,
#                                                                         machine_num=machine_num,
#                                                                         machine_type=machine_type,
#                                                                         remarks=bz)
#                 elif courier_num:
#                     machine_obj = models.Issue.objects.filter(machine_num=machine_num)
#                     if machine_obj:
#                         machine_obj.update(machine_num=time.time())
#                     new_iss = models.Issue.objects.filter(pk=pk).update(user_id=users, consignee=username,
#                                                                         courier_num=courier_num,
#                                                                         courier_status='单号已出', phone_num=phone,
#                                                                         address=address,
#                                                                         machine_type=machine_type,
#                                                                         remarks=bz)
#                     back_dic['msg'] = '修改成功'
#                 else:
#                     back_dic['code'] = 1002
#                     back_dic['msg'] = '序列号或单号必填一项'
#             return JsonResponse(back_dic)
#     else:
#         return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')
#     return render(request, 'home/issue_edit.html', locals())
#
#
# @login_required
# def issue_del(request, pk):
#     user = models.User.objects.filter(username=request.user.username).first()
#     if user.user_type == 1 or user.user_type == 2 or user.user_type == 4:
#         if request.is_ajax():
#             back_dic = {'code': 1000, 'msg': ''}
#             if request.method == 'POST':
#                 models.Issue.objects.filter(pk=pk).delete()
#                 back_dic['msg'] = '删除成功'
#             return JsonResponse(back_dic)
#     else:
#         return HttpResponse('<script>alert("对不起，您无权访问");xadmin.close();window.location.href="/home"</script>')




@login_required
def upload_file(request):
    """上传文件前端"""
    return render(request, 'home/upload_file.html', locals())

