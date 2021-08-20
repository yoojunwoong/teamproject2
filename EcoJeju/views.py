import json

import numpy
import pandas as pd
import datetime as dt

from django.http import HttpResponse
from django.shortcuts import render

from plotly.offline import plot
import plotly.express as px

from EcoJeju.models import user, worker, wastedata, region, disposedata, workerarea, wasteprediction

from config.settings import DATA_DIRS

map1 = pd.read_csv(DATA_DIRS[0]+'/0816_지역별_요일별.csv', encoding ='cp949')
geo_path2 = DATA_DIRS[0]+'/LSMD_ADM_SECT_UMD_제주.zip.geojson'
geo_data2 = json.load(open(geo_path2, encoding='utf-8'))

fig1 = plot(px.choropleth_mapbox(map1, geojson=geo_data2,
                                 locations='emd_nm',
                                 color='em_kg',
                                 color_continuous_scale="matter",
                                 range_color=(0, 50000),
                                 mapbox_style="carto-positron",
                                 featureidkey="properties.EMD_NM",
                                 zoom=9, center={"lat": 33.39075486566194, "lon": 126.53390204213252},
                                 opacity=0.5,
                                 labels={'emd_nm': 'em_kg'},
                                 animation_frame='week'), output_type='div')

fig2 = plot(px.choropleth_mapbox(map1, geojson=geo_data2,
                                 locations='emd_nm',
                                 color='pay_amt',
                                 color_continuous_scale="matter",
                                 range_color=(10000, 1200000),
                                 mapbox_style="carto-positron",
                                 featureidkey="properties.EMD_NM",
                                 zoom=9, center={"lat": 33.39075486566194, "lon": 126.53390204213252},
                                 opacity=0.5,
                                 labels={'emd_nm': 'pay_amt'},
                                 animation_frame='week'), output_type='div')

allwaste = wastedata.objects.all();

def home(request):
    context={
        'loginok': False,
        'plot_div1': fig1,
        'plot_div2': fig2
    }
    return render(request, 'dashboard.html',context)
def dashboard(request):
    if 'loginok' in request.session:
        context = {
            'loginok': request.session['loginok'],
            'id': request.session['id'],
            'type': request.session['type'],
            'name': request.session['name'],
            'plot_div1': fig1,
            'plot_div2': fig2
        }
    else :
        context={ 'loginok': False }
    return render(request, 'dashboard.html',context)
def userboard(request):
    if 'loginok' in request.session:
        context = {
            'loginok': request.session['loginok'],
            'id': request.session['id'],
            'type': request.session['type'],
            'name': request.session['name'],
        }
    else :
        context={
            'loginok': False
        }
    return render(request,'userboard.html',context)

def workerboard(request):
    if 'loginok' in request.session:
        context = {
            'loginok': request.session['loginok'],
            'id': request.session['id'],
            'type': request.session['type'],
            'name': request.session['name'],
        }
    else :
        context={ 'loginok': False,
                  }
    return render(request,'workerboard.html',context)


def login(request):
    return render(request, 'login.html')
def loginimpl(request):
    id = request.POST['loginid'];
    pwd = request.POST['loginpwd']
    typecheck = request.POST['logintype'];
    next = 'login.html'
    context={}
    if id == '' or pwd == '':
        context = {
                'result': '빈칸을 모두 채워주세요',
                   }
    elif(typecheck =='envir'):
        if worker.objects.filter(worker_id =id).exists():
            getworker = worker.objects.get(worker_id=id);
            if getworker.worker_pwd == pwd:
                context={
                    'loginok':True,
                    'id': id,
                    'type': 00,
                    'name': getworker.worker_name
                }
                request.session['loginok']= True;
                request.session['id'] = id;
                request.session['name'] = getworker.worker_name;
                request.session['type'] = 10;
                next = 'dashboard.html'
            else:
                context = {
                    "result": "비밀번호가 틀렸습니다",
                }
        else:
            context={
                "result": "존재하지 않는 아이디 입니다.",
            }
    elif typecheck =='normal':
        if user.objects.filter(user_id =id).exists():
            getuser = user.objects.get(user_id=id);
            if getuser.user_pwd == pwd:
                context={
                    'loginok':True,
                    'id': id,
                    'type': 10,
                    'name': getuser.user_name
                }
                request.session['loginok']= True;
                request.session['id'] = id;
                request.session['name'] = getuser.user_name;
                request.session['type'] = 10;
                next = 'dashboard.html'
            else:
                context = {
                    "result": "비밀번호가 틀렸습니다"
                }
        else:
            context = {
                "result": "존재하지 않는 아이디 입니다.",
            }
    else :
        context={
            "result": "로그인 실패",
        }
    return render(request,next,context)
def register(request):
    return render(request,'register.html')
def registerimpl(request):
    typecheck = request.POST['inputtype'];
    id = request.POST['inputid'];
    pwd = request.POST['inputpwd'];
    repwd = request.POST['inputrepwd'];
    name = request.POST['inputname'];

    if id=='' or pwd=='' or repwd==''or name =='':
        context = {'result': '빈칸을 모두 채워주세요'}
    elif user.objects.filter(user_id =id).exists() or worker.objects.filter(worker_id =id).exists() :
        context = {'result': '이미 존재하는 아이디 입니다.'}
    elif pwd != repwd:
        context = {'result': '비밀번호가 일치하지 않습니다.'}
    else:
        context = {'result': '회원가입을 성공하였습니다.'}
        if typecheck == 'envir':
            worker.objects.create(
                worker_id =id,
                worker_name =name,
                worker_pwd =pwd
            ).save()
        else:
            user.objects.create(
                user_id= id,
                user_name= name,
                user_pwd= pwd
            ).save()
    return HttpResponse(json.dumps(context), content_type="application/json")

def recover(request):
    return render(request,'recover.html')

def card1(request):
    todaystr ='2021-06-30'
    today = dt.datetime.strptime(todaystr, '%Y-%m-%d')
    week_ago = today - dt.timedelta(days=6)
    data = pd.DataFrame(allwaste.filter(base_date__gte= week_ago).values_list('base_date','em_g'));
    grouped = data[1].groupby([data[0]]).sum().reset_index()
    result=''
    for d in grouped[1]:
        result = result + ',' + str(int(d/1000))
    result = result[1:]
    print(result);
    context = {
        'data' : result,
        'today': todaystr,
        'today_g': float(grouped[1][grouped.shape[0]-1]/1000)
    }
    return HttpResponse(json.dumps(context), content_type='application/json');
def card2(request):
    todaystr ='2021-06-30'
    today = dt.datetime.strptime(todaystr, '%Y-%m-%d')
    week_ago = today - dt.timedelta(days=6)
    data = pd.DataFrame(allwaste.filter(base_date__gte= week_ago).values_list('base_date','pay_amt'));
    grouped = data[1].groupby([data[0]]).sum().reset_index()
    result=''
    for d in grouped[1]:
        result = result + ',' + str(int(d/10000))
    result = result[1:]
    print();
    context = {
       'data' : result,
        'today': todaystr,
        'today_amt': float(grouped[1][grouped.shape[0]-1]/10000)
    }
    return HttpResponse(json.dumps(context), content_type='application/json');
def plot1(request):
    datas = pd.DataFrame(allwaste.filter(base_date__year=2021).values_list('base_date','pay_amt'));
    datas['Month'] = datas[0].dt.month
    grouped = datas[1].groupby([datas['Month']])
    mon = pd.DataFrame(grouped.sum()).reset_index()
    result = []
    for i in range(len(mon['Month'])):
        result.append([str(mon['Month'][i]) + '월', float(mon[1][i]/10000)])
    context = {
        "label": "사용금액(만원)",
        "color": "#1f92fe",
        "data" : result
    }
    return HttpResponse(json.dumps(context), content_type='application/json');
def plot3(request):
    datas = pd.DataFrame(allwaste.filter(base_date__year=2021).values_list('base_date','em_g'));
    datas['Month'] = datas[0].dt.month
    grouped = datas[1].groupby([datas['Month']])
    mon = pd.DataFrame(grouped.sum()).reset_index()
    result = []
    for i in range(len(mon['Month'])):
        result.append([str(mon['Month'][i]) + '월', float(mon[1][i] / 1000)])
    context = {
        "label": "배출량(kg)",
        "color": "#1ba3cd",
        "data" : result
    }
    return HttpResponse(json.dumps(context), content_type='application/json');
def usergimpl(request):
    id = 'test01'
    todaystr ='2021-06-30'
    today = dt.datetime.strptime(todaystr, '%Y-%m-%d')
    month_ago = today - dt.timedelta(days=29)
    # disposedata = pd.read_csv(DATA_DIRS[0]+'/regiontabledata.csv', encoding ='cp949')
    datas = pd.DataFrame(disposedata.objects.filter(dispose_user_id=id, dispose_date__gte=month_ago).values('dispose_amount','dispose_weight', 'dispose_date'))
    todayg = int(datas[datas['dispose_date'] == today]['dispose_weight'][0])
    todayamt = int(datas[datas['dispose_date'] == today]['dispose_amount'][0])

    datas['Day'] = datas['dispose_date'].dt.day
    datas.sort_values(by=['Day'], axis=0, inplace=True)
    print(datas);
    first = 7 - int(datas['dispose_date'][0].isoweekday())
    week = [0, 0, 0, 0, 0, 0]
    aweek = [0, 0, 0, 0, 0, 0]
    for i in range(len(datas['Day'])):
        if datas['Day'][i] < first + 1:
            week[0] = week[0] + datas['dispose_weight'][i]
            aweek[0] = aweek[0] + datas['dispose_amount'][i]
        elif datas['Day'][i] < first + 8:
            week[1] = week[1] + datas['dispose_weight'][i]
            aweek[1] = aweek[1] + datas['dispose_amount'][i]
        elif datas['Day'][i] < first + 15:
            week[2] = week[2] + datas['dispose_weight'][i]
            aweek[2] = aweek[2] + datas['dispose_amount'][i]
        elif datas['Day'][i] < first + 22:
            week[3] = week[3] + datas['dispose_weight'][i]
            aweek[3] = aweek[3] + datas['dispose_amount'][i]
        elif datas['Day'][i] < first + 29:
            week[4] = week[4] + datas['dispose_weight'][i]
            aweek[4] = aweek[4] + datas['dispose_amount'][i]
        else:
            week[5] = week[5] + datas['dispose_weight'][i]
            aweek[5] = aweek[5] + datas['dispose_amount'][i]
    print(aweek)
    result = ''
    for d in week:
        if d == 0:
            continue;
        result = result + ',' + str(int(d))
    result = result[1:]
    total_g = int(sum(week)/1000)

    aresult=''
    for a in aweek:
        if a==0:
            continue
        aresult= aresult+','+str(a)
    aresult=aresult[1:]
    total_amt = int(sum(aweek))
    print(aresult)
    context = {
        'gvalues': result,
        'amtvalues':aresult,
        'totalg':total_g,
        'totalamt': total_amt,
        'todayg': todayg,
        'todayamt':todayamt,
        'todaystr':todaystr
    }
    return HttpResponse(json.dumps(context), content_type='application/json');
def bars3(request):
    id='test01'
    data2 = pd.DataFrame(disposedata.objects.filter(dispose_user_id = id).values('dispose_date','dispose_weight'))

    data2['dispose_date'] = pd.to_datetime(data2['dispose_date'])
    data2['dispose_year'] = data2['dispose_date'].dt.year
    data2['dispose_month'] = data2['dispose_date'].dt.month

    data2_1 = data2[data2['dispose_month'] == 1]
    data2_2 = data2[data2['dispose_month'] == 2]
    data2_3 = data2[data2['dispose_month'] == 3]
    data2_4 = data2[data2['dispose_month'] == 4]
    data2_5 = data2[data2['dispose_month'] == 5]
    data2_6 = data2[data2['dispose_month'] == 6]

    test2_1 = data2_1['dispose_weight'].sum()
    test2_2 = data2_2['dispose_weight'].sum()
    test2_3 = data2_3['dispose_weight'].sum()
    test2_4 = data2_4['dispose_weight'].sum()
    test2_5 = data2_5['dispose_weight'].sum()
    test2_6 = data2_6['dispose_weight'].sum()

    context = [{
        "label": "나의 한달 배출량",
        "color": "#FF3700",
        "data": [["1월", int(test2_1)], ["2월", int(test2_2)], ["3월", int(test2_3)],
                 ["4월", int(test2_4)], ["5월", int(test2_5)], ["6월", int(test2_6)]]
    }, {
        "label": "월별 가구당 배출 평균량",
        "color": "#57E9E1",
        "data": [['1월', 12417], ['2월', 12810], ['3월', 13518],
                 ['4월', 11979], ['5월', 13212], ['6월', 12027]]
    }]
    return HttpResponse(json.dumps(context), content_type='application/json');

    ##------------준웅님그래프---------------------------
def bars4(request):
    id='test01'
    data2 = pd.DataFrame(disposedata.objects.filter(dispose_user_id = id).values('dispose_date','dispose_amount'))
    data2['dispose_date'] = pd.to_datetime(data2['dispose_date'])
    data2['dispose_year'] = data2['dispose_date'].dt.year
    data2['dispose_month'] = data2['dispose_date'].dt.month

    data2_1 = data2[data2['dispose_month'] == 1]
    data2_2 = data2[data2['dispose_month'] == 2]
    data2_3 = data2[data2['dispose_month'] == 3]
    data2_4 = data2[data2['dispose_month'] == 4]
    data2_5 = data2[data2['dispose_month'] == 5]
    data2_6 = data2[data2['dispose_month'] == 6]

    test2_1 = data2_1['dispose_amount'].sum()
    test2_2 = data2_2['dispose_amount'].sum()
    test2_3 = data2_3['dispose_amount'].sum()
    test2_4 = data2_4['dispose_amount'].sum()
    test2_5 = data2_5['dispose_amount'].sum()
    test2_6 = data2_6['dispose_amount'].sum()

    context = [{
        "label": "월별 가구당 사용 금액 평균량",
        "color": "#5ab1ef",
        "data": [['1월', 369], ['2월', 381], ['3월', 372],
                 ['4월', 357], ['5월', 393], ['6월', 354]]
    }, {
        "label": "나의 한달 금액",
        "color": "#FF007B",
        "data": [["1월", int(test2_1)], ["2월", int(test2_2)], ["3월", int(test2_3)],
                 ["4월", int(test2_4)], ["5월", int(test2_5)], ["6월", int(test2_6)]]
    }]
    return HttpResponse(json.dumps(context), content_type='application/json');


def piecharts(request):
    id='worker'
    worklist = pd.DataFrame(workerarea.objects.filter(worker_id=id).values())
    areas=[];
    for area in worklist['area_cd']:
        cur = region.objects.get(region_id=area)
        areas.append({'area':area,'region':cur.region_name,'parent':cur.parent_name, 'city':cur.city_name})

    todaystr = '2021-06-30'
    today = dt.datetime.strptime(todaystr, '%Y-%m-%d')

    for area in areas:
        df =pd.DataFrame(wastedata.objects.filter(base_date = today, area_cd=area['area']).values())
        if df.empty :
            area['percent'] = 0
        else :
            val = numpy.around(df['em_g'][0] / 3000)
            area['percent'] = int(val)
    context={
        'areas': areas,
        'today': todaystr,
    }
    return HttpResponse(json.dumps(context), content_type='application/json');
def tables(request):
    id='worker'
    worklist = pd.DataFrame(workerarea.objects.filter(worker_id=id).values('area_cd'))

    checkp=[];
    for area in worklist['area_cd']:
        cur = region.objects.get(region_id=area)
        parent = cur.parent_name
        if parent not in checkp:
            checkp.append(parent);

    list = [];
    for p in checkp:
        jq = wasteprediction.objects.get(region=p)
        list.append({'region': jq.region, 'seven': int(jq.onemonth), 'eight': int(jq.tw0month)})

    context={
        'list': list
    }
    return HttpResponse(json.dumps(context), content_type='application/json');


# db에 데이터 넣기 위한 함수
def insertdata(request):
    #음식물 지역별 데이터 넣기
    # df = pd.read_csv(DATA_DIRS[0] + '\\foodwastedata.csv', encoding='cp949')
    # data21 = df[df['base_date'].str.split('-').str[0] == '2021']
    # for index in data21.index:
    #     base_date = dt.datetime.strptime(df.loc[index]['base_date'], '%Y-%m-%d')
    #     city = df.loc[index]['city']
    #     emd_nm = df.loc[index]['emd_nm']
    #     area_cd = df.loc[index]['em_area_cd']
    #     em_cnt = df.loc[index]['em_cnt']
    #     em_g = df.loc[index]['em_g']
    #     pay_amt = df.loc[index]['pay_amt']
    #     wastedata.objects.create(
    #         base_date =base_date,
    #         city = city,
    #         emd_nm =emd_nm,
    #         area_cd =area_cd,
    #         em_cnt =em_cnt,
    #         em_g =em_g,
    #         pay_amt =pay_amt
    #     ).save()
    # 지역 코드 데이터 넣기
    # datas = pd.read_csv(DATA_DIRS[0] + '\\regiontabledata.csv', encoding='cp949')
    # for index in datas.index:
    #     region_id =datas.loc[index]['region_id']
    #     region_name = datas.loc[index]['region_name']
    #     parent_name = datas.loc[index]['parent_name']
    #     city_name = datas.loc[index]['city_name']
    #     region.objects.create(
    #         region_id =region_id,
    #         region_name=region_name,
    #         parent_name = parent_name,
    #         city_name = city_name
    #     ).save()

    # # 사용자 이용 데이터 넣기
    # datas = pd.read_csv(DATA_DIRS[0] + '\\disposedata.csv', encoding='cp949')
    # print(datas);
    # for index in range(datas.shape[0]):
    #     dispose_date = dt.datetime.strptime(datas.loc[index]['dispose_date'], '%Y-%m-%d'),
    #     dispose_weight = datas.loc[index]['dispose_weight'],
    #     dispose_amount=datas.loc[index]['dispose_amount'],
    #     dispose_region_code=datas.loc[index]['dispose_city_code'],
    #     user_id = datas.loc[index]['dispose_id']
    #     print(dispose_date[0],dispose_weight[0],dispose_amount[0],dispose_region_code[0],user_id)
    #     disposedata.objects.create(
    #         dispose_date=dispose_date[0],
    #         dispose_weight=dispose_weight[0],
    #         dispose_amount= dispose_amount[0],
    #         dispose_region_code=dispose_region_code[0],
    #         dispose_user_id= user_id
    #     ).save()
    datas = pd.read_csv(DATA_DIRS[0] + '\\78월시계열예측kg.csv', encoding='cp949')
    for index in range(datas.shape[0]):
        region=datas['emd_nm'][index]
        predic_weight7 =datas['em_kg_pred7'][index]
        predic_weight8=datas['em_kg_pred8'][index]
        print(region,predic_weight7,predic_weight8)
        wasteprediction.objects.create(
            region=region,
            onemonth = predic_weight7,
            tw0month = predic_weight8,
        ).save()

    context={'result': 'success'}
    return render(request,'insertdata.html',context)

def into(request):
    return render(request,'insertdata.html')


if __name__ == '__main__' :
    card1();