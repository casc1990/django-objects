#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View #view模块

from .models import CourseOrg,Teacher,CityDict

class OrgView(View):
    def get(self,request):
        all_courseorg = CourseOrg.objects.all() #所有的课程机构
        org_num = all_courseorg.count()
        all_city = CityDict.objects.all() #所有的城市
        return render(request,'org-list.html',{
            'all_courseorg':all_courseorg,
            'all_city':all_city,
            'org_num':org_num,
        })
