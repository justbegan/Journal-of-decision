from django.conf.urls import url
from .views import *

urlpatterns = [


    url(r'^login/$', loginPage, name='login'),
    url(r'^logout/$', logOutUser, name='logout'),


    url(r'^$', dis_stats, name='index'),
    url(r'^ dis_decision$', dis_decision, name='dis_decision'),
    url(r'^cl_articles$', dis_cl_articles, name='cl_articles'),
    url(r'^cl_pension_type$', dis_cl_pens_type, name='cl_pension_type'),
    url(r'^dis_stats_ulus$', dis_stats_ulus, name='dis_stats_ulus'),
    url(r'^dis_art_and_pens$', dis_Art_and_Pens, name='dis_art_and_pens'),
    url(r'^dis_account$', dis_account, name='dis_account'),

    url(r'^Decision/edit_item/(?P<pk>\d+)$', edit_decision, name="edit_decision"),
    url(r'^Account/edit_item/(?P<pk>\d+)$', edit_account, name="edit_account"),


    url(r'^chrono$', dis_chrono, name="chrono"),
    url(r'^edit_art_cl$', cl_articles, name="edit_art_cl"),
    #url(r'^render_pdf_view$', render_pdf_view, name="render_pdf_view"),
    #delete
    url(r'^Decision/delete/(?P<pk>\d+)$', delete_decision, name="delete_decision"),
    url(r'^Art_and_Pens/delete/(?P<pk>\d+)$', delete_art_and_pens, name="delete_art_and_pens"),
    #add
    url(r'^add_decision$', add_decision, name="add_decision"),
    url(r'^add_art_and_pens$', add_art_and_pens, name="add_art_and_pens"),
    url(r'^add_account$', add_account, name="add_account"),


    url(r'^Account/refresh_pass/(?P<pk>\d+)$', refresh_pass, name="refresh_pass"),




]