from django.db import connection

def create_migration(**kwargs):
    pagetyes = [
        'group',
        'normal',
        'product',
        'sale',
        'blog',
        'contact',
    ]
    for i in pagetyes:        
        getdata ="Select * from root_pagetype where page_name='"+i+"'"
        cursor = connection.cursor()
        data = cursor.execute(getdata)
        if data != 1:
            print("\nIt seems First Time. Don't Worry we are adding our customized page types for you")
            trigger_sql = "INSERT INTO root_pagetype (page_name,status) VALUES ('"+i+"','1');"
            cursor.execute(trigger_sql)
            print ('Added =>'+i)

    # home = [
    # 'clients',
    # 'pemplate',
    # ]
    # pos = 0
    # for i in home:        
    #     pos = pos+1
    #     getdata ="Select * from admin_homenavigation where name='"+i+"'"
    #     cursor = connection.cursor()
    #     data = cursor.execute(getdata)
    #     if data != 1:
    #         print("\nWe are adding our customized Home names for you")
    #         trigger_sql = "INSERT INTO admin_homenavigation (name,status,page_type,position,parent_page_id) VALUES ('"+i+"','1','group',"+str(pos)+",'0');"
    #         cursor.execute(trigger_sql)
    #         print ('Added =>'+i)