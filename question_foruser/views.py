import json
from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Count
from question_foruser import models
from django.forms import ModelForm
from django.forms import Form
from django.forms import fields

from django.forms import widgets as wb


# from django.forms import  widgets
class QuestionForm(ModelForm):
    class Meta:
        model = models.Question
        fields = '__all__'
        widgets = {  # 格式
            'name': wb.Textarea(attrs={"cols": 50, "rows": 2})
        }


class OptionFrom(ModelForm):
    class Meta:
        model = models.Option
        fields = ["name", "value"]


# Create your views here.
def edit_item(request, nid):
    # print(nid)
    # question_list=models.Question.objects.filter(questionnaire_id=nid)
    # print(question_list)
    # 方法一
    # form_list = []
    # if not question_list:
    #     form=QuestionForm()#如果不放在列表里不能循环因为他虽然是个空的也是有值的
    #     form_list.append(form)
    #     return render(request,"form_index.html",{"form":form_list})
    # else:
    #     for que in question_list:
    #         form=QuestionForm(instance=que)
    #         form_list.append(form)
    #     return render(request, "form_index.html", {"form": form_list})
    # 方法二
    # def inner():
    #     question_list = models.Question.objects.filter(questionnaire_id=nid)
    #     if not question_list:
    #         form=QuestionForm()
    #         yield {"form":form,'obj':None,"option_class":"hide","options":None}
    #     else:
    #         for que in question_list:
    #             form=QuestionForm(instance=que)
    #             temp={"form":form,"obj":que,"option_class":"hide","options":None}
    #             if que.tp ==2:
    #                 temp["option_class"]=''
    #                 option_model_list=[]
    #                 option_list=models.Option.objects.filter(qs=que)
    #                 for v in option_list:
    #                     vm=OptionFrom(instance=v)
    #                     option_model_list.append(vm)
    #                 temp["options"]=option_model_list
    #
    #                 print(temp["options"])
    #             yield  temp
    #
    #
    # return render(request, "form_index.html", {"form": inner()})
    # 方法三
    def inner():
        question_list = models.Question.objects.filter(questionnaire_id=nid)
        if not question_list:
            form = QuestionForm()
            yield {"form": form, 'obj': None, "option_class": "hide", "options": None}
        else:
            for que in question_list:
                print(que, "所有的问题")
                form = QuestionForm(instance=que)
                temp = {"form": form, "obj": que, "option_class": "hide", "options": None}
                if que.tp == 2:
                    print(que.tp)
                    temp["option_class"] = ''

                    def inner_loop(quee):
                        option_list = models.Option.objects.filter(qs=quee)
                        print(option_list, "问题选项")
                        for v in option_list:
                            print(v, "********")
                            yield {"form": OptionFrom(instance=v), "obj": v}

                    temp["options"] = inner_loop(que)
                    # print(inner_loop(que))
                yield temp

    return render(request, "form_index.html", {"form": inner(), "nid": nid})


def index(request):
    questionnaire_list = models.Questionnaire.objects.all().annotate(x=Count("cls__student"))

    join_num = []
    for questionnaire in questionnaire_list:
        # print(questionnaire.question_set.all())
        part_num = models.Answer.objects.filter(question_id__in=questionnaire.question_set.all()).values_list("stu_id")
        print(part_num, "********")

        join_num.append((questionnaire.id, questionnaire.cls.student_set.count()))

    print(questionnaire_list)

    return render(request, "index.html", {"questionnaire_obj": questionnaire_list})


def del_item(request, del_id):
    del_id = int(del_id)
    print(type(del_id))
    models.Questionnaire.objects.filter(id=del_id).delete()
    return redirect("/index/")


def login(request):
    stu_obj = models.Student.objects.filter(name="杨磊").first()
    request.session["stu_info"] = {"id": stu_obj.id, "user": stu_obj.name}
    return HttpResponse("登陆成功")


def save_item(request, save_id):
    # print(save_id)
    print(json.loads(request.body.decode("utf-8")))
    question_list = json.loads(request.body.decode("utf-8"))
    qL = []
    qL2 = []
    for i in question_list:
        type1 = i.get("type")
        print(type(type1))
        if type1 != '2':
            qL.append(i)
        else:
            qL2.append(i)
    print(qL, '前端传的数据问题类型为1或3')
    print(qL2, '前端传的数据问题类型为2')
    questionnaire_obj = models.Questionnaire.objects.filter(id=save_id)[0]
    print(questionnaire_obj)
    question_list = models.Question.objects.filter(questionnaire=questionnaire_obj)
    qL1 = []
    qL21 = []
    for i in question_list:
        if i.tp != 2:
            qL1.append({"pid": save_id, "title": i.name, "type": i.tp})
        else:
            option_list1 = []
            option_list = models.Option.objects.filter(qs_id=2)
            print(option_list, "问题选项")
            for s in option_list:
                option_list1.append({"id": s.id, "title": s.name, "val": s.value})
            qL21.append({"pid": save_id, "title": i.name, "type": i.tp, "options": option_list1})
    print(qL21, "后端数据类型是2的")
    print(qL1, "后端数据类型是1或3")
    # 开始业务判断
    question_l = []  #
    for i in qL:
        # print(type(i.get("type")),'前端数据的类型')
        question_l.append(i.get("type"))

    question_l1 = []  # 这是后端的数据
    for y in qL1:
        question_l1.append(y.get("type"))

    # 先删除  在后端不在前端
    for i in question_l1:
        if str(i) not in question_l:
            models.Question.objects.filter(tp=i, questionnaire_id=save_id).delete()

    # 添加  在前端不在后端：
    for y in qL:
        if int(y.get("type")) not in question_l1:
            form = QuestionForm(name=y.get("title"), tp=y.get("type"), questionnaire_id=save_id)
            if form.is_valid():
                form.save()

    # 在端又在后端   先删除后端在添加前端的数据
    for y in qL:
        if int(y.get("type")) in question_l1:
            models.Question.objects.filter(tp=int(y.get("type")), questionnaire_id=save_id).delete()
            # form = QuestionForm(name=y.get("title"), tp=y.get("type"), questionnaire_id=save_id)
            # if form.is_valid():
            #     form.save()
            models.Question.objects.create(name=y.get("title"), tp=y.get("type"), questionnaire_id=save_id)
    # 先删除
    # 如果前端没有值 后端也没有值什么也不做； 反之把后端的数据删除
    if not qL2:
        if qL21:
            models.Question.objects.filter(tp=2, questionnaire_id=save_id).delete()
        else:
            pass
    if qL2:
        models.Question.objects.filter(tp=2, questionnaire_id=save_id).delete()
        for i in qL2:
            question_obj = models.Question.objects.create(tp=2, questionnaire_id=save_id, name=i["title"])
            # if form.is_valid():
            #     form.save()
    z_list = []
    for i in qL21:
        for z in i.get("options"):
            z_list.append(z["title"])
    if qL2:
        for i in qL2:
            for z in i["options"]:
                if not z.get("id"):  # 所有空项目
                    # form=OptionFrom(qs_id=2,name=i.get("title"),value=i.get("val"))
                    # if form.is_valid():
                    #     form.save()
                    models.Option.objects.create(qs_id=2, name=z.get("title"), value=int(z.get("val")))
                elif z.get("title") in z_list:
                    models.Option.objects.filter(qs_id=save_id, name=z.get("title")).delete()
                    # form=OptionFrom(qs_id=save_id,name=i.get("title"),value=i.get("val"))
                    # if form.is_valid():
                    #     form.save()
                    models.Option.objects.create(qs_id=save_id, name=z.get("title"), value=int(z.get("val")))

    return HttpResponse(json.dumps(True))


def save2_item(request, qid):  # 保存问题
    ajax_question_list = json.loads(request.body.decode("utf-8"))
    '''
   ajax_question_list= [
       {
       'pid': '28',
        'title': '对我们的评价', 
        'type': '3'
        },
         {
         'pid': '29', 
         'title':'老师长的帅不帅',
          'type': '1'
          }, 
             {
             'pid': '30',
              'title': '老师怎么样',
               'type': '2',
                'options': [
                {'id': '', 'title': '很帅', 'val': '10'}, 
                {'id': '', 'title': '帅', 'val': '9'},
                 {'id': '', 'title': '一般', 'val': '8'}
                 ]
                 }
         ]
    '''
    print(ajax_question_list, '前端传来的数据')
    ret = {"status": True, "error": None, "data": None}
    try:
        ajax_question_id = [(item.get("pid")) for item in ajax_question_list if item.get("pid")]
        question_list = models.Question.objects.filter(questionnaire_id=qid)
        question_id_list = [str(item.id) for item in question_list]
        print(question_id_list, "数据库的问题id")
        print(ajax_question_id, "前端传来的id")
        question_del_id = set(question_id_list).difference(ajax_question_id)  # 删除在数据库里但是没有在前端的id
        for item in ajax_question_list:
            pid = item.get("pid")
            title = item.get("title")
            type = item.get("type")
            op = item.get("options")
            print(op,"选项")

            if pid not in question_id_list:
                print(6666)
                new_question_obj = models.Question.objects.create(name=title, tp=int(type),
                                                                  questionnaire_id=qid)  # 如果在前端没有在后端就添加
                if not op:
                    models.Option.objects.filter(qs_id=int(pid)).delete()
                else:
                    # 不推荐使用
                    models.Option.objects.filter(qs_id=int(pid)).delete()
                    for item in op:
                        print(item,"op里面的内容")
                        models.Option.objects.create(name=item.get("title"), value=int(item.get("val")),
                                                     qs=new_question_obj)
                        print("执行啦")
            else:
                models.Question.objects.filter(id=int(pid)).update(name=title, tp=type)# 如果前后端都有那就更新
                new_question_obj =models.Question.objects.filter(id=int(pid)).first()
                print("更新的内容")
                if not op:
                    models.Option.objects.filter(qs_id=int(pid)).delete()
                else:
                    # 不推荐使用
                    models.Option.objects.filter(qs_id=int(pid)).delete()
                    for item in op:
                        print(item, "op里面的内容")
                        models.Option.objects.create(name=item.get("title"), value=int(item.get("val")),
                                                     qs=new_question_obj)
                        print("执行啦")
            # 删除所有没在里面的id
            models.Question.objects.filter(id__in=question_del_id).delete()  # 删除这个数据
    except Exception as e:
        ret["status"]=False
        ret["error"]=str(e)
    return HttpResponse(json.dumps(ret))


def answer_question(request, cls_id, qn_id):
    stu_id = request.session["stu_info"].get("id")
    # 判断是不是这个班的学生
    ret=models.Student.objects.filter(id=stu_id,cls_id=cls_id)
    # ret=models.Student.objects.filter(id=stu_id,cls_id=cls_id).count()
    if not ret:
        return HttpResponse("你不是这个班的学生")
    ret1 = models.Answer.objects.filter(stu_id_id=stu_id, question_id__questionnaire_id=qn_id).count()
    if ret1:
        return HttpResponse("对不起您已经做个了")
    question_list1 = models.Question.objects.filter(questionnaire_id=qn_id)
    print(question_list1, "获取问题")
    field_dict = {}
    from django.core.exceptions import ValidationError
    def func(que):
        if len(que) < 15:
            raise ValidationError("你的太短")
    for question1 in question_list1:
        if question1.tp == 1:
            field_dict["val_%s" % question1.id] = fields.ChoiceField(
                required=True,
                error_messages={"required": "必填"},
                label=question1.name,
                choices=[(i, i) for i in range(1, 11)],
                widget=wb.RadioSelect,
            )
        elif question1.tp == 2:
            field_dict["option_id_%s" % question1.id] = fields.ChoiceField(
                label=question1.name,
                error_messages={"required": "必填"},
                choices=models.Option.objects.filter(qs=question1).values_list("id", "name"),

                widget=wb.RadioSelect,
            )
        else:
            field_dict["content_%s" % question1.id] = fields.CharField(
                label=question1.name,
                widget=wb.Textarea,
                validators=[func, ]#自定义的form验证类型
            )
    AnswerForm = type('AnswerForm', (Form,), field_dict)
    if request.method == "GET":
        form = AnswerForm()
        return render(request, "answer_question.html", {"form": form})
    elif request.method == "POST":
        form = AnswerForm(data=request.POST)#(通过request.POST来取数据)
        if form.is_valid():
            dict1 = {}
            print(form.cleaned_data, "clean_data")
            for k, v in form.cleaned_data.items():#取form.cleaned_data的数据用.items()
                k, qid = k.rsplit("_", 1)
                print(k, qid, "qid")
                answer_dict = {"stu_id_id": stu_id, "question_id_id": qid, k: v}  #数据的拼接
                models.Answer.objects.create(**answer_dict)#用键值对的形式
            return HttpResponse("感谢参与")

        else:
            return render(request, "answer_question.html", {"form": form})
