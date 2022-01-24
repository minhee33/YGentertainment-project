# Define your item pipelines here
#
# Don"t forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from urllib import parse
from django.utils import timezone
from crawler.models import SocialbladeYoutube, SocialbladeTiktok, SocialbladeTwitter, SocialbladeTwitter2, \
    Weverse, CrowdtangleInstagram, CrowdtangleFacebook, Vlive, Melon, Spotify

from dataprocess.models import CollectData, CollectTarget

DataModels = {
    "youtube": SocialbladeYoutube,
    "tiktok": SocialbladeTiktok,
    "twitter": SocialbladeTwitter,
    "twitter2": SocialbladeTwitter2,
    "weverse": Weverse,
    "instagram": CrowdtangleInstagram,
    "facebook": CrowdtangleFacebook,
    "vlive": Vlive,
    "melon": Melon,
    "spotify": Spotify,
}


def process_itemsave(spider_name, item):
    nowdate = item["recorded_date"]
    model_name = None
    if spider_name == "crowdtangle":
        url = parse.urlparse(item["url"])
        model_name = parse.parse_qs(url.query)["platform"][0]
        dayfilter_obj = DataModels[model_name].objects.filter(artist=item["artist"],
                                                              recorded_date__year=nowdate.year,
                                                              recorded_date__month=nowdate.month,
                                                              recorded_date__day=nowdate.day)
    else:
        dayfilter_obj = DataModels[spider_name].objects.filter(artist=item["artist"],
                                                               recorded_date__year=nowdate.year,
                                                               recorded_date__month=nowdate.month,
                                                               recorded_date__day=nowdate.day)
    # 오늘일자로 이미 저장된 아티스트 정보가 있는 경우 => 데이터를 최신버전으로 수정
    if dayfilter_obj.exists():
        if spider_name == "youtube":
            return update_youtube(item)
        elif spider_name == "tiktok":
            return update_tiktok(item)
        elif spider_name == "twitter" or spider_name == "twitter2":
            return update_twitter(item, spider_name)
        elif spider_name == "weverse":
            return update_weverse(item)
        elif spider_name == "vlive":
            return update_vlive(item)
        elif spider_name == "crowdtangle":
            return update_crowdtangle(item, model_name)
        elif spider_name == "spotify":
            return update_spotify(item)
        elif spider_name == "melon":
            return update_melon(item)
    # 오늘일자로 저장된 데이터가 없는 경우 => 새로 생성
    else:
        item.save()
    return item


def update_youtube(item):
    nowdate = item["recorded_date"]
    existingItem = SocialbladeYoutube.objects.get(artist=item["artist"],
                                                  recorded_date__year=nowdate.year,
                                                  recorded_date__month=nowdate.month,
                                                  recorded_date__day=nowdate.day)
    existingItem.uploads = item.get("uploads")
    existingItem.subscribers = item.get("subscribers")
    existingItem.views = item.get("views")
    existingItem.recorded_date = nowdate
    existingItem.save()


def update_tiktok(item):
    nowdate = item["recorded_date"]
    existingItem = SocialbladeTiktok.objects.get(artist=item.get("artist"),
                                                 recorded_date__year=nowdate.year,
                                                 recorded_date__month=nowdate.month,
                                                 recorded_date__day=nowdate.day)
    existingItem.followers = item.get("followers")
    existingItem.uploads = item.get("uploads")
    existingItem.likes = item.get("likes")
    existingItem.recorded_date = nowdate
    existingItem.save()


def update_twitter(item, name):
    nowdate = item["recorded_date"]
    existingItem = DataModels[name].objects.get(artist=item.get("artist"),
                                                recorded_date__year=nowdate.year,
                                                recorded_date__month=nowdate.month,
                                                recorded_date__day=nowdate.day)
    existingItem.followers = item.get("followers")
    existingItem.twits = item.get("twits")
    existingItem.recorded_date = nowdate
    existingItem.save()


def update_weverse(item):
    nowdate = item["recorded_date"]
    existingItem = Weverse.objects.get(artist=item.get("artist"),
                                       recorded_date__year=nowdate.year,
                                       recorded_date__month=nowdate.month,
                                       recorded_date__day=nowdate.day
                                       )
    existingItem.weverses = item.get("weverses")
    existingItem.recorded_date = nowdate
    existingItem.save()


def update_vlive(item):
    nowdate = item["recorded_date"]
    existingItem = Vlive.objects.get(artist=item.get("artist"),
                                     recorded_date__year=nowdate.year,
                                     recorded_date__month=nowdate.month,
                                     recorded_date__day=nowdate.day
                                     )
    existingItem.members = item.get("members")
    existingItem.videos = item.get("videos")
    existingItem.likes = item.get("likes")
    existingItem.plays = item.get("plays")
    existingItem.recorded_date = nowdate
    existingItem.save()


def update_melon(item):
    nowdate = item["recorded_date"]
    existingItem = Melon.objects.get(artist=item.get("artist"),
                                     recorded_date__year=nowdate.year,
                                     recorded_date__month=nowdate.month,
                                     recorded_date__day=nowdate.day
                                     )
    existingItem.listeners = item.get("listeners")
    existingItem.streams = item.get("streams")
    existingItem.recorded_date = nowdate
    existingItem.save()


def update_spotify(item):
    nowdate = item["recorded_date"]
    existingItem = Spotify.objects.get(artist=item.get("artist"),
                                       recorded_date__year=nowdate.year,
                                       recorded_date__month=nowdate.month,
                                       recorded_date__day=nowdate.day
                                       )
    existingItem.monthly_listens = item.get("monthly_listens")
    existingItem.followers = item.get("followers")
    existingItem.recorded_date = nowdate
    existingItem.save()


def update_crowdtangle(item, name):
    nowdate = item["recorded_date"]
    existingItem = DataModels[name].objects.get(artist=item.get("artist"),
                                                recorded_date__year=nowdate.year,
                                                recorded_date__month=nowdate.month,
                                                recorded_date__day=nowdate.day
                                                )
    existingItem.followers = item.get("followers")
    existingItem.recorded_date = nowdate
    existingItem.save()


def datasave(spider_name, item):
    Target_row = CollectData()
    json_obj = {
        "artist": item.get("artist"),
        "recorded_date": str(item.get("recorded_date")),
        "reserved_date": str(item.get("reserved_date")),
    }
    if spider_name == "youtube":
        json_obj["uploads"] = item.get("uploads")
        json_obj["subscribers"] = item.get("subscribers")
        json_obj["views"] = item.get("views")
        json_obj["user_created"] = item.get("user_created")
        json_obj["url"] = item.get("url")
        target_foreign_key = CollectTarget.objects.get(target_url=item.get("url"))
    elif spider_name == "tiktok":
        json_obj["uploads"] = item.get("uploads")
        json_obj["followers"] = item.get("followers")
        json_obj["likes"] = item.get("likes")
        json_obj["url"] = item.get("url")
        target_foreign_key = CollectTarget.objects.get(target_url=item.get("url"))
    elif spider_name == "twitter" or spider_name == "twitter2":
        target_foreign_key = CollectTarget.objects.get(target_url=item.get("url"))
        json_obj["followers"] = item.get("followers")
        json_obj["twits"] = item.get("twits")
        json_obj["user_created"] = item.get("user_created")
    elif spider_name == "weverse":
        target_foreign_key = CollectTarget.objects.get(target_url=item.get("url"))
        json_obj["weverses"] = item.get("weverses")
        json_obj["url"] = item.get("url")
    elif spider_name == "vlive":
        json_obj["members"] = item.get("members")
        json_obj["videos"] = item.get("videos")
        json_obj["likes"] = item.get("likes")
        json_obj["plays"] = item.get("plays")
        json_obj["url"] = item.get("url")
        target_foreign_key = CollectTarget.objects.get(target_url=item.get("url"))
    elif spider_name == "crowdtangle":
        target_foreign_key = CollectTarget.objects.get(target_url=item.get("url"))
        json_obj["followers"] = item.get("followers")
        json_obj["url"] = item.get("url")
    elif spider_name == "spotify":
        target_foreign_key = CollectTarget.objects.get(target_url=item.get("url1"))
        json_obj["monthly_listens"] = item.get("monthly_listens")
        json_obj["followers"] = item.get("followers")
        json_obj["url1"] = item.get("url1")
        json_obj["url2"] = item.get("url2")
    elif spider_name == "melon":
        json_obj["listeners"] = item.get("listeners")
        json_obj["streams"] = item.get("streams")
        json_obj["fans"] = item.get("fans")
        json_obj["url1"] = item.get("url1")
        json_obj["url2"] = item.get("url2")
        target_foreign_key = CollectTarget.objects.get(target_url=item.get("url1"))
    Target_row.collect_target = target_foreign_key
    Target_row.collect_items = json_obj
    Target_row.save()


class CrawlerPipeline(object):
    def process_item(self, item, spider):
        spider_name = spider.name  # spider의 이름을 추출 => 동적으로 spider에 따라 다른 pipeline 적용
        item["recorded_date"] = timezone.now()  # 업데이트 시간 기록
        process_itemsave(spider_name, item)
        datasave(spider_name, item)
