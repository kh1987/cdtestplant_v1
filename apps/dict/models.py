from django.db import models
from utils.models import CoreModel
from apps.dict.fragment.enums import DocNameEnum
from apps.project.models import Project

# ~~~~~~~~~~~~~字典以及字典item~~~~~~~~~~~~~
class Dict(CoreModel):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="字典名称", help_text="字典名称")
    code = models.CharField(max_length=100, blank=True, null=True, verbose_name="编码", help_text="编码")
    status = models.CharField(max_length=8, blank=True, null=True, verbose_name="状态", help_text="状态", default='1')
    remark = models.CharField(max_length=2000, blank=True, null=True, verbose_name="备注", help_text="备注")

    def __str__(self):
        return f'字典名称:{self.name}-字典类码:{self.code}'

    class Meta:
        db_table = 'system_dict'
        verbose_name = "字典表"
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)

class DictItem(CoreModel):
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name="显示名称", help_text="显示名称")
    key = models.CharField(max_length=100, blank=True, null=True, verbose_name="实际值", help_text="实际值")
    show_title = models.CharField(max_length=64, blank=True, verbose_name="类型转文字", help_text="类型转文字")
    status = models.CharField(max_length=8, blank=True, null=True, verbose_name="状态", help_text="状态", default='1')
    dict = models.ForeignKey(to="Dict", db_constraint=False, related_name="dictItem", on_delete=models.CASCADE,
                             help_text="字典")
    remark = models.CharField(max_length=2000, blank=True, null=True, verbose_name="备注", help_text="备注")
    # 针对依据文件的字段
    doc_name = models.CharField(max_length=64, blank=True, null=True, verbose_name="文档名称", help_text="文档名称")
    publish_date = models.CharField(max_length=64, blank=True, null=True, verbose_name="发布日期", help_text="发布日期")
    source = models.CharField(max_length=32, blank=True, null=True, verbose_name='来源', help_text="来源")

    def __str__(self):
        return f'字典项名称:{self.title}-字典项显示名称:{self.show_title}'

    class Meta:
        db_table = 'system_dict_item'
        verbose_name = "字典表item表"
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)

# ~~~~~~~~~~~~~用户文档片段~~~~~~~~~~~~~
## 用户字典字段：和生成文档强关联
class UserField(CoreModel):
    name = models.CharField("字段名称-字母", max_length=64)

    class Meta:
        abstract = True
        verbose_name = '用户字段核心抽象模型'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime', '-id')

class WordField(UserField):
    frag = models.ForeignKey("Fragment", related_name='uWFeild', related_query_name='uWQField', on_delete=models.CASCADE)
    word = models.CharField("单行文本", max_length=1024)

    class Meta:
        db_table = 'fragment_field_word'
        verbose_name = '储存当行文本'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime', '-id')

class TextField(UserField):
    # 以;号分隔为段落
    text = models.TextField("多行文本段落")
    frag = models.ForeignKey("Fragment", related_name='uTFeild', related_query_name='uTQField', on_delete=models.CASCADE)

    class Meta:
        db_table = 'fragment_field_text'
        verbose_name = '储存当行文本'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime', '-id')

class PictureField(UserField):
    img = models.ImageField("图片", upload_to="field_images")
    frag = models.ForeignKey("Fragment", related_name='uPFeild', related_query_name='uPQField', on_delete=models.CASCADE)

    class Meta:
        db_table = 'fragment_field_picture'
        verbose_name = '图片'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime', '-id')

class TableField(UserField):
    frag = models.ForeignKey("Fragment", related_name='uBFeild', related_query_name='uBQField', on_delete=models.CASCADE)
    # 以逗号分隔，表示表头信息
    headers = models.CharField("表头", max_length=1024, null=True, blank=True)
    # 以逗号分隔，根据标头数量确定行和列
    text = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'fragment_field_table'
        verbose_name = '图片'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime', '-id')

# fragment表
class Fragment(CoreModel):
    belong_doc_choice = (
        (1, DocNameEnum.dg),
        (2, DocNameEnum.sm),
        (3, DocNameEnum.jl),
        (4, DocNameEnum.hsm),
        (5, DocNameEnum.hjl),
        (6, DocNameEnum.bg),
        (7, DocNameEnum.wtd)
    )
    name = models.CharField(verbose_name='片段名称-必须和文件名一致', max_length=128)
    belong_doc = models.PositiveSmallIntegerField("所属文档", choices=belong_doc_choice)
    # 关联的项目
    project = models.ForeignKey(Project, related_name='frag', related_query_name='qFrag', on_delete=models.DO_NOTHING)
    field_seq = models.CharField(max_length=64, verbose_name='用户字段表的顺序')
    is_main = models.BooleanField(default=False, verbose_name='是否替换磁盘的片段')

    class Meta:
        db_table = 'fragment_core'
        verbose_name = '文档片段'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime', '-id')
        # 片段名称name和所属产品文档联合唯一
        constraints = [
            models.UniqueConstraint(fields=['name', 'belong_doc'], name='unique_name_belong_doc')
        ]
