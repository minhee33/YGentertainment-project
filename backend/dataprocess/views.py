import os
from django.contrib import auth
from django.shortcuts import render
from h11 import Data
from account.models import User

from dataprocess.models import CollectData
from crawler.models import *
from config.models import PlatformTargetItem, CollectTargetItem, Schedule
from config.serializers import PlatformTargetItemSerializer, CollectTargetItemSerializer, ScheduleSerializer
from dataprocess.functions import export_datareport, import_datareport, import_total
from django.views.decorators.csrf import csrf_exempt

from .serializers import *
from .models import *
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from utils.decorators import login_required
from utils.api import APIView, validate_serializer

from django.shortcuts import render
from django.http import HttpResponse

from datetime import datetime
import openpyxl
from openpyxl.writer.excel import save_virtual_workbook
from .resources import *
from .models import *
import logging

formatter = logging.Formatter('[%(asctime)s] - [%(levelname)s] - [%(name)s:%(lineno)d]  - %(message)s', '%Y-%m-%d %H:%M:%S')
serverlogger = logging.getLogger(__name__)
userlogger = logging.getLogger("HTTP-Method")

trfh = logging.handlers.TimedRotatingFileHandler(
    filename = os.path.join("../backend/data/log/user", f"{datetime.today().strftime('%Y-%m-%d')}.log"),
    when = "midnight",
    interval=1,
    encoding="utf-8",
)
trfh.setFormatter(formatter)
trfh.setLevel(logging.INFO)
userlogger.addHandler(trfh)
userlogger.setLevel(logging.DEBUG)

# login check using cookie
def logincheck(request):
    # 로그인 정보를 받기 위해 cookie사용
    username = request.COOKIES.get('username')
    if username is not None:
        if User.objects.filter(username=username).exists():
            # 이미 존재하는 username일때만 로그인
            user = User.objects.filter(username=username).first()
            auth.login(request, user)
    return request

# Create your views here.
def base(request):
    values = {
      'first_depth' : '데이터 리포트',
    }
    request = logincheck(request)
    return render(request, 'dataprocess/main.html',values)

@csrf_exempt
def daily(request):
    if request.method == 'GET':
        '''
        general page
        '''
        platforms = Platform.objects.all() #get all platform info from db
        values = {
            'first_depth' : '데이터 리포트',
            'second_depth': '일별 리포트',
            'platforms': platforms
        }
        request = logincheck(request)
        return render(request, 'dataprocess/daily.html',values)
    else:
        type = request.POST['type']
        if type == 'import':
            '''
            import from excel
            '''
            platforms = Platform.objects.all()  # get all platform info from db
            if not 'importData' in request.FILES:
                values = {
                    'first_depth' : '데이터 리포트',
                    'second_depth': '일별 리포트',
                    'platforms': platforms,
                    'alert': '파일을 첨부해주세요.'
                    }
                request = logincheck(request)
                return render(request, 'dataprocess/daily.html', values)
            import_file = request.FILES['importData']            
            excel_import_date = request.POST.get('excel_import_date', None)  # 0000-0-0 형태

            wb = openpyxl.load_workbook(import_file)
            sheets = wb.sheetnames
            worksheet = wb[sheets[0]]
            import_datareport(worksheet, excel_import_date)

            values = {
                'first_depth' : '데이터 리포트',
                'second_depth': '일별 리포트',
                'platforms': platforms,
                'alert': '저장되었습니다.'
                }
            request = logincheck(request)
            return render(request, 'dataprocess/daily.html',values)
        elif type == 'export':
            '''
            export to excel
            '''
            excel_export_type = request.POST.get('excel_export_days', None) # 누적 or 기간별
            excel_export_start_date = request.POST.get('excel_export_start_date', None) # 0000-0-0 형태
            excel_export_end_date = request.POST.get('excel_export_end_date', None) # 0000-0-0 형태
            book = export_datareport(excel_export_type, excel_export_start_date, excel_export_end_date)
            if excel_export_type == '누적':
                filename = "datareport %s.xlsx" % (excel_export_start_date)
            elif excel_export_type == '기간별':
                filename = "datareport기간별 %s~%s.xlsx" % (excel_export_start_date,excel_export_end_date)
            response = HttpResponse(content=save_virtual_workbook(book), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename='+filename
            return response
        elif type == 'import2':
            '''
            import2 from excel
            '''
            platforms = Platform.objects.all()  # get all platform info from db
            if not 'importData2' in request.FILES:
                values = {
                    'first_depth' : '데이터 리포트',
                    'second_depth': '일별 리포트',
                    'platforms': platforms,
                    'alert': '파일을 첨부해주세요.'
                    }
                request = logincheck(request)
                return render(request, 'dataprocess/daily.html', values)
            import_file = request.FILES['importData2']
            wb = openpyxl.load_workbook(import_file)
            sheets = wb.sheetnames
            worksheet = wb[sheets[0]]
            import_total(worksheet)
            values = {
                'first_depth' : '데이터 리포트',
                'second_depth': '일별 리포트',
                'platforms': platforms,
                'alert': '저장되었습니다.'
                }
            request = logincheck(request)
            return render(request, 'dataprocess/daily.html',values)
    
def platform(request):
     '''
     general page
     '''
     values = {
        'first_depth' : '플랫폼 관리',
        'second_depth': '플랫폼 관리'
    }
     request = logincheck(request)
     return render(request, 'dataprocess/platform.html',values)

def artist(request):
    artists = Artist.objects.all()
    values = {
      'first_depth' : '아티스트 관리',
      'second_depth': '데이터 URL 관리',
      'artists': artists
    }
    request = logincheck(request)
    return render(request, 'dataprocess/artist.html',values)

@csrf_exempt
def artist_add(request):
    platforms = Platform.objects.all()
    values = {
      'first_depth' : '아티스트 관리',
      'second_depth': '데이터 URL 관리',
      'platforms' : platforms
    }
    request = logincheck(request)
    return render(request, 'dataprocess/artist_add.html',values)

def monitering(request):
    platforms = Platform.objects.all()
    values = {
      'first_depth' : '모니터링 관리',
      'second_depth': '모니터링',
      'platforms' : platforms
    }
    request = logincheck(request)
    return render(request, 'dataprocess/monitering.html', values)


def login(request):
    values = {
      'first_depth' : '로그인'
    }
    request = logincheck(request)
    return render(request, 'dataprocess/login.html',values)

def platform_info(request):
    if request.method == 'GET':
        platform = request.GET.get('platform', None)
        try:
            platform_objects = Platform.objects.get(name = platform)
            
            if platform_objects.exists():
                platform_objects_values = platform_objects.values()
                platform_id = platform_objects_values['id']
                collecttargets = CollectTarget.objects.filter(platform = platform_id)
                collecttargets = collecttargets.values()
                platform_set = set()
                platform_list = []
                for collecttarget in collecttargets:
                    platform_objects = CollectTargetItem.objects.filter(collect_target_id = collecttarget['id'])
                    platform_objects_values = platform_objects.values()
                    for p in platform_objects_values:
                        if p['target_name'] in platform_set:
                            continue
                        platform_set.add(p['target_name'])
                        platform_list.append(p)
                return JsonResponse(data={'success': True, 'data': platform_list})
            else:
                return JsonResponse(data={'success': True, 'data': []})
        except:
            return JsonResponse(status=400, data={'success': False})


class PlatformAPI(APIView):
    # @login_required
    def get(self, request):
        '''
        Platform read api
        '''
        try:
            platform_objects = Platform.objects.all()
            if platform_objects.exists():
                platform_objects_values = platform_objects.values()
                platform_datas = []
                for platform_value in platform_objects_values:
                    platform_datas.append(platform_value)
                return JsonResponse(data={'success': True, 'data': platform_datas})
            else:
                return JsonResponse(data={'success': True, 'data': []})
        except:
            return JsonResponse(status=400, data={'success': False})

    # @login_required
    def post(self, request):
        '''
        Platform create api
        '''
        try:
            platform_object = JSONParser().parse(request)
            platform_serializer = PlatformSerializer(data=platform_object)
            if platform_serializer.is_valid():
                # 1. platform 생성
                platform_serializer.save()

                #특정 아티스트 전용 collect_target 생성 시 사용할 코드
                # 2. 현재 존재하는 모든 artist에 대해 collect_target 생성 -> platform과 연결
                artist_objects = Artist.objects.all()
                artist_objects_values = artist_objects.values()
                for artist_objects_value in artist_objects_values:
                    collecttarget = CollectTarget(
                        platform_id = platform_serializer.data['id'],
                        artist_id = artist_objects_value['id']
                        )
                    collecttarget.save()
                    #3. 해당 collecttarget에 대한 schedule 생성
                    schedule_object = Schedule.objects.filter(collect_target_id = collecttarget.id).first()
                    schedule_data = {
                            'collect_target': collecttarget.id,
                            'period': 'daily',
                            'active': True,
                            'excute_time': datetime.time(9,0,0)
                        }
                    schedule_serializer = ScheduleSerializer(schedule_object, data=schedule_data)
                    if schedule_serializer.is_valid():
                        schedule_serializer.save()
                    #4. 만든 collect target에 대해 수집항목들 생성
                    collecttarget_object = CollectTarget.objects.filter(platform = platform_serializer.data['id'],
                            artist = artist_objects_value['id'])
                    collecttarget_object = collecttarget_object.values()[0]
                    for collect_item in platform_object['collect_items']:
                        collect_item = CollectTargetItem(
                            collect_target_id=collecttarget_object['id'],
                            target_name=collect_item['target_name'],
                            xpath=collect_item['xpath']
                        )
                        collect_item.save()

                return JsonResponse(data={'success': True, 'data': platform_serializer.data}, status=status.HTTP_201_CREATED)
            return JsonResponse(data={'success': False,'data': platform_serializer.errors}, status=400)
        except:
            return JsonResponse(data={'success': False}, status=400)

    # @login_required
    def put(self, request):
        '''
        Platform update api
        '''
        try:
            platform_list = JSONParser().parse(request)
            for platform_object in platform_list:
                platform_data = Platform.objects.filter(pk=platform_object['id']).first()
                past_data = platform_data
                if platform_data is None:
                    # 원래 없는 건 새로 저장
                    platform_serializer = PlatformSerializer(data=platform_object)
                    if platform_serializer.is_valid():
                        platform_serializer.save()
                else:
                    data = PlatformSerializer(platform_data).data
                    print(data)
                    past_name = data["name"]
                    past_url = data["url"]
                    cur_name = platform_object["name"]
                    cur_url = platform_object["url"]
                    platform_serializer = PlatformSerializer(platform_data, data=platform_object)
                    if platform_serializer.is_valid():
                        if past_name != cur_name:
                            userlogger.info(f"[CHANGE]: {past_name} -> {cur_name}")
                        if past_url != cur_url:
                            userlogger.info(f"[CHANGE]: {past_url} -> {cur_url}")
                        platform_serializer.save()
                collecttarget_objects = CollectTarget.objects.filter(platform_id = platform_serializer.data['id'])
                if collecttarget_objects.exists():
                    collecttarget_values = collecttarget_objects.values()
                    for collecttarget_value in collecttarget_values:
                        schedule_object = Schedule.objects.filter(collect_target_id = collecttarget_value['id']).first()
                        schedule_data = {
                                'collect_target': collecttarget_value['id'],
                                'period': 'daily',
                                'active': platform_object['active'],
                                'excute_time': datetime.time(9,0,0)
                            }
                        schedule_serializer = ScheduleSerializer(schedule_object, data=schedule_data)
                        if schedule_serializer.is_valid():
                            schedule_serializer.save()
            return JsonResponse(data={'success': True}, status=status.HTTP_201_CREATED)
        except:
            return JsonResponse(data={'success': False}, status=400)

class ArtistAPI(APIView):
    # @login_required
    def get(self, request):
        '''
        Artist read api
        '''
        try:
            artist_objects = Artist.objects.all()
            if artist_objects.exists():
                artist_objects_values = artist_objects.values()
                artist_datas = []
                for artist_value in artist_objects_values:
                    artist_datas.append(artist_value)
                return JsonResponse(status=200,data={'success': True, 'data': artist_datas})
            else:
                return JsonResponse(data={'success': True, 'data': []})
        except:
            return JsonResponse(status=400, data={'success': False})

    # @login_required
    def post(self, request):
        '''
        Artist create api
        '''
        try:
            artist_object = JSONParser().parse(request)
            artist_serializer = ArtistSerializer(data=artist_object)
            if artist_serializer.is_valid():
                # 1. artist 생성
                artist_serializer.save()
                # 2. 현재 존재하는 모든 platform에 대해 collect_target 생성 -> artist와 연결
                for obj in artist_object['urls']:
                    platform_id = Platform.objects.get(name = obj['platform_name']).id
                    artist_id = artist_serializer.data['id']
                    target_url = obj['url1']
                    target_url_2 = obj['url2']
                    collecttarget = CollectTarget(
                        platform_id=platform_id,
                        artist_id=artist_id,
                        target_url=target_url,
                        target_url_2=target_url_2
                    )
                    collecttarget.save()
                    #3. 해당 collecttarget에 대한 schedule 생성
                    schedule_object = Schedule.objects.filter(collect_target_id = collecttarget.id).first()
                    schedule_data = {
                            'collect_target': collecttarget.id,
                            'period': 'daily',
                            'active': True,
                            'excute_time': datetime.time(9,0,0)
                        }
                    schedule_serializer = ScheduleSerializer(schedule_object, data=schedule_data)
                    if schedule_serializer.is_valid():
                        schedule_serializer.save()
    
                return JsonResponse(data={'success': True, 'data': artist_serializer.data}, status=status.HTTP_201_CREATED)
            return JsonResponse(data={'success': False,'data': artist_serializer.errors}, status=400)
        except:
            return JsonResponse(data={'success': False}, status=400)

    # @login_required
    def put(self, request):
        '''
        Artist update api
        '''
        try:
            artist_list = JSONParser().parse(request)
            for artist_object in artist_list:
                artist_data = Artist.objects.get(id=artist_object["id"])
                data = ArtistSerializer(artist_data).data
                print(data)
                past_name = data["name"]
                past_num = data["member_num"]
                past_agency = data["agency"]
                cur_name = artist_object["name"]
                cur_num = artist_object["member_num"]
                cur_agnecy = artist_object["agnecy"]
                artist_serializer = ArtistSerializer(artist_data, data=artist_object)
                if artist_serializer.is_valid():
                    if past_name != cur_name:
                        userlogger.info(f"[CHANGE]: {past_name} -> {cur_name}")
                    if past_num != cur_num:
                        userlogger.info(f"[CHANGE]: {past_num} -> {cur_num}")
                    if past_agency != cur_agnecy:
                        userlogger.info(f"[CHANGE]: {past_agency} -> {cur_agnecy}")
                    artist_serializer.save()
                else:
                    return JsonResponse(data={'success': False, 'data': artist_serializer.errors}, status=400)
            return JsonResponse(data={'success': True}, status=status.HTTP_201_CREATED)
        except:
            return JsonResponse(data={'success': False}, status=400)


class PlatformOfArtistAPI(APIView):
    # @login_required
    def get(self, request):
        '''
        Platform of Artist read api
        '''
        try:
            artist = request.GET.get('artist', None)
            # 해당 artist 찾기
            artist_object = Artist.objects.filter(name = artist)
            artist_object = artist_object.values()[0]
            # 해당 artist를 가지는 collect_target들 가져오기
            collecttarget_objects = CollectTarget.objects.filter(artist_id=artist_object['id'])
            if collecttarget_objects.exists():
                collecttarget_objects_values = collecttarget_objects.values()
                platform_datas = []
                for collecttarget_value in collecttarget_objects_values:
                    platform_object = Platform.objects.get(pk=collecttarget_value['platform_id'])
                    platform_datas.append({  
                        'artist_id':artist_object['id'],
                        'platform_id' : collecttarget_value['platform_id'],
                        'id': collecttarget_value['id'],
                        'name': platform_object.name,
                        'target_url':collecttarget_value['target_url'],
                        'target_url_2': collecttarget_value['target_url_2']
                    })
                return JsonResponse(data={'success': True, 'data': platform_datas})
            else:
                return JsonResponse(data={'success': True, 'data': []})
        except:
            return JsonResponse(status=400, data={'success': False})

    # @login_required
    def put(self, request):
        '''
        Platform of Artist update api
        '''
        try:
            collecttarget_list = JSONParser().parse(request)
            for collecttarget_object in collecttarget_list:
                CollectTarget.objects.filter(pk=collecttarget_object['id']).update(target_url=collecttarget_object['target_url'])
                if collecttarget_object['target_url_2']:
                    CollectTarget.objects.filter(pk=collecttarget_object['id']).update(target_url_2=collecttarget_object['target_url_2'])
            return JsonResponse(data={'success': True}, status=status.HTTP_201_CREATED)
        except:
            return JsonResponse(data={'success': False}, status=400)


class CollectTargetItemAPI(APIView):
    # @login_required
    def get(self, request):
        '''
        CollectTargetItem read api
        '''
        try:
            artist = request.GET.get('artist', None)
            platform = request.GET.get('platform', None)
            # 해당 artist, platform 찾기
            artist_object = Artist.objects.filter(name=artist)
            artist_object = artist_object.values()[0]
            platform_object = Platform.objects.filter(name=platform)
            platform_object = platform_object.values()[0]
            # 해당 artist와 platform을 가지는 collect_target 가져오기
            collecttarget_objects = CollectTarget.objects.filter(artist_id=artist_object['id'], platform_id=platform_object['id'])
            if collecttarget_objects.exists():
                collecttargetitems_datas = []
                collecttarget_objects_value = collecttarget_objects.values()[0]
                collecttargetitmes_objects = CollectTargetItem.objects.filter(collect_target_id=collecttarget_objects_value['id'])
                collecttargetitmes_values = collecttargetitmes_objects.values()
                for collecttargetitmes_value in collecttargetitmes_values:
                    collecttargetitems_datas.append(collecttargetitmes_value)
                # schedule 확인
                schedule_object = Schedule.objects.filter(collect_target_id = collecttarget_objects_value['id'])
                if schedule_object.exists():
                    period = schedule_object.values()[0]['period']
                else:
                    period = 'daily'
                return JsonResponse(data={'success': True, 'data': {'items':collecttargetitems_datas, 'period': period}})
            else:
                return JsonResponse(data={'success': True, 'data': {'items':[],'period':'daily'}})
        except:
            return JsonResponse(status=400, data={'success': False})

    # @login_required
    def put(self, request):
        '''
        CollectTargetItem update api
        '''
        try:
            collecttargetitem = JSONParser().parse(request)
            artist = collecttargetitem["artist"]
            platform = collecttargetitem["platform"]
            period = collecttargetitem["period"]
            collecttargetitem_list = collecttargetitem['items']
            artist_object = Artist.objects.filter(name = collecttargetitem['artist'])
            artist_object = artist_object.values()[0]
            platform_object = Platform.objects.filter(name = collecttargetitem['platform'])
            platform_object = platform_object.values()[0]
            collecttarget_object = CollectTarget.objects.filter(artist_id=artist_object['id'], platform_id=platform_object['id'])
            collecttarget_object = collecttarget_object.values()[0]
            for collecttargetitem_object in collecttargetitem_list:
                # 여기 수정!!!!
                collecttargetitem_data = CollectTargetItem.objects.filter(id=collecttargetitem_object['id'],
                                                                          target_name=collecttargetitem_object['target_name'], xpath=collecttargetitem_object['xpath']).first()
                # 없으면 새로 저장
                if collecttargetitem_data is None:
                    collecttargetitem_serializer = CollectTargetItemSerializer(data={
                        'collect_target': collecttarget_object['id'],
                        'target_name': collecttargetitem_object['target_name'],
                        'xpath': collecttargetitem_object['xpath']
                    })
                    if collecttargetitem_serializer.is_valid():
                        collecttargetitem_serializer.save()
                    else:
                        # return JsonResponse(data={"success": False, "data": collecttargetitem_serializer.errors}, status=400)
                        return JsonResponse(data={'success': False}, status=400)
                # 있으면 업데이트
                else:
                    collecttargetitem_serializer = CollectTargetItemSerializer(collecttargetitem_data, data=collecttargetitem_object)
                    if collecttargetitem_serializer.is_valid():
                        collecttargetitem_serializer.save()
                        userlogger.debug(f"{artist} - {platform} - {period}: ")
                    else:
                        return JsonResponse(data={'success': False,'data': collecttargetitem_serializer.errors}, status=400)
            Schedule.objects.filter(collect_target_id = collecttarget_object['id']).update(
                period = collecttargetitem['period'])
                
                
            return JsonResponse(data={'success': True}, status=status.HTTP_201_CREATED)
        except:
            return JsonResponse(data={'success': False}, status=400)

    def delete(self, request):
        '''
        CollectTargetItem delete api
        '''
        try:
            delete_id = JSONParser().parse(request)['id']
            obj = CollectTargetItem.objects.filter(id = delete_id)
            obj.delete()
            return JsonResponse(data={'success': True}, status=status.HTTP_200_OK)
        except:
            return JsonResponse(data={'success': False}, status=400)

#platform collect target API 
class PlatformTargetItemAPI(APIView):
    # @login_required
    def get(self, request):
        '''
        PlatformTargetItem read api
        '''
        try:
            platform = request.GET.get('platform', None)
            # 해당 platform 찾기
            platform_object = Platform.objects.filter(name = platform)
            platform_object = platform_object.values()[0]
            # 해당 platform을 가지는 platform_target 가져오기
            collecttarget_objects = PlatformTargetItem.objects.filter(platform_id = platform_object['id'])
            if collecttarget_objects.exists():
                collecttargetitems_datas = []
                collecttarget_objects_value = collecttarget_objects.values()[0]
                collecttargetitmes_objects = PlatformTargetItem.objects.filter(platform_id=collecttarget_objects_value['platform_id'])
                collecttargetitmes_values = collecttargetitmes_objects.values()
                for collecttargetitmes_value in collecttargetitmes_values:
                    collecttargetitems_datas.append(collecttargetitmes_value)
                return JsonResponse(data={'success': True, 'data': collecttargetitems_datas,'platform_id':collecttarget_objects_value['platform_id']})
            else:
                return JsonResponse(data={'success': True, 'data': []})
        except:
            return JsonResponse(status=400, data={'success': False})

    # @login_required
    def put(self, request):
        '''
        PlatformTargetItem update api
        '''
        try:
            collecttargetitem_list = JSONParser().parse(request)
            for i,collecttargetitem_object in enumerate(collecttargetitem_list):

                collecttargetitem_data = PlatformTargetItem.objects.filter(platform_id=collecttargetitem_object['platform'])[i]
                collecttargetitem_serializer = PlatformTargetItemSerializer(collecttargetitem_data, data=collecttargetitem_object)
                if collecttargetitem_serializer.is_valid():
                    collecttargetitem_serializer.save()
                else:
                    return JsonResponse(data={'success': False,'data': collecttargetitem_serializer.errors}, status=400)
            return JsonResponse(data={'success': True}, status=status.HTTP_201_CREATED)
        except:
            return JsonResponse(data={'success': False}, status=400)


class DataReportAPI(APIView):
    def get(self, request):
        '''
        Data-Report read api
        '''
        platform = request.GET.get('platform', None)
        type = request.GET.get('type', None)
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)

        #artist name
        artist_objects = Artist.objects.filter(active=1)
        artist_objects_values = artist_objects.values()
        artist_list = []
        for a in artist_objects_values:
            artist_list.append(a['name'])

        #platform target names
        platform_id = Platform.objects.get(name = platform).id
        collecttargets = CollectTarget.objects.filter(platform = platform_id)
        collecttargets = collecttargets.values()
        platform_list = set()
        for collecttarget in collecttargets:
            platform_objects = CollectTargetItem.objects.filter(collect_target_id = collecttarget['id'])
            platform_objects_values = platform_objects.values()
            for p in platform_objects_values:
                if p['target_name'] in platform_list:
                    continue
                platform_list.add(p['target_name'])
        platform_list = list(platform_list)
        #플랫폼 헤더 정보 순서와 db 칼럼 저장 순서 싱크 맞추기
        platform_header = []
        objects = CollectData.objects.filter(collect_items__platform=platform)
        objects_values = objects.values()
        if len(objects_values) > 0:
            key_list = list(objects_values[0]['collect_items'].keys())
            for key in key_list:
                if key in platform_list:
                    platform_header.append(key)
                else:
                    continue
        else:
            platform_header = platform_list


        try:
            if type == '누적':
                start_date_dateobject = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                start_date_string = start_date_dateobject.strftime("%Y-%m-%d")
                check = False
                filter_datas = []
                for artist in artist_list:
                    filter_objects = CollectData.objects.filter(collect_items__artist=artist, collect_items__platform=platform,
                        collect_items__reserved_date = start_date_string)
                    if filter_objects.exists():
                        check = True
                        # 같은 날짜에 여러개 있을 때 가장 앞의 것 가져오기
                        filter_value = filter_objects.values()[0]
                        filter_datas.append(filter_value['collect_items'])
                # 해당날짜에 데이터가 하나라도 있을 때
                if check:
                    return JsonResponse(data={'success': True, 'data': filter_datas, 'artists': artist_list, 'platform': platform_header})
                # 해당날짜에 데이터가 하나도 없을 때
                else:
                    crawling_artist_list = []
                    objects = CollectData.objects.filter(collect_items__platform=platform)
                    objects_value = objects.values()
                    for val in objects_value:
                        crawling_artist_list.append(val['collect_items']['artist'])
                    return JsonResponse(status=200, data={'success': True, 'data': 'no data', 'artists': artist_list, 'platform': platform_header,
                                                        'crawling_artist_list': crawling_artist_list})

            elif type == '기간별':
                # 전날 값을 구함
                start_date_dateobject = datetime.datetime.strptime(start_date, "%Y-%m-%d").date() - datetime.timedelta(1)
                end_date_dateobject = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
                start_date_string = start_date_dateobject.strftime("%Y-%m-%d")
                end_date_string = end_date_dateobject.strftime("%Y-%m-%d")
                check = False
                filter_datas_total = []
                for artist in artist_list:
                    filter_objects_start = CollectData.objects.filter(collect_items__artist=artist, collect_items__platform=platform,
                            collect_items__reserved_date = start_date_string)
                    filter_objects_end = CollectData.objects.filter(collect_items__artist=artist, collect_items__platform=platform,
                            collect_items__reserved_date = end_date_string)
                    # 둘 다 존재할 때
                    if filter_objects_start.exists() and filter_objects_end.exists():
                        check = True
                        filter_objects_start_value = filter_objects_start.values()[0]
                        filter_objects_start_value = filter_objects_start_value['collect_items']

                        # id랑 artist, date 빼고 보내주기
                        data_json = {}
                        filter_objects_end_value = filter_objects_end.values()[0]
                        filter_objects_end_value = filter_objects_end_value['collect_items']
                        for field_name in filter_objects_start_value.keys():
                            if field_name != 'id' and field_name != 'artist' and field_name != 'user_created' and field_name != 'recorded_date' and field_name != 'platform' and field_name!='artist' and field_name != 'url' and field_name != 'reserved_date' and field_name != 'updated_dt':
                                if filter_objects_end_value[field_name] is not None and filter_objects_start_value[field_name] is not None:
                                    data_json[field_name] = filter_objects_end_value[field_name] - filter_objects_start_value[field_name]
                                elif filter_objects_end_value[field_name] is not None:  # 앞의 날짜를 0으로 처리한 형태
                                    data_json[field_name] = filter_objects_end_value[field_name]
                                else: # 앞의 날짜가 없다면 0으로 보내기
                                    data_json[field_name] = 0
                            else:  # 숫자 아닌 다른 정보들(user_created 등)
                                data_json[field_name] = filter_objects_start_value[field_name]
                        filter_datas_total.append(data_json)
                    elif not filter_objects_start.exists() and filter_objects_end.exists():
                        # 시작날짜의 데이터가 존재하지 않고 끝날짜의 데이터만 존재할 때
                        # 시작날짜: 0으로 해서 계산 -> 끝날짜 데이터 자체를 보냄
                        check = True
                        filter_objects_end_value = filter_objects_end.values()[0]
                        filter_objects_end_value = filter_objects_end_value['collect_items']
                        filter_datas_total.append(filter_objects_end_value)
                if check: # 양끝 모두 존재 or 끝날짜만 존재
                    return JsonResponse(data={'success': True, 'data': filter_datas_total, 'artists': artist_list, 'platform': platform_header})
                else: # 끝날짜의 데이터가 아예 존재하지 않을 때
                    datename = "%s-%s-%s"%(end_date_dateobject.year, end_date_dateobject.month, end_date_dateobject.day)
                    return JsonResponse(status=400, data={'success': False, 'data': datename})
            else:
                start_date_dateobject = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                start_date_string = start_date_dateobject.strftime("%Y-%m-%d")
                objects = CollectData.objects.filter(collect_items__platform=platform,
                            collect_items__reserved_date = start_date_string)
                if objects.exists():
                    platform_queryset_values = objects.values()
                    platform_datas = []
                    for queryset_value in platform_queryset_values:
                        platform_datas.append(queryset_value['collect_items'])
                    return JsonResponse(data={'success': True, 'data': platform_datas, 'artists': artist_list, 'platform': platform_header})
                else:
                    return JsonResponse(status=400, data={'success': False, 'data': 'there is no data'})
        except:
            return JsonResponse(status=400, data={'success': False})
    
    def post(self, request):
        """
        Data-Report update api
        """
        update_data_object = JSONParser().parse(request)
        start_date = update_data_object[len(update_data_object)-1]['start_date']
        platform = update_data_object[len(update_data_object)-1]['platform_name']
        # artist name
        artist_objects = Artist.objects.filter(active=1)

        artist_objects_values = artist_objects.values()
        artist_list = []
        for a in artist_objects_values:
            artist_list.append(a['name'])

        # crawled artist list
        a_objects = CollectData.objects.filter(collect_items__platform=platform)
        a_objects_values = a_objects.values()
        a_list = []
        for val in a_objects_values:
            a_list.append(val['collect_items']['artist'])

        #platform target names
        platform_id = Platform.objects.get(name = platform).id
        collecttargets = CollectTarget.objects.filter(platform = platform_id)
        collecttargets = collecttargets.values()
        platform_list = set()
        for collecttarget in collecttargets:
            platform_objects = CollectTargetItem.objects.filter(collect_target_id = collecttarget['id'])
            platform_objects_values = platform_objects.values()
            for p in platform_objects_values:
                if p['target_name'] in platform_list:
                    continue
                platform_list.add(p['target_name'])
        platform_list = list(platform_list)

        #플랫폼 헤더 정보 순서와 db 칼럼 저장 순서 싱크 맞추기
        platform_header = []
        objects = CollectData.objects.filter(collect_items__platform=platform)
        objects_values = objects.values()
        if len(objects_values) > 0:
            key_list = list(objects_values[0]['collect_items'].keys())
            for key in key_list:
                if key in platform_list:
                    platform_header.append(key)
                else:
                    continue
        else:
            platform_header = platform_list

        try:
            start_date_dateobject = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            start_date_string = start_date_dateobject.strftime("%Y-%m-%d")
            for index, element in enumerate(update_data_object):
                if index == len(update_data_object)-1:
                    break
                artist_object = Artist.objects.filter(name=element['artist'])
                artist_object = artist_object.values()[0]
                platform_object = Platform.objects.filter(name=platform)
                platform_object = platform_object.values()[0]
                collecttarget_object = CollectTarget.objects.filter(platform_id = platform_object['id'],
                                        artist_id = artist_object['id'])
                collecttarget_object = collecttarget_object.values()[0]
                CollectData.objects.update_or_create(
                        collect_target_id = collecttarget_object['id'],
                        collect_items__reserved_date = start_date_string,
                        # collect_items = element,
                        # 바뀌는 값
                        defaults = {'collect_items': element}
                )
                    
            artist_set = set()
            filter_objects = CollectData.objects.filter(collect_items__platform=platform,
                            collect_items__reserved_date = start_date_string)
            if filter_objects.exists():
                filter_objects_values=filter_objects.values()
                filter_datas=[]

                crawling_artist_list = set()
                objects_value = filter_objects.values()
                for val in objects_value:
                    val = val['collect_items']
                    # 각 아티스트가 한번만 들어가도록
                    if val['artist'] in crawling_artist_list:
                        continue
                    crawling_artist_list.add(val['artist'])
                crawling_artist_list = list(crawling_artist_list)
                for filter_value in filter_objects_values:
                    filter_value = filter_value['collect_items']
                    # 각 아티스트당 하나의 데이터만 들어가도록
                    if filter_value['artist'] in artist_set:
                        continue
                    filter_datas.append(filter_value)
                return JsonResponse(data={'success': True, 'data': filter_datas,'artists':artist_list,'platform':platform_header,'crawling_artist_list':crawling_artist_list})
            else:
                # 존재하지 않을 때 -> 플랫폼 전체 데이터를 보자
                filter_objects = CollectData.objects.filter(collect_items__platform=platform)
                crawling_artist_list = set()
                objects_value = filter_objects.values()
                for val in objects_value:
                    val = val['collect_items']
                    # 각 아티스트가 한번만 들어가도록
                    if val['artist'] in crawling_artist_list:
                        continue
                    crawling_artist_list.add(val['artist'])
                crawling_artist_list = list(crawling_artist_list)
                # datename = "%s-%s-%s"%(start_date_dateobject.year, start_date_dateobject.month, start_date_dateobject.day)
                return JsonResponse(status=200, data={'success': True, 'data': 'no data', 'artists': artist_list, 'platform': platform_header, 'crawling_artist_list': crawling_artist_list})
        except:
            return JsonResponse(status=400, data={'success': False})
