import os

from django.contrib.staticfiles import finders
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
# import xlsxwriter
# from xlrd import open_workbook
# from xlutils.copy import copy
# from openpyxl.writer.excel import save_virtual_workbook
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from Journal_of_decision import settings
from .models import *
from .forms import *
from django.views.generic import View
# Create your views here.
from time import time
from django.http import JsonResponse
#import pyodbc
from .filters import *
from decision.classes.Connect_user_fio import *
from decision.classes.procedure import *
import csv
from django.http import HttpResponse
import datetime as date_time
#pdf
from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
#pdf_end


@login_required(login_url='login')
def display(request,Model,index_header,title_list,page_title,role="0"):

    if Model == Decision:

        if role == 'Контроль' or role == 'Руководитель управления':
            items = Model.objects.all().order_by('-recovery_time')
        elif role == 'Руководитель отдела' and request.user.otdel != "0":
            items = Model.objects.filter(usr_departament_code=request.user.otdel,dec_status='Активный').all().order_by('-recovery_time')
        elif role == 'Специалист отдела' and request.user.otdel != "0":
            items = Model.objects.filter(usr_departament_code=request.user.otdel,dec_status='Активный',user_fio=request.user.username).all().order_by('-recovery_time')
        elif request.user.otdel == "0":
            items = Model.objects.none()
    else:
        items = Model.objects.all()



    myFilter = OrderFilter(request.GET, queryset=items)


    items_f = myFilter.qs

    paginator = Paginator(items_f, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        'items': page_obj,
        'title_list': title_list,
        'header': index_header,
        'page_title': page_title,
        'myFilter': myFilter,

    }

    if 'export' in request.GET:
        return export_csv(request)

    return render(request, 'inv/index.html',context)


def deadline():
    return Decision.objects.filter(recovery_time__lte=date_time.date.today()).values_list('id')

def dis_decision(request):
    #
    # if Profile.objects.filter(user_id=request.user.id).count()==0:
    #     return render(request, 'inv/errorpage.html', {'error': "У пользователя не настроены права доступа"})
    # else:
    title_list = ['id', 'Состояние', 'Код отдела', 'Код улуса', 'Снилс', 'ФИО','Срок восстановления']
    return display(request,Decision,'decision',title_list,"Решения",request.user.role)


def dis_Art_and_Pens(request):
    title_list = ['id', 'Вид обращения', 'Основание обращения', 'Основание приостановления']
    return display(request,Art_and_Pens,'art_and_pens',title_list,"Классификатор основания приостановления")




def dis_chrono(request):
    title_list = ['id', 'Снилс', 'Время добавления', 'Логин специалиста','Примечание']

    return display(request,Decision,'chrono',title_list,"Хронология",request.user.role)




def dis_cl_articles(request):
    title_list = ['id','Название','Код']
    return display(request,Article_cl,'article_cl',title_list,"Статьи",request.user.role)

def dis_cl_pens_type(request):
    title_list = ['id','Название','Код']
    return display(request,Pension_type_cl,'pension_type_cl',title_list,"Вид пенсии",request.user.role)

def dis_stats(request):
    if CreateUlusOtdel.objects.all().count()==0:
        procedure_stats("отдел")
    proc_in_stats("отдел")
    title_list =['id','Отдел','Количество','Просроченные','Последний день','Осталось 3 дня']
    return display(request, Stats, 'dis_stats', title_list, "Статистика отделов")


def dis_stats_ulus(request):
    if CreateUlusOtdel.objects.all().count()==0:
        procedure_stats("улус")
    proc_in_stats("улус")
    title_list = ['id', 'улус', 'Количество', 'Просроченные', 'Последний день', 'Осталось 3 дня']
    return display(request, Stats_ulus, 'dis_stats_ulus', title_list, "Статистика улусов")

def rol_confines(func):
    def wrapper(request):
        if request.user.is_admin == True:
            return func(request)
        else:
            return render(request, 'inv/errorpage.html', {'error': "У пользователя нет права доступа"})
    return wrapper

@rol_confines
def dis_account(request):
    title_list = ['id', 'Логин', 'Фио', 'Роль']
    return display(request, Account, 'account', title_list, "Пользователи")



def edit_item(request, pk, model, cls, name):

    item = get_object_or_404(model, pk=pk)
    if 'pdf_app_1' in request.POST:
        return pdf_app_1(request)
    if 'pdf_app_2' in request.POST:
        return pdf_app_2(request)


    if request.method == "POST":

        form = cls(request.POST, instance=item)

        if form.is_valid():

            form.save()
            if name == "Decision":
                return redirect("/Decision/edit_item/"+str(pk)+"")
            if name == "Account":
                return redirect("/Account/edit_item/" + str(pk) + "")
    else:

        form = cls(instance=item)
        context = {'form': form, 'cls_name':name}
        return render(request, 'inv/edit_item.html', context)

def edit_decision(request,pk):
    return edit_item(request,pk,Decision,DecisionForm,"Decision")

def edit_account(request,pk):

    return edit_item(request,pk,Account,RegForm,"Account")



def add_item(request, cls):
    if request.method == "POST":

        form = cls(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user_fio = request.user.username

            obj.usr_departament_code = request.user.otdel
            if request.user.role != 'Контроль' or request.user.role != 'Руководитель управления':
                obj.usr_district_code = request.user.rayon

            obj.save()
            if cls == DecisionForm:
                return redirect('dis_decision')
            elif cls == Art_and_PensForm:
                return redirect('dis_art_and_pens')
            # elif cls == UserForm:
            #     return redirect('dis_account')


        else:
            return render(request, 'inv/add_new.html', {'form': form})

    else:

        if cls == DecisionForm:
            form = cls()
            if request.user.role == 'Контроль' or request.user.role == 'Руководитель управления':
                u_role = "admin"
            else:
                u_role = "user"


            return render(request, 'inv/add_new.html', {'form': form,
                                                            'header': 'decision',
                                                            'role':u_role,
                                                            })
        elif cls == Art_and_PensForm:
            form = cls()

            return render(request, 'inv/add_new.html', {'form': form,
                                                        'header':'art_and_pens'
                                                        })

        # elif cls == UserForm:
        #     form = cls()
        #
        #     return render(request, 'inv/add_new.html', {'form': form,
        #                                                 'header':'account'
        #                                                 })


def add_decision(request):
    if request.is_ajax():
        snils = str(request.GET.get("input_text"))
        try:
            return JsonResponse({'stat':1,'ra':str(NVP_return_list(snils)[0][0]),'fio':str(NVP_return_list(snils)[1]),'adress':str(NVP_return_list(snils)[0][4]),'date_z':str(NVP_return_list(snils)[0][5]),'number_z':str(NVP_return_list(snils)[0][6]),},status=200)
        except:
            return JsonResponse({'stat':0,},status=200)
    return add_item(request, DecisionForm)

def add_art_and_pens(requset):
    return add_item(requset, Art_and_PensForm)

#def add_account(request):
#    return add_item(request, UserForm)

def add_account(request):
    context = {}
    if request.POST:
        form = RegForm(request.POST)
        if form.is_valid():
            form.save()
            #email = form.cleaned_data.get('email')
            #raw_password = form.cleaned_data.get('password1')
            #account = authenticate(email=email,password = raw_password)
            #login(request,account)
            return redirect('dis_account')
        else:
            context['form'] = form

    else:
        form = RegForm()
        context['form'] = form
    return render(request,'inv/register.html',context)




def cl_articles(request):
    item = get_object_or_404(Article_cl)

    if request.method == "POST":
        form = Articles_clForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:

        form = Articles_clForm(instance=item)
        context = {
            'form': [form],

        }
        return render(request, 'inv/edit_item.html', context)


def loginPage(request):

    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(request,username= username,password = password)

        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.info(request,'Username or passwrod in incorrect')

    contex ={}
    return render(request,'inv/login_form.html',contex)

def logOutUser(request):

    logout(request)
    return redirect('login')





def export_csv(request):

    response = HttpResponse(content_type='text/csv')
    response.write(u'\ufeff'.encode('utf8'))

    writer = csv.writer(response,delimiter=';')
    writer.writerow(['Номер','номер отдела','код улуса', 'снилс', 'ФИО', 'адрес',
                     'Вид пенсии / иной выплаты','Основание обращения','Дата обращения',
                     'Рег. Номер заявления','Вид обращения','Дата решения','Номер решения',
                     'Причина','ФИО специалиста','Срок восста- новления','Дата решения','Номер решения',
                     'Причина','ФИО специалиста','Срок обработки обращения'])

    rol = request.user.role

    if rol == 'Контроль' or rol == 'Руководитель управления':
        items = Decision.objects.all().values_list('id', 'usr_departament_code', 'usr_district_code', 'snils', 'fio', 'adress', 'types_of_pension', 'law',
         'appeal_date', 'statement_reg_num', 'appeal_type', 'decision_date', 'decision_number', 'cause', 'user_fio',
         'recovery_time', 'decision_date_block3', 'decision_number_2', 'cause_2', 'user_fio', 'actual_term')

    elif rol == 'Руководитель отдела':
        items =  Decision.objects.filter(usr_departament_code=request.user.role).all().values_list('id', 'usr_departament_code', 'usr_district_code', 'snils', 'fio', 'adress', 'types_of_pension', 'law',
         'appeal_date', 'statement_reg_num', 'appeal_type', 'decision_date', 'decision_number', 'cause', 'user_fio',
         'recovery_time', 'decision_date_block3', 'decision_number_2', 'cause_2', 'user_fio', 'actual_term')

    elif rol == 'Специалист отдела':
        items = Decision.objects.filter(usr_departament_code=request.user.role,user_fio=request.user.username).all().values_list('id', 'usr_departament_code', 'usr_district_code', 'snils', 'fio', 'adress', 'types_of_pension', 'law',
         'appeal_date', 'statement_reg_num', 'appeal_type', 'decision_date', 'decision_number', 'cause', 'user_fio',
         'recovery_time', 'decision_date_block3', 'decision_number_2', 'cause_2', 'user_fio', 'actual_term')


    myFilter = OrderFilter(request.GET, queryset=items)
    items_f = myFilter.qs
    for member in items_f:
        writer.writerow(member)

    response['Content-Disposition'] = 'attachment; filename="11.csv"'
    return response





def delete_decision(request,pk):

    Decision.objects.filter(id=pk).delete()
    return dis_decision(request)

def delete_art_and_pens(request,pk):

    Art_and_Pens.objects.filter(id=pk).delete()
    return dis_Art_and_Pens(request)

#pdf
def fetch_pdf_resources(uri, rel):
    if uri.find(settings.MEDIA_URL) != -1:
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))
    elif uri.find(settings.STATIC_URL) != -1:
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ''))
    else:
        path = None
    return path



def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result,
                            encoding='utf-8',
                            link_callback=fetch_pdf_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def art_and_pens_val(art,pens):
    try:
        return Art_and_Pens.objects.filter(law = str(art),appeal_type= str(pens)).values_list('ground_for_suspension')[0][0]
    except:
        return "Не найдено"

def changer_date_format(d):
    date_object = datetime.strptime(str(d), '%Y-%m-%d').date()
    return date_object

def pdf_app_1(request):
    template_path = 'inv/pdf_app_1.html'
    context = {"decision_date": changer_date_format(request.POST['decision_date']),
            "decision_number": request.POST['decision_number'],
            "fio": request.POST['fio'],
            "statement_reg_num": request.POST['statement_reg_num'],
            "appeal_date": changer_date_format(request.POST['appeal_date']),
            "article_and_pens": art_and_pens_val(request.POST['law'],request.POST['appeal_type']),
            "cause": request.POST['cause'],
            "phone": "555-555-2345",
            "email": "youremail@dennisivy.com",
            "website": "dennisivy.com", }
    return rende_pdf_view(template_path, context)

def pdf_app_2(request):
    template_path = 'inv/pdf_app_2.html'
    context = {"decision_date": changer_date_format(request.POST['decision_date']),
            "decision_number": request.POST['decision_number'],
            "fio": request.POST['fio'],
            "addres": request.POST['adress'],
            "types_of_pension": return_type_of_pens(request.POST['types_of_pension']),
            "cause": request.POST['cause'],
            "article_and_pens": art_and_pens_val(request.POST['law'],request.POST['appeal_type']),}


    return rende_pdf_view(template_path, context)


def rende_pdf_view(template_path,context):

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Приложение_1.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=fetch_pdf_resources)
    # if error then show some funy view

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response


def return_type_of_pens(p_id):
    p_id = str(p_id)
    return Pension_type_cl.objects.filter(id=p_id).values_list('title')[0][0]
#pdf_end


def refresh_pass(pk):
    pk = str(pk)
    print(pk)
    #Account.objects.filter(id = pk).update(password = 'pbkdf2_sha256$216000$Z7Ams5XHSkKv$8jAHocUZ8')
