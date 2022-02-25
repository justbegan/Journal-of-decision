from django.db import models
from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
from dateutil.relativedelta import relativedelta
import datetime as dd
now = dd.datetime.now()
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
class Article_cl(models.Model):
    code = models.CharField('Код статьи',max_length=5)
    title = models.CharField('Название статьи', max_length=200)
    def __str__(self):
        return self.title

class Pension_type_cl(models.Model):
    title = models.CharField('Вид пенсии', max_length=100)
    code = models.CharField('Код вида пенсии', max_length=100)
    def __str__(self):
        return self.title


class Decision(models.Model):
    choices = (
        ('Активный', 'Активный'),
        ('Завершенный', 'Завершенный'),
    )
    dec_status = models.CharField('Состояние', choices=choices, max_length=15, default='')
    usr_departament_code = models.CharField('Код отдела',max_length=200,default='Auto',null=True)
    usr_district_code = models.CharField('Код улуса',max_length=100,default='Auto',null=True)
    snils = models.CharField('Снилс',max_length=16,default='')
    fio = models.CharField('ФИО',max_length=100,default='')
    types_of_pension = models.ForeignKey(Pension_type_cl,null=True, on_delete=models.SET_NULL, verbose_name="Виды пенсий")
    law = models.ForeignKey(Article_cl,null=True,on_delete=models.SET_NULL,verbose_name="Статья закона")
    appeal_date = models.DateField('Дата обращения')
    statement_reg_num = models.CharField('Рег. номер заявления',max_length=100)
    choices_appeal = (('назначение','назначение'),('перерасчет','перерасчет'),('перевод','перевод'),('восстановление','восстановление'),('возобновление','возобновление'))
    appeal_type = models.CharField('Вид обращения',choices=choices_appeal,max_length=100)
    adress = models.CharField('Адрес',max_length=200)
    note = models.CharField('Примечание',max_length=200,blank=True)
    #block2
    decision_date = models.DateField('Дата решения')
    decision_number = models.CharField('Номер решения',max_length=30,default="Номер решения_1")
    choices_cause = (('проведением проверки','проведением проверки'),('непредставлением иными государственными органами в установленный срок','непредставлением иными государственными органами в установленный срок'))
    cause = models.CharField('Причина',choices=choices_cause,max_length=100)
    user_fio = models.CharField('ФИО специалиста',max_length=100,default="auto")
    #block3
    recovery_time = models.DateField('Срок восстановления',blank=True)
    decision_date_block3 = models.DateField('Дата решения востановления',blank=True,null=True)
    decision_number_2 = models.CharField('Номер решения ',max_length=30,default="Номер решения_2")
    choices_cause_2 = (
        ('Завершение проверки', 'Завершение проверки'),
        ('Поступление ответ', 'Поступление ответ'),
        ('Истечение 3-х мес.срока','Истечение 3-х мес.срока')
    )
    cause_2 = models.CharField('Причина, Востановления срока',choices=choices_cause_2,max_length=100,blank=True,null=True)
    add_time = models.CharField('Дата добавления', default=datetime.now(), max_length=50)
    actual_term = models.CharField('Cрок обработки обращения',default='0',max_length=20)

    def save(self,*args,**kwargs):
        self.decision_number = str(self.statement_reg_num) + str("П")
        self.decision_number_2 = str(self.statement_reg_num) + str("В")
        self.recovery_time = self.decision_date + relativedelta(months=+3)

        if self.decision_date_block3 == None:
            pass
        else:
            self.actual_term = str(self.days_between(str(self.decision_date),str(self.decision_date_block3)))
        super(Decision,self).save(*args,**kwargs)

    def days_between(self,d1, d2):
        d1 = datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.strptime(d2, "%Y-%m-%d")
        return (d2 - d1).days


class Chrono(models.Model):
    ch_snils = models.CharField('Снилс', max_length= 100)
    add_time = models.CharField('Дата добавления', default=datetime.now(), max_length=50)
    user_login = models.CharField('Логин специалиста', max_length= 100)
    info = models.CharField('Примечание',max_length=200,default='')




class Upfr_cl(models.Model):
    org_name = models.CharField('Наименование управления',max_length=100,null=True)
    director_poss = models.CharField('Должность руководителя', max_length=100, null=True)
    director_fio = models.CharField('ФИО руководителя', max_length=100, null=True)

class Departament_cl(models.Model):
    departament_title = models.CharField('Наименование отдела', max_length=100)
    departament_code = models.CharField('Код отдела',unique=True,max_length=100)
    director_poss = models.CharField('Должность руководителя', max_length=100, null=True)
    director_fio = models.CharField('ФИО руководителя', max_length=100, null=True)

class Distric_cl(models.Model):
    distric_name = models.CharField('Наименование улуса', max_length=100)
    distric_code = models.CharField('Код улуса',max_length=100,unique=True)

class Profile(models.Model):
    user = models.CharField('Догин',max_length=100,default="00")
    otdel_code = models.CharField('Код отдела',max_length=10,default="00",blank=True)
    district = models.CharField('Код улуса ',max_length=10,blank=True)
    choise_role = (
        ('Специалист отдела', 'Специалист отдела'),
        ('Руководитель отдела', 'Руководитель отдела'),
        ('Руководитель управления','Руководитель управления'),
        ('Контроль','Контроль')
    )
    role = models.CharField('Роль',choices=choise_role,default='Специалист отдела',max_length=30)
    def __str__(self):
        return 'user:{0} otdel_code:{1} district:{2}'.format(self.user,self.otdel_code,self.district)

class Stats(models.Model):
    otdel_name = models.CharField('Наименование отдела',max_length=100,blank=True,null=True)
    otdel = models.CharField('Отдел',max_length=10)
    quantity = models.CharField('Количество', max_length=10,default="0")
    over_dec = models.CharField('Просроченные', max_length=10,default="0")
    last_day = models.CharField('Последний день', max_length=10,default="0")
    left_3_day = models.CharField('Осталось 3 дня', max_length=10,default="0")


class Stats_ulus(models.Model):
    ulus_name = models.CharField('Наименование улуса', max_length=100,blank=True,null=True)
    ulus = models.CharField('улус',max_length=10)
    quantity = models.CharField('Количество', max_length=10,default="0")
    over_dec = models.CharField('Просроченные', max_length=10,default="0")
    last_day = models.CharField('Последний день', max_length=10,default="0")
    left_3_day = models.CharField('Осталось 3 дня', max_length=10,default="0")


class CreateUlusOtdel(models.Model):
    on_or_off = models.BooleanField('Создать улус и отделы',blank=True,null=True)

class Art_and_Pens(models.Model):
    choices_appeal = (('назначение', 'назначение'), ('перерасчет', 'перерасчет'), ('перевод', 'перевод'),
                      ('восстановление', 'восстановление'), ('возобновление', 'возобновление'))

    choices_suspension = (('частью 8 статьи 22 Федерального закона от 28.12.2013 № 400-ФЗ "О страховых пенсиях"','частью 8 статьи 22 Федерального закона от 28.12.2013 № 400-ФЗ "О страховых пенсиях"'),('частью 7 статьи 23 Федерального закона от 28.12.2013 № 400-ФЗ "О страховых пенсиях"','частью 7 статьи 23 Федерального закона от 28.12.2013 № 400-ФЗ "О страховых пенсиях"'),('частью 6 статьи 10 Федерального закона от 28.12.2013 № 424-ФЗ "О накопительной пенсии"','частью 6 статьи 10 Федерального закона от 28.12.2013 № 424-ФЗ "О накопительной пенсии"'),('пунктом 4 статьи 24 Федерального закона от 15.12.2001 № 166-ФЗ "О государственном пенсионном обеспечении в РФ"','пунктом 4 статьи 24 Федерального закона от 15.12.2001 № 166-ФЗ "О государственном пенсионном обеспечении в РФ"'),('статьи 2 Федерального закона от 27.11.2001 № 155-ФЗ "О дополнительном социальном обеспечении членов летных экипажей воздушных судов гражданской авиации"','статьи 2 Федерального закона от 27.11.2001 № 155-ФЗ "О дополнительном социальном обеспечении членов летных экипажей воздушных судов гражданской авиации"'),('части 4.1 статьи 4 Федерального закона от 10.05.2010 № 84-ФЗ "О дополнительном социальном обеспечении отдельных категорий работников организаций угольной промышленности"','части 4.1 статьи 4 Федерального закона от 10.05.2010 № 84-ФЗ "О дополнительном социальном обеспечении отдельных категорий работников организаций угольной промышленности"'),('постановления Правительства РФ от 07.06.2002 № 390','постановления Правительства РФ от 07.06.2002 № 390'),('постановления Правительства РФ от 04.06.2007 N 343','постановления Правительства РФ от 04.06.2007 N 343'),('постановление Правительства РФ от 02.05.2013 N 397','постановление Правительства РФ от 02.05.2013 N 397')
    )
    appeal_type = models.CharField('Вид обращения', choices=choices_appeal, max_length=100)
    law = models.ForeignKey(Article_cl, null=True, on_delete=models.SET_NULL, verbose_name="Статья закона")
    ground_for_suspension = models.CharField('Основание приостановления',choices=choices_suspension, max_length=500)

    def __str__(self):
        return 'Вид обращения:{0} Статья закона:{1} Основание приостановления:{2}'.format(self.appeal_type,self.law, self.ground_for_suspension)


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,

        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email 					= models.CharField(verbose_name="Логин", max_length=60, unique=True)
    username 				= models.CharField('ФИО',max_length=30, unique=True)
    date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin				= models.BooleanField('Админ',default=False)
    is_active				= models.BooleanField(default=True)
    is_staff				= models.BooleanField(default=False)
    is_superuser			= models.BooleanField(default=False)
    otdel = models.CharField('Отдел', max_length=60,default="0")
    rayon = models.CharField('Район', max_length=60,default="0")
    choise_role = (
        ('Специалист отдела', 'Специалист отдела'),
        ('Руководитель отдела', 'Руководитель отдела'),
        ('Руководитель управления', 'Руководитель управления'),
        ('Контроль', 'Контроль'))
    role = models.CharField('Роль',max_length=30,choices=choise_role, default='специалист-отдела')


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True



