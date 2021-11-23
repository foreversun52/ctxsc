from django.urls import path, re_path
from home import views as home
urlpatterns = [
    path('', home.home, name='home'),
    # 欢迎页
    path('welcome/', home.welcome, name='welcome'),
    path('site/', home.site, name='site'),

    # # 人员相关的操作
    path('member_list/', home.member_list, name='member_list'),
    path('product_list/', home.product_list, name='product_list'),
    path('material_info/', home.material_info, name='material_info'),
    path('packing_info/', home.packing_info, name='packing_info'),


    path('user_info/', home.user_info, name='user_info'),
    path('add_user/', home.add_user, name='add_user'),
    re_path('edit_user/(\d+)/', home.edit_user, name='edit_user'),
    re_path('del_user/(\d+)/', home.del_user, name='del_user'),


    path('one_floor_info_list/', home.one_floor_info_list, name='one_floor_info_list'),
    path('two_floor_info_list/', home.two_floor_info_list, name='two_floor_info_list'),
    path('three_floor_info_list/', home.three_floor_info_list, name='three_floor_info_list'),
    path('finished_info_list/', home.finished_info_list, name='finished_info_list'),
    # path('member_data_list/', home.member_data_list, name='member_data_list'),
    path('add_member/', home.add_member, name='add_member'),
    path('add_material/', home.add_material, name='add_material'),
    re_path('edit_material/(\d+)/', home.edit_material, name='edit_material'),
    path('add_packing/', home.add_packing, name='add_packing'),
    path('add_product/', home.add_product, name='add_product'),
    re_path('edit_product/(\d+)/', home.edit_product, name='edit_product'),
    re_path('edit_product_info/(\d+)/', home.edit_product_info, name='edit_product_info'),
    re_path('edit_one_floor_info/(\d+)/', home.edit_one_floor_info, name='edit_one_floor_info'),
    re_path('edit_two_floor_info/(\d+)/', home.edit_two_floor_info, name='edit_two_floor_info'),
    re_path('edit_three_floor_info/(\d+)/', home.edit_three_floor_info, name='edit_three_floor_info'),
    re_path('edit_finished_info/(\d+)/', home.edit_finished_info, name='edit_finished_info'),
    re_path('del_product/(\d+)/', home.del_product, name='del_product'),
    re_path('del_material/(\d+)/', home.del_material, name='del_material'),
    re_path('del_packing/(\d+)/', home.del_packing, name='del_packing'),
    # re_path('set_password/(\w+)/', home.set_password, name='set_pwd'),
    re_path('edit_member/(\d+)/', home.edit_member, name='edit_member'),
    re_path('del_member/(\d+)/', home.del_member, name='del_member'),
]
