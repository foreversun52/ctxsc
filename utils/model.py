from django.db import models


class BaseModel(models.Model):
    delete_choices = (
        (0, '否'),
        (1, '是')
    )
    is_delete = models.SmallIntegerField(default=0, choices=delete_choices, verbose_name='是否删除')
    is_show = models.SmallIntegerField(default=1,choices=delete_choices, verbose_name='是否显示')
    created_time = models.DateField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        abstract = True
