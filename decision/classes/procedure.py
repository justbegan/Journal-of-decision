
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
# import xlsxwriter
# from xlrd import open_workbook
# from xlutils.copy import copy
# from openpyxl.writer.excel import save_virtual_workbook
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from decision.models import *
from decision.forms import *
from klassifikator.models import *
from django.views.generic import View
# Create your views here.
from time import time
from django.http import JsonResponse
#import pyodbc
from decision.filters import *
from decision.classes.Connect_user_fio import *
from datetime import date

import datetime as dd

now = dd.datetime.now()


#add ulus and otdel
def procedure_stats(type):
    if type == "отдел":
        count = 0
        otdel_list = ['ОУП №1 Якутск','ОУП №2 Алдан','ОУП №3 Ленск','ОУП №4 Н-Бестях','ОУП №5 Покровск','ОУП №6 Мирный','ОУП №7 Нерюнгри','ОУП №8 Сунтар']
        for i in otdel_list:
            count = count+1
            Stats.objects.update_or_create(otdel=count,otdel_name = i)
    if type == "улус":
        count_1 = 0
        ra = Raion.objects.values_list('raion')
        for ii in ra:
            count_1 = count_1 +1
            Stats_ulus.objects.update_or_create(ulus=count_1,ulus_name=ii[0])




#end add
def proc_in_stats(type):
    if type == "отдел":
        for i in Stats.objects.values_list('otdel'):
            last_1 = 0
            last_3 = 0
            time_over = 0

            otdel_count = Decision.objects.filter(usr_departament_code=i[0],dec_status='Активный').values_list().count()
            Stats.objects.filter(otdel = i[0]).update(quantity=otdel_count)


            for ii in Decision.objects.filter(usr_departament_code=i[0],dec_status='Активный').values_list('recovery_time'):
                if days_between(str(now.date()),str(ii[0]))==3:
                    last_3 = last_3+1
                if days_between(str(now.date()), str(ii[0])) < 0:
                    time_over = time_over+1
                if days_between(str(now.date()), str(ii[0])) == 0:
                    last_1 = last_1+1

            Stats.objects.filter(otdel=i[0]).update(over_dec=time_over,last_day = last_1,left_3_day=last_3)

    if type == "улус":
        for i in Stats_ulus.objects.values_list('ulus'):
            last_1 = 0
            last_3 = 0
            time_over = 0

            ulus_count = Decision.objects.filter(usr_district_code=i[0],dec_status='Активный').values_list().count()
            Stats_ulus.objects.filter(ulus=i[0]).update(quantity=ulus_count)

            for ii in Decision.objects.filter(usr_district_code=i[0],dec_status='Активный').values_list('recovery_time'):
                if days_between(str(now.date()), str(ii[0])) == 3:
                    last_3 = last_3 + 1
                if days_between(str(now.date()), str(ii[0])) < 0:
                    time_over = time_over + 1
                if days_between(str(now.date()), str(ii[0])) == 0:
                    last_1 = last_1 + 1

            Stats_ulus.objects.filter(ulus=i[0]).update(over_dec=time_over, last_day=last_1, left_3_day=last_3)






def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return (d2 - d1).days





