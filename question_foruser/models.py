from django.db import models

# Create your models here.
class UserInfo(models.Model):
    """"用户"""
    name=models.CharField(max_length=32)
    pwd=models.CharField(max_length=32)
    def __str__(self):
        return  self.name
    class Meta:
        verbose_name_plural="用户表"
class Student(models.Model):
    """学生"""
    name=models.CharField(max_length=32)
    pwd=models.CharField(max_length=32)
    cls=models.ForeignKey(to="Class")
    class  Meta:
        verbose_name_plural="学生表"
    def __str__(self):
        return  self.name
class Class(models.Model):
    """班级"""
    name=models.CharField(max_length=32)
    user_teacher=models.ForeignKey(to="UserInfo")
    class Meta:
        verbose_name_plural="班级表"
    def __str__(self):
        return  self.name
class Questionnaire(models.Model):
    """问卷表"""
    name=models.CharField(max_length=64)
    creater=models.ForeignKey(to="UserInfo")
    cls=models.ForeignKey(to="Class")
    class Meta:
        verbose_name_plural="问卷表"
    def __str__(self):
        return  self.name
class Question(models.Model):
    """问题表"""
    name=models.CharField(max_length=64)
    question_type=(
        (1,"打分"),
        (2,"单选"),
        (3,"评价"),
    )
    tp=models.IntegerField(choices=question_type)
    questionnaire=models.ForeignKey(to="Questionnaire",default=1)
    class Meta:
        verbose_name_plural="问题表"
    def __str__(self):
        return self.name
class Option(models.Model):
    """单选题"""
    name=models.CharField(verbose_name="内容",max_length=32)
    value=models.IntegerField(verbose_name="分值" ,default=8)
    qs=models.ForeignKey(to="Question")
    class Meta:
        verbose_name_plural="单选题"
    def __str__(self):
        return  self.name
class Answer(models.Model):
    """答案"""
    stu_id=models.ForeignKey(to="Student")
    question_id=models.ForeignKey(to="Question",verbose_name='关联的第几题')
    option=models.ForeignKey(to="Option")
    val=models.IntegerField(null=True,blank=True)
    content = models.CharField(max_length=255,null=True,blank=True)
    def __str__(self):
        return self.content
    class Meta:
        verbose_name_plural="答案"



