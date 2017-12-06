from django.shortcuts import render,HttpResponse,redirect
from django.db.models import Count
from question_foruser import  models
from django.forms import  ModelForm
from django.forms import  widgets as wb
class QuestionForm(ModelForm):
    class Meta:
        model=models.Question
        fields='__all__'
        widgets = {  # 格式
            'name': wb.Textarea(attrs={"cols":50,"rows":2})
        }

class OptionFrom(ModelForm):
    class Meta:
        model=models.Option
        fields=["name","value"]

def edit_item(request,nid):
    # print(nid)
    # question_list=models.Question.objects.filter(questionnaire_id=nid)
    # print(question_list)
    #方法一
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
    #方法二
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
            form=QuestionForm()
            yield {"form":form,'obj':None,"option_class":"hide","options":None}
        else:
            for que in question_list:
                form=QuestionForm(instance=que)
                temp={"form":form,"obj":que,"option_class":"hide","options":None}
                if que.tp ==2:
                    temp["option_class"]=''
                    def inner_loop(quee):
                        option_list = models.Option.objects.filter(qs=quee)
                        for v in option_list:
                           yield {"form":OptionFrom(instance=v),"obj":v}
                    temp["options"]=inner_loop(que)
                yield  temp
    return render(request, "form_index.html", {"form": inner()})










# Create your views here.
def index(request):
    questionnaire_list=models.Questionnaire.objects.all().annotate(x=Count("cls__student"))

    join_num = []
    for questionnaire in questionnaire_list:
        join_num.append((questionnaire.id, questionnaire.cls.student_set.count()))

    print(questionnaire_list)

    return  render(request,"index.html",{"questionnaire_obj": questionnaire_list})
def del_item(request,del_id):
    del_id=int(del_id)
    print(type(del_id))
    models.Questionnaire.objects.filter(id=del_id).delete()
    return  redirect("/index/")

def save_item(request,save_id):
    pass


