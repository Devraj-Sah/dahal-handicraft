from django.template.defaulttags import register
from root.models import *
from account.models import CustomUser
from django.db.models import Q

@register.filter
def get_NepaliDate(date):
    try:
        import datetime
        import nepali_datetime
        dt = datetime.date(date.year,date.month,date.day)
        nepali_date = nepali_datetime.date.from_datetime_date(dt)
        return nepali_date
        # return nepali_date.strftime('%K-%n-%D (%k %N %G)')   
    except:
        return date
        
@register.filter
def times(count, start):
    if start > 3 :
        return range(start-2,count)
    return range(1,count)

# @register.filter
# def str(str):
#     if len(str) > 50:
#         to_str = '%.50s' % str
#         data = to_str + ' ...'
#         return data
#     return str

@register.filter
def str_rm(string,num=50):
    if len(string) > num:
        total_str = '%.'+str(num)+'s'
        to_str =  total_str % string
        data = to_str + ' ...'
        return data
    return string

@register.filter()
def to_int(value):
    return int(value)