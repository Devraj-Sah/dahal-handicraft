import json
import time
from ..models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse



def RecursionChild(parentobj,nodes):
    for child in parentobj:
        # print(child.id)
        data = [child.id,child.parent.id,1,child.name,False]
        nodes.append(data)
        if child.childs.all().count()>0:
            RecursionChild(child.childs.all(),nodes)        
    

@csrf_exempt
def TreeAjax(request):
    nodes = []
    root_obj = Navigation.objects.filter(parent_id= None)
    for root in root_obj:
        children = root.childs.all()
        RecursionChild(children,nodes)

        # while children.count()>0:

            # for chil in children:
            #     print(chil)
            #     data = [chil.id,chil.parent.id,1,chil.name,False]
            #     nodes.append(data)
            
        # if root.childs.count()>0:
        #     for chil in root.childs.all():
        #         # print(chil)
        #         data = [chil.id,chil.parent.id,1,chil.name,False]
        #         nodes.append(data)
        data = [root.id,-1,0,root.name,False]
        nodes.append(data)
       
#old
# @csrf_exempt
# def TreeAjax(request):
#     nodes = [  # [id,parent,type,name, checked]
#         [0, -1, 0, 'Root1', False],
#         [1, 0, 2, 'Knot1', False],
#         [2, 0, 2, 'Knot2', False],
#         [3, 1, 3, 'Leaf1', False],
#         [4, 2, 3, 'Leaf2', False],
#         [5, 0, 2, 'Knot3', False],
#         [6, 5, 3, 'Leaf2', False],
#         [7, -1, 0, 'Root2', True],
#         [8, 7, 2, 'Knot4', True],
#     ]

    rq = {
        "cmd": request.GET["cmd"],
        "id": request.GET["id"],
        "idt": request.GET["idt"],
        "ckd": request.GET["ckd"],
        "cmt": request.GET["cmt"],
        "tid": request.GET["tid"],
        "tzo": request.GET["tzo"],
        "ver": request.GET["ver"],
        'pfx' : '',
    }
    if 'pfx' in request.GET.items():
        rq['pfx'] = request.GET['pfx']

    rq["fid"] = rq["id"].replace(rq["pfx"], "")
    rsp = {"status": True, "prompt": ""}
    if rq["cmd"] == "opn":
        rsp["factor"] = Children(nodes, rq)
        print(rsp)
    elif rq["cmd"] == "sch":
        rsp["factor"] = Search(nodes, rq)
    elif rq["cmd"] == "new" or rq["cmd"] == "add":
        rsp["factor"] = {"id": rq["pfx"] + str(time.time())}
    elif rq["cmd"] == "cpy" or rq["cmd"] == "mve":
        rsp["factor"] = {}  # return old_id => new_id
        for id in rq["id"]:
            if rq["cmd"] == "cpy":
                rsp["factor"][id] = rq["pfx"] + str(time.time())
            else:
                rsp["factor"][id] = rq["id"][0]
    else:
        # dummy response
        pass
    return JsonResponse(rsp)


def Children(nodes, rq):
    rlt = []
    for i in range(len(nodes)):
        if nodes[i][1] == int(rq["fid"]):
            for node in nodes:
                if node[1] == nodes[i][0]:
                    if nodes[i][2] != 0:
                        nodes[i][2] = 1
            sta = {"opened": False, "checked": (("ckd" in rq) and nodes[i][4])}
            chd = nodes[i][2] < 2
            r = {"id": rq["pfx"] + str(nodes[i][0]), "text": nodes[i][3], "state": sta, "children": chd, "type": nodes[i][2]}
            rlt.append(r)

    # return HttpResponse('rlt')
    return rlt
    
def Search(nodes, rq):
    nds = {}
    Find(nodes, nds, rq["fid"], -1, rq["fnd"])
    rlt = []
    a = list(nds.keys())
    for id in nds:
        if not nds[id][0]:
            for i in range(len(a)):
                if nds[a[i]][1] == id and nds[a[i]][0]:
                    nds[id][0] = True
        if nds[id][0]:
            rlt.append(rq["pfx"] + id)
    return rlt


def Find(nodes, rlt, id, pnt, cnd):
    for node in nodes:
        if node[1] == id and len(rlt[id]) == 0:
            fnd = node[3].find(cnd["str"])  # VR Jun 2022
            rlt[id] = [fnd != -1, pnt]
            Find(nodes, rlt, node[0], node[1], cnd)