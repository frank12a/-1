from django.forms import  Form
from django.forms import fields
from django.forms import widgets,ValidationError
from . import  models
class QuestForm(Form):
    name=fields.CharField(
        required=True,
        error_messages={'required':'必须写内容'},
        widget=widgets.TextInput()
    )

    tp=fields.ChoiceField(choices=[])
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["tp"].choices=models.Question.question_type.values("name","tp")

