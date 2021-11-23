from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    """用户表"""
    delete_choices = (
            (0, '否'),
            (1, '是')
        )
    type_choices = (
        (1, '管理员'),
        (2, '普通员工'),
    )

    user_type = models.SmallIntegerField(choices=type_choices, default=3, verbose_name='用户类型')
    is_show = models.SmallIntegerField(default=1,choices=delete_choices, verbose_name='是否可以修改数据')

    class Meta:
        verbose_name_plural = '用户表'

    def __str__(self):
        return self.username


class Customer(models.Model):
    name = models.CharField(max_length=50, unique=True)
    mobile = models.CharField(max_length=20, null=True, verbose_name='客户联系方式')
    customer_info = models.TextField(null=True, verbose_name='客户信息')
    create_date = models.DateField(null=True, verbose_name='客户创建日期')

    class Meta:
        verbose_name_plural = '客户信息表'

    def __str__(self):
        return self.name


class Material(models.Model):
    material_name = models.CharField(max_length=50, null=True, verbose_name='材料名称')
    material_price = models.CharField(max_length=50, null=True, verbose_name='材料价格')
    show_type = models.SmallIntegerField(default=1, null=True, verbose_name='显示区分')
    is_enable = models.SmallIntegerField(default=1, null=True, verbose_name='是否显示')

    class Meta:
        verbose_name_plural = '材料信息表'

    def __str__(self):
        return self.material_name


class Packing(models.Model):
    packing_name = models.CharField(max_length=50, null=True, verbose_name='材料名称')
    show_type = models.SmallIntegerField(default=1, null=True, verbose_name='显示区分')
    is_enable = models.SmallIntegerField(default=1, null=True, verbose_name='是否显示')

    class Meta:
        verbose_name_plural = '包装信息表'

    def __str__(self):
        return self.packing_name


class OneFloor(models.Model):
    # 一楼
    one_floor_user = models.ForeignKey(to='User', on_delete=models.DO_NOTHING, verbose_name='一楼数据填写人')
    material_height = models.CharField(max_length=10, null=True, verbose_name='材料宽')
    material_thickness = models.CharField(max_length=10, null=True,  verbose_name='材料厚度')
    material_type = models.ForeignKey(to='Material', null=True, on_delete=models.DO_NOTHING, verbose_name='材料类别')
    power_time = models.CharField(max_length=10, null=True, verbose_name='开机做片时间')
    pulling_long = models.CharField(max_length=10, null=True, verbose_name='拉片长度')
    shipment_num = models.CharField(max_length=50, null=True, verbose_name='每片出货个数')
    company_choices = (
        (1, '个'),
        (2, '套'),
    )
    slice_company = models.SmallIntegerField(default=1, choices=company_choices, verbose_name='出货单位')
    ton_num = models.CharField(max_length=50, null=True, verbose_name='每吨出货片数')  # 公式：1000000/（材料宽/10*拉片长度*1.4*厚度/1000）
    ton_nums = models.CharField(max_length=50, null=True, verbose_name='每吨成品数量')  # 公式：每片出货个数*每吨出货片数
    ton_slice_time = models.CharField(max_length=10, null=True, verbose_name='每吨拉片时长')  # 公式：每吨出货片数*开机做片时间/3600

    class Meta:
        verbose_name_plural = '一楼产品信息表'

    def __str__(self):
        return self.one_floor_user.username


class TowFloor(models.Model):
    company_choices = (
        (1, '个'),
        (2, '套'),
    )
    choices = (
        (1, '个数'),
        (2, '重量'),
    )
    two_floor_user = models.ForeignKey(to='User', on_delete=models.DO_NOTHING, verbose_name='二楼数据填写人')
    knife_num = models.CharField(max_length=50, null=True, verbose_name='冲刀拼数')
    bed_num = models.CharField(max_length=50, null=True, verbose_name='冲床张数')
    bed_yield = models.CharField(max_length=50, null=True, verbose_name='冲床产量')
    bed_yield_comany = models.SmallIntegerField(default=1, choices=company_choices, verbose_name='冲床产量单位')
    bed_price = models.CharField(max_length=50, null=True, verbose_name='冲床工价')
    two_packing_type = models.ForeignKey(to='Packing', null=True, on_delete=models.DO_NOTHING, verbose_name='包装类型')
    two_packing_num_one = models.CharField(max_length=50, null=True, verbose_name='包装数量-个')
    two_packing_num_two = models.CharField(max_length=50, null=True, verbose_name='包装数量-叠')
    two_packing_num_three = models.CharField(max_length=50, null=True, verbose_name='包装数量-条')
    two_packing_num_four = models.CharField(max_length=50, null=True, verbose_name='包装数量-层')
    two_packing_nums = models.CharField(max_length=50, null=True, verbose_name='包装总数')   # 个*叠*条*层
    packing_num_choices = models.SmallIntegerField(default=1, choices=choices, verbose_name='包装数量类型（个数/重量）')
    packing_weight = models.CharField(max_length=10, null=True, verbose_name='重量/公斤')
    two_packing_price = models.CharField(max_length=50, null=True, verbose_name='二楼包装工价')

    class Meta:
        verbose_name_plural = '二楼产品信息表'

    def __str__(self):
        return self.two_floor_user.username


class ThreeFloor(models.Model):
    three_floor_user = models.ForeignKey(to='User', on_delete=models.DO_NOTHING, verbose_name='三楼数据填写人')
    edge_price = models.CharField(max_length=50, null=True, verbose_name='拆边工价')
    three_packing_type = models.ForeignKey(to='Packing', null=True, on_delete=models.DO_NOTHING, verbose_name='包装类型')
    three_packing_num_one = models.CharField(max_length=50, null=True, verbose_name='包装数量-个')
    three_packing_num_two = models.CharField(max_length=50, null=True, verbose_name='包装数量-叠')
    three_packing_num_three = models.CharField(max_length=50, null=True, verbose_name='包装数量-条')
    three_packing_num_four = models.CharField(max_length=50, null=True, verbose_name='包装数量-层')
    three_packing_nums = models.CharField(max_length=50, null=True, verbose_name='包装总数')   # 个*叠*条*层
    three_packing_price = models.CharField(max_length=50, null=True, verbose_name='三楼包装工价')

    class Meta:
        verbose_name_plural = '三楼产品信息表'

    def __str__(self):
        return self.three_floor_user.username


class FinishedProduct(models.Model):
    choices = (
        (1, '套'),
        (2, '公斤'),
        (3, '个'),
    )
    finished_user = models.ForeignKey(to='User', on_delete=models.DO_NOTHING, verbose_name='成品数据填写人')
    sheet_weight = models.CharField(max_length=50, null=True, verbose_name='整张材料重量')
    slice_weight = models.CharField(max_length=50, null=True, verbose_name='单片成品重量')
    individual_weight = models.CharField(max_length=50, null=True, verbose_name='单个成品重量')
    leftovers_weight = models.CharField(max_length=50, null=True, verbose_name='边角料重量')
    leftovers_percentage = models.CharField(max_length=50, null=True, verbose_name='边角料占比')  # 边角料重量/整张材料重量
    product_price = models.CharField(max_length=50, null=True, verbose_name='成品单价')
    product_price_choices = models.SmallIntegerField(default=1, null=True, choices=choices, verbose_name='成品单价的单位')
    material_price = models.CharField(max_length=50, null=True, verbose_name='材料价格')
    gross_profit = models.CharField(max_length=50, null=True, verbose_name='毛利润')

    class Meta:
        verbose_name_plural = '成品数据信息'

    def __str__(self):
        return self.finished_user.username


class ProductInfo(models.Model):
    prod_choices = (
        (1, '未开始'),
        (2, '制作中'),
        (3, '已完成'),
    )
    customer_name = models.ForeignKey(to='Customer', on_delete=models.DO_NOTHING, verbose_name='客户')
    product_name = models.CharField(max_length=50, unique=True, verbose_name='品名')
    one_floor = models.OneToOneField(to='OneFloor', null=True, on_delete=models.CASCADE, verbose_name='对应一楼的流程')
    two_floor = models.OneToOneField(to='TowFloor', null=True, on_delete=models.CASCADE, verbose_name='对应二楼的流程')
    three_floor = models.OneToOneField(to='ThreeFloor', null=True, on_delete=models.CASCADE, verbose_name='对应三楼的流程')
    finished_product = models.OneToOneField(to='FinishedProduct', null=True, on_delete=models.CASCADE, verbose_name='成品数据')
    product_status = models.SmallIntegerField(default=1, choices=prod_choices, verbose_name='产品状态')
    product_img = models.ImageField(upload_to='product', null=True, verbose_name='产品图片')
    p_create_date = models.DateField(null=True, verbose_name='产品创建时间')

    class Meta:
        verbose_name_plural = '产品信息表'

    def __str__(self):
        return self.product_name
