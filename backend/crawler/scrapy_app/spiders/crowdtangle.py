from urllib import parse

import scrapy
from ..items import CrowdtangleFacebookItem, CrowdtangleInstagramItem
from dataprocess.models import CollectTarget
from dataprocess.models import Artist
from dataprocess.models import Platform
from datetime import datetime
from config.models import CollectTargetItem
from django.db.models import Q


class CrowdTangleSpider(scrapy.Spider):
    name = "crowdtangle"
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "crawler.scrapy_app.middlewares.LoginDownloaderMiddleware": 100
        },
    }
    facebook_id = Platform.objects.get(name="facebook").id
    instagram_id = Platform.objects.get(name="instagram").id
    CrawlingTarget = CollectTarget.objects.filter(Q(platform_id=facebook_id) | Q(platform_id=instagram_id))

    def start_requests(self):
        for row in self.CrawlingTarget:
            artist_name = Artist.objects.get(id=row.artist_id).name
            artist_url = row.target_url
            target_id = row.id
            print("artist : {}, url : {}, url_len: {}".format(
                artist_name, artist_url, len(artist_url)))
            yield scrapy.Request(url=artist_url, callback=self.parse, encoding="utf-8", meta={"artist": artist_name,
                                                                                              "target_id": target_id})

    def parse(self, response):
        artist = response.meta["artist"]
        follower_xpath = CollectTargetItem.objects.get(Q(collect_target_id=response.meta["target_id"]) & Q(target_name="followers")).xpath + "/text()"
        follower_num = None
        try:
            follower_num = response.xpath(follower_xpath).get()
        except ValueError:
            pass
            # Xpath Error라고 나올 경우, 잘못된 Xpath 형식으로 생긴 문제입니다.

        if follower_num is None:
            pass
            # Xpath가 오류여서 해당 페이지에서 element를 찾을 수 없는 경우입니다.
            # 혹은, Xpath에는 문제가 없으나 해당 페이지의 Element가 없는 경우입니다.
            # 오류일 경우 item을 yield 하지 않아야 합니다.
        else:
            url = parse.urlparse(response.url)
            target = parse.parse_qs(url.query)["platform"][0]
            if target == "facebook":
                item = CrowdtangleFacebookItem()
                item["artist"] = artist
                item["followers"] = int(follower_num.replace(",", ""))
                item["url"] = response.url
                item["reserved_date"] = datetime.now().date()
                yield item
            else:
                item = CrowdtangleInstagramItem()
                item["artist"] = artist
                item["followers"] = int(follower_num.replace(",", ""))
                item["url"] = response.url
                item["reserved_date"] = datetime.now().date()
                yield item
