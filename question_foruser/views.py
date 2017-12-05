from django.shortcuts import render,HttpResponse,redirect
from django.db.models import Count
from question_foruser import  models

# Create your views here.
def index(request):
    questionnaire_list=models.Questionnaire.objects.all().annotate(x=Count("cls__student"))

    # join_num = []
    for questionnaire in questionnaire_list:
        # join_num.append((questionnaire.id, questionnaire.cls.student_set.count()))
        print(questionnaire.join_num)
    print(questionnaire_list)

    return  render(request,"index.html",{"questionnaire_obj": questionnaire_list})
def del_item(request,del_id):
    del_id=int(del_id)
    print(type(del_id))
    models.Questionnaire.objects.filter(id=del_id).delete()
    return  redirect("/index/")
def edit_item(request,edit_id):
    edit_id=int(edit_id)
    return  render(request,"edit_questionnaire.html")


