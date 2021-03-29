from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

# 세션
from django.contrib.auth.decorators import login_required
# DB
from django.db import connection
from django.db.models import Sum,Min,Max,Count,Avg
# 크롤링
from bs4 import BeautifulSoup
from selenium import webdriver

# 그래프
from matplotlib import font_manager, rc 
import matplotlib.pyplot as plt 
import pandas as pd

# 모델 호출 
from .models import GDPTable
from .models import PopulationTable
#
import urllib.request
# 쿼리
import json
import io
# byte배열로 이미지를 변환
import base64
from base64 import b64encode
# 변수 
cursor = connection.cursor()


# Create your views here.

def search_main(request) :
    if request.method == 'GET' :
        data = list(GDPTable.object.all().values("CountryName"))
        request.session['prev'] = request.get_full_path() 
        print(request.session['prev'])
        # print(data)
        # data1= []
        # for tmp in data:
        #     data1.append(tmp["CountryName"])
        # print(data1)
        data1=[]
        for i in range(1960, 2020, 1):
            data1.append(i)
        return render(request, 'main/search_main.html',{'list':data,'year':data1})

# search_country_graph_pop -  나라의 1인당 GDP 구하기
# plot_font - 그래프 폰트함수
def plot_font():
    font_name = font_manager\
        .FontProperties(fname="c:/Windows/Fonts/malgun.ttf") \
        .get_name()
    rc('font',family=font_name)



# @login_required
@csrf_exempt #  뷰어 
# search_detail - 검색하는 창
def search_detail(request) :
    if request.method == 'GET' :
        # 경로 저장용 세션 

        data = list(GDPTable.object.all().values("CountryName"))
        return render(request, 'test/search_detail.html', {'list':data , 'year':range(1960,2020,1), 'how_many':range(1,31,1)})


#@login_required
@csrf_exempt
# search_show - 검색 결과 출력 창 
def search_show(request):
    """
    service/search_show 검색 후 그래프 출력 창
    """
    if request.method == 'GET':
        # session에서 값 받기
        country_name = request.session['country_name']
        tmp_year = request.session['tmp_year']
    
        # 데이터 베이스에서 조건에 맞는 데이터 가져오기
        year = 'gdp_' + str(tmp_year) # 이 때, 모델에 입력한 변수와 대소문자도 동일해야 한다
        one_country = GDPTable.objects.filter(CountryName=country_name).values(year)[0][year]
        avg = GDPTable.objects.aggregate(gdp_avg=Avg(year))
        
        # 그래프 변수 준비
        plot_font()
        y = [float(one_country), float(avg['gdp_avg'])]
        x = [str(tmp_year) + '년' + country_name + '의 GDP' , str(tmp_year) + '년' + "평균 GDP" ]
        

        to_json = dict()
        to_json[country_name+" GDP_in " +str(tmp_year)] = one_country
        to_json["Average GDP_in " +str(tmp_year)] = float(avg['gdp_avg'])
        country_name = country_name.replace(" ","_")
        FILE_NAME = country_name+"_GDP_in_" +str(tmp_year)+".json"
        FILE_PATH = "./static/json/"+FILE_NAME
        html_file_path = "/static/json/"+FILE_NAME
        with open(FILE_PATH, "w") as json_file:
            json.dump(to_json, json_file)
            
        print("helloo")
        try : 
            sql1 = "SELECT * FROM SERVICE_NATIONDATATABLE WHERE COUNTRYNAME = '"+country_name +"'"
            cursor.execute(sql1)
            print("helloo")
            data1 = cursor.fetchall()
            print(type(data1))
            img_data = []
            for i in data1[0] : 
                tmp =str(i).replace(" ","")
                img_data.append(tmp)
            print("**",img_data)
            flag = img_data[-1]
            loc =img_data[-2]
            real_img_data = img_data[1:4]

            if loc =='no_value' or flag =='no_value' : 
                print("tlqkf",loc)
                
                file1 = open('./static/img/no_image.jpg','rb')
                noimg = file1.read()
                img64 = b64encode(noimg).decode("utf-8")
                data4 = "data:;base64,{}".format(img64)
                if loc =='no_value' : 
                    print("no loc")
                    loc = data4
                    
                if flag =='no_value' :
                    print("no flag")
                    flag = data4
                    
        except : 
            real_img_data = ["no_data","no_data","no_data"]
            file1 = open('./static/img/no_image.jpg','rb')
            noimg = file1.read()
            img64 = b64encode(noimg).decode("utf-8")
            data4 = "data:;base64,{}".format(img64)
            loc = data4
            flag = data4

        return render(request, 'test/search_show.html', {'xlist' : x, 'ylist' : y, 'country' : country_name, 'year' : tmp_year, 'file_name' : html_file_path, "img_data" : real_img_data, "flag" : flag, "loc" : loc})
        

    # search_detail.html에서 값을 POST로 먼저 받는다
    elif request.method == 'POST':
        tmp_year = request.POST['year']
        country_name = request.POST['country_name']

        request.session['tmp_year'] = tmp_year
        request.session['country_name'] = country_name
        return redirect('/test/search_show')





# @login_required
@csrf_exempt
def sort_by_year(request):
    """
    service/sort_by_year 
    해당년도 GDP 상위 
    몇개국 나라 검색 후 그래프 출력
    """
    if request.method == 'GET':

        # session에서 값 받기
        tmp_year = request.session['year']
        how_many = int(request.session['how_many'])

        # 데이터 베이스에서 조건에 맞는 데이터 가져오기
        year = 'gdp_' + str(tmp_year)
        print(year)
        # print(GDPTable.object.all().values('CountryName',year))
        # data = GDPTable.object.all().order_by('-'+year).values('CountryName',year)[0:int(how_many)] # [ {} , {} , {} ]
        data = GDPTable.object.all().order_by(year).values('CountryName',year)[0:int(how_many)] # [ {} , {} , {} ]
        # print(data)

        # 그래프 변수 준비
        x = list()
        y = list()
        for i in data:
            # print(data)
            x.append(i['CountryName'])
            if i[year] == '':
                i[year] = float(0)
                y.append(float(i[year]))
            else :  
                y.append(float(i[year]))

        df = pd.DataFrame(y,x )
        print(df) 
        

        # 배포용 제이슨 데이터 가공
        to_json = dict()
        for idx, val in enumerate(data):
            to_json['Rank'+str(idx+1)] = val # { {} , {} , {} }
        
        # 배포용 제이슨 파일 준비
        FILE_NAME = year + '_TOP_' + str(how_many) + '.json'
        FILE_PATH = './static/json/' + FILE_NAME
        html_file_path = '/static/json/' + FILE_NAME
        with open(FILE_PATH, 'w') as json_file:
            json.dump(to_json, json_file)

        
        try : 
            sql1 = "SELECT * FROM SERVICE_NATIONDATATABLE WHERE COUNTRYNAME = '"+CountryName +"'"
            cursor.execute(sql1)
            data1 = cursor.fetchall()
            print(type(data1))
            img_data = []
            for i in data1[0] : 
                tmp =str(i).replace(" ","")
                img_data.append(tmp)
            print("**",img_data)
            flag = img_data[-1]
            loc =img_data[-2]
            real_img_data = img_data[1:4]

            if loc =='no_value' or flag =='no_value' : 
                print("tlqkf",loc)
                
                file1 = open('./static/img/no_image.jpg','rb')
                noimg = file1.read()
                img64 = b64encode(noimg).decode("utf-8")
                data4 = "data:;base64,{}".format(img64)
                if loc =='no_value' : 
                    print("no loc")
                    loc = data4
                    
                if flag =='no_value' :
                    print("no flag")
                    flag = data4
                    
        except : 
            real_img_data = ["no_data","no_data","no_data"]
            file1 = open('./static/img/no_image.jpg','rb')
            noimg = file1.read()
            img64 = b64encode(noimg).decode("utf-8")
            data4 = "data:;base64,{}".format(img64)
            loc = data4
            flag = data4

        return render(request, 'test/sort_by_year.html', {'xlist' : x, 'ylist' : y, "file_name" : html_file_path, 'how_many' : year + ' TOP_' + str(how_many), 'file_name' : html_file_path})
    
    # search_detail.html에서 값을 POST로 먼저 받는다
    elif request.method == 'POST':
        tmp_year = request.POST['year']
        how_many = request.POST['how_many']
        request.session['year'] = tmp_year
        request.session['how_many'] = how_many
        return redirect('/service/sort_by_year')


# @login_required
# search_country - 나라 검색 # 뷰어 
def search_country(request): 
    if request.method == 'GET':
        #request.session['prev'] = request.path     

        data = list(GDPTable.object.all().values("CountryName"))
        return render(request, 'service/search_country.html',{'list':data})

####
#PATH = "/service/search_country_graph?CountryName="
#con = COUNTRYNAME.replace(" ","+")
#real_path = PATH + str(con)


# @login_required
# search_country_graph - 나라 클릭하면 연도 그래프
def search_country_graph(request):

    if request.method == "GET":
        ## HTML에서 값을 받아서 oracle의 CountryName과 같은 이름을 가진 값을 data에 담고 sql문을 돌려 data의 CountryName과 같은 이름을 가진 것을 SELECT *
        CountryName = request.GET["CountryName"] 
        # print(CountryName)
        data = GDPTable.object.get(CountryName=CountryName)   
        sql = "SELECT * FROM SERVICE_GDPTABLE WHERE COUNTRYNAME =%s"
        cursor.execute(sql, [data.CountryName])

        ## Country_gdp_test 를 쓸 수 있는 정보로 가공. y축의 값만 만드는 이유는 x축이 숫자라서 자바스크립트에서 만들기 때문 원래는 x축 y축 다 가공해야 한다
        
        Country_gdp_test = cursor.fetchone()    # fetchall = [(...)], fetchone = (...)
        Country_gdp = list(Country_gdp_test[2:])

        ## 한국의 GDP 정보를 가지고 온다 (비교하기 위해)
        sql = "SELECT * FROM SERVICE_GDPTABLE WHERE COUNTRYNAME = 'Korea, Rep.' "
        cursor.execute(sql)
        korea=cursor.fetchone()
        Korea_gdp = list(korea[2:])

        y_tmp=[]
        for i in range(1960,2020,1):
            y_tmp.append(i)
        y_real=y_tmp[2:]

        try : 
            sql1 = "SELECT * FROM SERVICE_NATIONDATATABLE WHERE COUNTRYNAME = '"+CountryName +"'"
            cursor.execute(sql1)
            data1 = cursor.fetchall()
            print(type(data1))
            img_data = []
            for i in data1[0] : 
                tmp =str(i).replace(" ","")
                img_data.append(tmp)
            print("**",img_data)
            flag = img_data[-1]
            loc =img_data[-2]
            real_img_data = img_data[1:4]

            if loc =='no_value' or flag =='no_value' : 
                print("tlqkf",loc)
                
                file1 = open('./static/files/no_image.jpg','rb')
                noimg = file1.read()
                img64 = b64encode(noimg).decode("utf-8")
                data4 = "data:;base64,{}".format(img64)
                if loc =='no_value' : 
                    print("no loc")
                    loc = data4
                    
                if flag =='no_value' :
                    print("no flag")
                    flag = data4
                    
        except : 
            real_img_data = ["no_data","no_data","no_data"]
            file1 = open('./static/files/no_image.jpg','rb')
            noimg = file1.read()
            img64 = b64encode(noimg).decode("utf-8")
            data4 = "data:;base64,{}".format(img64)
            loc = data4
            flag = data4

        #json만드는 파트 
        dict1=dict()
        for idx, val in enumerate(y_real):
            dict1[Country_gdp[idx]] =val
        cnn = CountryName.replace(" ","_")
        FILE_NAME = cnn + "_yearly_GDP.json"
        FILE_PATH = "./static/files/"+FILE_NAME
        html_file_path = "/static/files/"+FILE_NAME
        with open(FILE_PATH, "w") as json_file:
            json.dump(dict1, json_file)

        return render (request,'service/search_country_graph.html', {'one':data, "Country_gdp":Country_gdp, "korea_gdp":Korea_gdp,
           "file_name":html_file_path,"img_data":real_img_data,"flag":flag,"loc":loc})

def search_country_graph_pop(request):
    if request.method == 'GET':
        ### 나라의 1인당 GDP 구하기

        ## 클릭한 나라의 인구 값 출력
        CountryName = request.GET["CountryName_pop"]                                                  
        data = PopulationTable.objects.get(CountryName=CountryName)                                   

        sql = "SELECT * FROM SERVICE_POPULATIONTABLE WHERE COUNTRYNAME =%s"                   
        cursor.execute(sql, [data.CountryName])
        pop = cursor.fetchone()                                                               
        Country_pop = list(pop)[2:]                                                             
        # print(Country_pop)

        
        ## 클릭한 나라의 GDP 값 출력

        sql = "SELECT * FROM SERVICE_GDPTABLE WHERE COUNTRYNAME =%s"
        cursor.execute(sql, [data.CountryName])
        gdp1 = cursor.fetchone()

        Country_gdp = list(gdp1)[2:]
        #Country_pop = 해당 나라 인구/Country_gdp = 해당 나라 GDP

        ## GDP/인구 값 출력
        capita=[]
        for i in range (0,60,1):    # 0의 값으로 나누면 에러가 나니까 예외처리를 한다
            try:
                avg=Country_gdp[i]/Country_pop[i]
                capita.append(avg)
            except:
                avg1=1
                capita.append(avg1)
        # print(capita) #clear

        ### 한국 1인당 GDP 출력

        ## 한국 인구 출력
        sql = "SELECT * FROM SERVICE_POPULATIONTABLE WHERE COUNTRYNAME = 'Korea, Rep.'"
        cursor.execute(sql)
        korea=cursor.fetchone()
        Korea_pop=list(korea[2:])
        # print(year_korea, Korea_pop) 한국의 연도 = year_korea, 한국의 인구수 = Korea_pop

        ## 한국의 GDP 출력
        sql = "SELECT * FROM SERVICE_GDPTABLE WHERE COUNTRYNAME = 'Korea, Rep.'"
        cursor.execute(sql)
        Korea_gdp_test = cursor.fetchone()  # fetchone()으로 받으면 (...) fetchall()로 받으면 [(...)]형태가 된다
        korea_gdp =list(Korea_gdp_test[2:])

        # 한국 GDP/인구 출력
        kor_capita = []
        for i in range(0,60,1):
            try:
                avg_kor=korea_gdp[i]/Korea_pop[i]
                kor_capita.append(avg_kor)
            except:
                kor_capita.append(1)
        # print(kor_capita, len(kor_capita)) clear kor_capita = 한국 1인당 GDP

        y_tmp=[]
        for i in range(1960,2020,1):
            y_tmp.append(i)
        y_real=y_tmp[2:]

        try : 
            sql1 = "SELECT * FROM SERVICE_NATIONDATATABLE WHERE COUNTRYNAME = '"+CountryName +"'"
            cursor.execute(sql1)
            data1 = cursor.fetchall()
            print(type(data1))
            img_data = []
            for i in data1[0] : 
                tmp =str(i).replace(" ","")
                img_data.append(tmp)
            print("**",img_data)
            flag = img_data[-1]
            loc =img_data[-2]
            real_img_data = img_data[1:4]

            if loc =='no_value' or flag =='no_value' : 
                print("tlqkf",loc)
                
                file1 = open('./static/files/no_image.jpg','rb')
                noimg = file1.read()
                img64 = b64encode(noimg).decode("utf-8")
                data4 = "data:;base64,{}".format(img64)
                if loc =='no_value' : 
                    print("no loc")
                    loc = data4
                    
                if flag =='no_value' :
                    print("no flag")
                    flag = data4
                    
        except : 
            real_img_data = ["no_data","no_data","no_data"]
            file1 = open('./static/files/no_image.jpg','rb')
            noimg = file1.read()
            img64 = b64encode(noimg).decode("utf-8")
            data4 = "data:;base64,{}".format(img64)
            loc = data4
            flag = data4

        #json만드는 파트 
        dict1=dict()
        for idx, val in enumerate(y_real):
            dict1[Country_gdp[idx]] =val
        cnn = CountryName.replace(" ","_")
        FILE_NAME = cnn + "_yearly_GDP.json"
        FILE_PATH = "./static/files/"+FILE_NAME
        html_file_path = "/static/files/"+FILE_NAME
        with open(FILE_PATH, "w") as json_file:
            json.dump(dict1, json_file)

        return render(request,'service/search_country_graph_pop.html',{'one':data,'capita':capita,'kor_capita':kor_capita,
        "file_name":html_file_path,"img_data":real_img_data,"flag":flag,"loc":loc})
        