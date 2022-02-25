from decision.models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm

class DateInput(forms.DateInput):
    input_type = 'date'


class DecisionForm(forms.ModelForm):

    class Meta:
        model = Decision
        fields = ('dec_status','usr_departament_code','snils','usr_district_code','fio','types_of_pension','law','appeal_date','statement_reg_num','appeal_type','adress','note','decision_date','decision_number','cause','user_fio','recovery_time','decision_date_block3','decision_number_2','cause_2','actual_term')
        widgets = {
            'appeal_date': DateInput(format="%Y-%m-%d"),
            'decision_date':DateInput(format="%Y-%m-%d"),
            'recovery_time':DateInput(format="%Y-%m-%d"),
            'decision_date_block3': DateInput(format="%Y-%m-%d"),

        }
class DecisionForm_edit(forms.ModelForm):

    class Meta:
        model = Decision
        fields = ('dec_status','usr_departament_code','snils','usr_district_code','fio','types_of_pension','law','appeal_date','statement_reg_num','appeal_type','adress','note','decision_date','decision_number','cause','user_fio','recovery_time','decision_date_block3','decision_number_2','cause_2','actual_term')




class ChronoForm(forms.ModelForm):
    class Meta:
        model = Decision
        fields = ('snils','add_time','user_fio','note')

class Articles_clForm(forms.ModelForm):
    class Meta:
        model = Article_cl
        fields = ('code','title')

class Pension_type_clForm(forms.ModelForm):
    class Meta:
        model = Pension_type_cl
        fields = ('code','title')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('otdel_code','district')

class Art_and_PensForm(forms.ModelForm):
    class Meta:
        model = Art_and_Pens
        fields = ('appeal_type','law','ground_for_suspension')


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('email','username','role','otdel','rayon')


class RegForm(UserCreationForm):
    #email = forms.CharField(max_length=60)
    class Meta:
        model = Account
        fields = ('email','username','otdel','rayon','role','is_admin','password1','password2')