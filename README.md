## 1. 빅콘테스트 퓨처스리그 데이터분석 프로젝트🍊

- 팀명 : 재주도좋다

- 팀장 : 주현정

- 팀원 : 송재현, 안유진, 유준웅



## **2. 프로젝트 설명📌**

### 1. 프로젝트 주제💡

#### **제주도 음식물 쓰레기양 예측을 통한 배출량 감소 방안 도출**

- 음식물 쓰레기 데이터를 활용한 배출량을 지역별, 연령별 등으로 시각화하여 음식물 배출 관련 정보 열람 브라우저 개설
- 예측 모델 개발을 통하여 제주 읍면동별 배출량을 예측하고, 음식물 쓰레기 배출 요인에 따른 배출량 감소 방안 도출



### 2. 프로젝트 환경 및 사용 tool🛠

|    전처리     |                시각화                |       데이터 분석 및 머신러닝       |   배포   |
| :-----------: | :----------------------------------: | :---------------------------------: | :------: |
| Pandas, numpy | Matplotlib, Seaborn, Plotly, Tableau | Sklearn, ARIMA, ETS, forecastHybrid | AWS 예정 |

| DB구축  |    Web Server    |             개발 도구              |          협업 도구           |
| :-----: | :--------------: | :--------------------------------: | :--------------------------: |
| MariaDB | Django ver 3.2.4 | jupyter notebook & Colab & pycharm | Zoom & Google Drive & Github |



### 3. 가이드📲

`pycharm-community`와 `python` 버전 3.6이상이 설치된 로컬에서 위 GitHub코드를 수동으로 다운받아 사용합니다. 또는 cmd창에서 해당 repository를 git clone하여 local에서 바로 사용할 수 있습니다 . AWS을 통하여 웹페이지를 배포할 예정입니다.

[링크준비중]



## 3. project process📑

### 1. 주제 선정

연간 음식물 쓰레기 배출에 대한 환경 오염 문제는 심각해지고 있습니다. 특히, 제주도에서 클린하우스 제도를 해결방안으로 도입한 이후에도 음식물 쓰레기 배출량은 현저히 증가하는 추세입니다. 빅콘테스트 경진대회 주최측으로부터 제주테크노파크에서 제공받은 4개년 음식물 쓰레기 배출량 관련 데이터 셋을 이용하여 현상에 요인 분석과 제주도민을 위한 배출량 열람 페이지를 개발하고자 합니다.



### 2. Process

1. 8월 6일 ~ 8일 : 데이터 수집 및 필요한 파일 다운로드

 - 데이터 수집 기간 : 2018년 1월 1일 ~ 2021년 6월 30일
   제공 : 빅콘테스트 경진대회 주최측, 제주테크노파크
   데이터 다운로드 : https://www.bigcontest.or.kr/index.php 회원가입 후 진행. 대회 참가자만 다운로드 가능하며 파일 원본의 상업적 목적의 배포를 금합니다.
 - 지도시각화를 위한 제주도 읍면동 행정코드
   다운로드 : [국가공간정보포털 접속](http://data.nsdi.go.kr/dataset/15145) -> LSMD_ADM_SECT_UMD_제주.zip (2021-08-17 업데이트)

|     빅콘테스트 제공      |
| :----------------------: |
|       음식물쓰레기       |
|      내국인유동인구      |
| 장기체류 외국인 유동인구 |
| 단기체류 외국인 유동인구 |
|         거주인구         |
|    음식관련 카드소비     |



2. 8월 9일 ~ 10일 : 음식물쓰레기 FOOD_WASTE 외 datasets 전처리 및 가공

   1. 기본 결측치 전처리
      
      [01 &#95;음식물쓰레기 &#95;기본전처리.ipynb](https://github.com/Songgplant/KDT-Semi_Project02/blob/master/Jypyternotebook/01_%EC%9D%8C%EC%8B%9D%EB%AC%BC%EC%93%B0%EB%A0%88%EA%B8%B0_%EA%B8%B0%EB%B3%B8%EC%A0%84%EC%B2%98%EB%A6%AC.ipynb)
      음식물 배출량, 배출 건수, 배출 건수에 대한 금액 결측치 처리
      지역별, 배출지역코드 결측치 처리
      
   2. 분석 목적에 따른 데이터셋 가공

      - 가공 분류 대상
        - 날짜별 총 음식물쓰레기 배출량

        - 지역별 총 배출량 및 지불금액
        - 요일,주간,월간,년간 단위 데이터셋 분할

      - [전체월간배출량.ipynb](https://github.com/Songgplant/KDT-Semi_Project02/blob/master/Jypyternotebook/%EC%A0%84%EC%B2%B4%EC%9B%94%EA%B0%84%EB%B0%B0%EC%B6%9C%EB%9F%89.ipynb)
        object 타입으로 저장된 날짜값을 형식에 맞게 '-'로 분할하여 저장

      ```python
      df['base_date'] = df['base_date'].astype('str')
      datas = df['base_date'].str.split('-')
      df['year'] = datas.str.get(0)
      df['month'] = datas.str.get(1)
      ```

      - [월별지역별총배출량&#95;dataset생성.ipynb](https://github.com/Songgplant/KDT-Semi_Project02/blob/master/Jypyternotebook/%EC%9B%94%EB%B3%84%EC%A7%80%EC%97%AD%EB%B3%84%EC%B4%9D%EB%B0%B0%EC%B6%9C%EB%9F%89_dataset%EC%83%9D%EC%84%B1.ipynb)
        날짜값을 다른 방법으로 변환 : datetime함수 이용

      ```python
      df['base_date'] = pd.to_datetime(df['base_date'])
      df['year_date'] = df['base_date'].dt.year
      df['month_date'] = df['base_date'].dt.month
      ```

      ​		목적에 맞게 column 선택 후 원하는 통계값 계산

      ```python
      jejudf = df.loc[:, ['year_date', 'month_date', 'emd_nm', 'em_g']]
      gd = jejudf.groupby(['year_date', 'month_date', 'emd_nm']).sum()
      gd
      ```

      - [0816&#95;지역별&#95;pay&#95;amt.ipynb](https://github.com/Songgplant/KDT-Semi_Project02/blob/master/Jypyternotebook/0816_%EC%A7%80%EC%97%AD%EB%B3%84_pay_amt.ipynb)
        dataframe 그룹집계함수 사용 후 새로운 dataframe 형태로 저장할 때는 index를 다시 지정해야 함

      ```python
      grouped = data['pay_amt'].groupby([data['year_date'],data['month_date'],data['emd_nm']])
      grouped.sum()
      region_pay = pd.DataFrame(grouped.sum()).reset_index()
      ```

      - [0816_요일별 데이터분할.ipynb](https://github.com/Songgplant/KDT-Semi_Project02/blob/master/Jypyternotebook/0816_%EC%9A%94%EC%9D%BC%EB%B3%84%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B6%84%ED%95%A0.ipynb)
        datetime의 기능 : day_name()으로 요일 추출 가능

        ```python
        df0 = df[(df['year_date']==2021) & (df['month_date']==6)]
        df0['week'] = df0['date'].dt.day_name()
        ```

      

3. 8월 11일 ~ 12일 :

   1. ERD 설계 및 웹페이지 환경 세팅
      - Django와 **static html**기반 웹페이지 기본요소 구축

      - 서버 Database 구축을 위한 ERD 설계

        : **ERD Cloud를 이용하여 ERD 구성도 작성**

        ![trickERD](https://github.com/Songgplant/KDT-Semi_Project02/blob/master/md_images/trickERD.png)

      - django의 models.py를 이용하여 **MariaDB**와 연동 및 테이블 생성
        : 대표 Entity = user

        ```python
        class user(models.Model): # 생성하고자 하는 테이블 이름을 클래스name으로 지정
            # 테이블 속성값 설계 코드
            # column_name = models.CharField(max_length=값의 길이, unique=중복값X, verbose_name="시스템에 연동될 이름", primary_key=기본키지정)
            user_id = models.CharField(max_length=20, unique=True, verbose_name="유저 아이디", primary_key=True)
            user_pwd = models.CharField(max_length=20, verbose_name='유저 비밀번호')
            user_name = models.CharField(max_length=20, verbose_name= '유저 이름')
            register_date = models.DateTimeField(auto_now_add=True, verbose_name="계정생성시간")
        
            def __str__(self):
                return self. user_name;
            class Meta:
                db_table = 'user'
                verbose_name ='개인 사용자'
                verbose_name_plural='개인 사용자'
        ```

      - 설계 후 최종 생성한 Entity 목록 (Table 목록)
      
        ![tricktablecmd](https://github.com/Songgplant/KDT-Semi_Project02/blob/master/md_images/tricktablecmd.png)
      
      - 사용자 로그인/회원가입 기능 생성 및 사용자 DB연동
        DB연동 방식 : Entity 생성 코드 입력 후 Terminal에서 실행

        ```
        python manage.py makemigrations, python manage.py migrate
        ```
      
        연동 된 DB를 이용하여 로그인/회원가입과 연동
      
      - 메인페이지 음식물 쓰레기 정보 DB 설계, 구축 및 연동
        models.py 에서 MySQL Entity 설계
      
        ```python
        class wastedata(models.Model):
            data_id = models.AutoField(primary_key=True)
            base_date = models.DateTimeField();
            city = models.CharField(max_length=10, verbose_name='city')
            emd_nm = models.CharField(max_length=10, verbose_name='town name')
            area_cd = models.CharField(max_length=20, verbose_name='area code')
            em_cnt = models.IntegerField( verbose_name='cnt');
            em_g = models.IntegerField(verbose_name = 'g');
            pay_amt = models.IntegerField(verbose_name='pay amount');
        
            def __str__(self):
                return self.area_cd;
        
            class Meta:
                db_table = 'wastedata'
                verbose_name ='food waste data'
                verbose_name_plural='food waste data'
        ```
      
        views.py로 연결 : 설계한 모든 Entity를 import
      
        ```python
        from EcoJeju.models import user, worker, wastedata, region, disposedata, workerarea, wasteprediction
        allwaste = wastedata.objects.all();
        ```

        
      
   2. 공통 컬럼으로 데이터 셋 병합 및 상관관계 분석
      - `emd_cd`, `emd_nm` 기준으로 통합
        [0812&#95;데이터셋 통합&#95;상관관계분석.ipynb](https://github.com/Songgplant/KDT-Semi_Project02/blob/master/Jypyternotebook/0812_%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%85%8B%20%ED%86%B5%ED%95%A9_%EC%83%81%EA%B4%80%EA%B4%80%EA%B3%84%EB%B6%84%EC%84%9D.ipynb)
        날짜, 읍면동코드를 기준으로 `outer join` 방식을 통해 데이터 병합
        : 거주인구는 월단위로 측정 -> 일단위로 변동된 값이 아니므로 년/월/지역에 일치하는 값에 모두 들어가는 outer join을 사용함

        ```python
        final = pd.merge(data1, data3_2, left_on=['year_date','month_date','emd_cd'], right_on=['year_date','month_date','emd_cd'], how='outer')
        ```

        

   3. 2021년 7, 8월 지역별 음식물 배출량 예측 모델 개발

      - 배출량(em_g) 예측을 위한 시계열 모델 : **ARIMA, ETS, forecasthybrid**

        [0813&#95;최종&#95;시계열분석.ipynb](https://github.com/Songgplant/KDT-Semi_Project02/blob/master/Jypyternotebook/0813_최종_시계열분석.ipynb)
        예측 모델 평가 척도 MAE 라이브러리 import방식 말고 함수로 계산식 생성

        ```python
        def mae(df) :
          n = len(df['emd_nm'])
          df['dif'] = np.abs(df['em_g'] - df['em_g_pred'])
          result = sum(df['dif']) / n
          return result
        ```

        파이썬에서 R 패키지를 불러와 작동하는 `rpy2` 사용

        ```python
        import rpy2.robjects as robjects
        from rpy2.robjects import pandas2ri
        
        pandas2ri.activate()
        # 예시 알고리즘 : ARIMA 자기회귀누적이동평균모델
        auto_arima = """ # R 코드 실행 line
            function(ts){
                library(stats)
                library(forecast)
                d_params = ndiffs(ts)
                model = auto.arima(ts, max.p=2, d=d_params)
                forecasted_data = forecast(model, h=2)
                out_df = data.frame(forecasted_data$mean)
                colnames(out_df) = c('amount')
                out_df
            }
        """
        ```

        

4. 8월 13일 ~15일 :

   1. 제주도 지도 시각화

      - plotly 라이브러리 활용
        [plotly지도시각화.ipynb](https://github.com/Songgplant/KDT-Semi_Project02/blob/master/Jypyternotebook/plotly지도시각화.ipynb)
        지도시각화를 위해 앞서 다운로드한 geojson 파일을 json.load로 진행. 세부 코드는 링크 참조

        ```python
        geo_path2 = '/content/drive/MyDrive/세미2차/LSMD_ADM_SECT_UMD_제주.zip.geojson'
        geo_data2 = json.load(open(geo_path2, encoding='utf-8'))
        geo_data2
        ```

   2. Front-end 화면 구성 및 설계 및 div 기준으로 html setting
      - 사용자/관리자/공용 UI/UX 구성
        Directory `templates` : 
        dashboard.html, insertdata.html, login.html, recover.html, register.html, userboard.html, workerboard.html

   

5. 8월 16일 ~ 17일 :

   1. 추가적인 DB 구축 및 시스템 구성 정리
      
      - 알고리즘기반 예측 데이터DB 추가 구축 및 전체 DB 연동
      
   2. 가공한 database, datasets를 기반으로 분석 결과 시각화
      : `공용 페이지` `사용자 페이지` `관리자 페이지` setting

      - static -> app.js 파일 내 그래프(init+'그래프명') 기본 함수 세팅
        -> javascript, ajax 위주로 그래프별 내장 function 생성 후 data를 연결. 차트 기본요소는 js와 css로 생성 후 브라우저 구성 html div class name으로 연결

        ```js
        function () {
          'use strict';
          $(initFlotSpline);
          function initFlotSpline() {
            function data3(){
                var result;
                $.ajax({
                    url:'plot3',
                    async: false,
                    datatype:'JSON',
                    success:function(data){
                        result = data;
                    }
                });
                return result;
            };
            var datav3 = [data3()];
              
        // data 지정 후 차트에 값 할당
        var chart = $('.chart-spline');
        if (chart.length) $.plot(chart, data, options);
        var chartv3 = $('.chart-splinev3');
        if (chartv3.length) $.plot(chartv3, datav3, options);
        ```

        - 사용자의 활용 목적에 따라 그래프 및 기능 생성
          dashboard.html - class="app.js에서 생성한 차트"

        ```html
        <!-- START card-->
        <div class="card card-default card-demo" id="cardChart9">
            <div class="card-header">
                <a class="float-right" href="#" data-tool="card-refresh" data-toggle="tooltip" title="Refresh card"><em class="fas fa-sync"></em></a>
                <a class="float-right" href="#" data-tool="card-collapse" data-toggle="tooltip" title="Collapse card"><em class="fa fa-minus"></em></a>
                <div class="card-title">2021년 월별 음식물 쓰레기 배출량 Chart</div>
            </div>
            <div class="card-wrapper">
                <div class="card-body">
                    <div class="chart-splinev3 flot-chart"></div>
                </div>
            </div>
        </div>
        <!-- END card-->
        ```

   3. 포트폴리오 제작
      - README.md 작성, 코드 정리 및 디버깅, , 완료보고서 PT 제작

      

6. 8월 18일 ~ 19일 :

   2. 최종 브라우저 UI
      
      공용 메인 페이지 구성
      ![trickmainui](https://github.com/Songgplant/KDT-Semi_Project02/blob/master/md_images/trickmainui.png)
      
      사용자 페이지 구성
      
      ![trickuserui](https://github.com/Songgplant/KDT-Semi_Project02/blob/master/md_images/trickuserui.png)
      
      관리자 페이지 구성
      ![trickmanagerui](https://github.com/Songgplant/KDT-Semi_Project02/blob/master/md_images/trickmanagerui.png)
      
   2. 최종 포트폴리오, 완료보고서 PT제작

   

7. 8월 20일 : 1차 최종 점검 및 발표



2. 8월 31일 : 경진대회 사전 보고서 제출마감(평가반영)



---

#### 팀원 GitHub주소

🤗[주현정님](https://github.com/HyunJung-Eliana)  🧐[송재현님](https://github.com/Songgplant)  🥰[안유진님](https://github.com/U-jjin)  😇[유준웅님](https://github.com/yoojunwoong)
