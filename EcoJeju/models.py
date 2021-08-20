from django.db import models

class user(models.Model):
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

class worker(models.Model):
    worker_id = models.CharField(max_length=20, unique=True, verbose_name="유저 아이디", primary_key=True)
    worker_pwd = models.CharField(max_length=20, verbose_name='유저 비밀번호')
    worker_name = models.CharField(max_length=20, verbose_name= '유저 이름')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name="계정생성시간")

    def __str__(self):
        return self.worker_name;
    class Meta:
        db_table = 'worker'
        verbose_name ='worker 사용자'
        verbose_name_plural='worker 사용자'

class workerarea(models.Model):
    workerarea_id = models.AutoField(primary_key=True)
    worker_id = models.CharField(max_length=20, verbose_name="담당자")
    area_cd = models.CharField(max_length=20, verbose_name="담당 구역 코드")

    def __str__(self):
        return self. workerarea_id;
    class Meta:
        db_table = 'workerarea'
        verbose_name ='담당 구역 정보'
        verbose_name_plural='담당 구역 정보'

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

class region(models.Model):
    region_id = models.CharField(max_length=20, unique=True, verbose_name="지역 아이디",primary_key=True)
    region_name = models.CharField(max_length=20, verbose_name="구역 이름")
    parent_name =  models.CharField(max_length=20, verbose_name="지역 이름",null=True)
    city_name = models.CharField(max_length=20, verbose_name="도시 이름", null=True)

    def __str__(self):
        return self.region_name;
    class Meta:
        db_table = 'region'
        verbose_name ='지역 코드 정보'
        verbose_name_plural='지역 코드 정보'




class disposedata(models.Model):
    dispose_id = models.AutoField(primary_key=True)
    dispose_user_id= models.CharField(max_length=20, verbose_name="사용 유저 아이디")
    dispose_region_code =  models.CharField(max_length=20, verbose_name="구역 코드")
    dispose_weight = models.IntegerField(verbose_name="유저 쓰레기 무게")
    dispose_amount = models.IntegerField(verbose_name="유저 쓰레기 비용")
    dispose_date = models.DateTimeField(verbose_name="배출 시간")

    def __str__(self):
        return self.dispose_id;
    class Meta:
        db_table = 'disposedata'
        verbose_name ='개인 배출 정보'
        verbose_name_plural='개인 배출 정보'

class wasteprediction(models.Model):
    prediction_id = models.AutoField(primary_key=True)
    region = models.CharField(max_length=20, verbose_name="지역 이름")
    onemonth = models.IntegerField(verbose_name="다음달 예측")
    tw0month = models.IntegerField(verbose_name="다다음달 예측")

    def __str__(self):
        return self.dprediction_id;
    class Meta:
        db_table = 'wasteprediction'
        verbose_name ='음식물 쓰레기 예측 배출량'
        verbose_name_plural='음식물 쓰레기 예측 배출량'