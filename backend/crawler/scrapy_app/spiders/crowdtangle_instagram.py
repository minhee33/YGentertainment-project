import scrapy
from ..items import CrowdtangleInstagramItem


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'crawler.scrapy_app.middlewares.LoginDownloaderMiddleware': 100
        },
    }

    def start_requests(self):
        artist_url = {
            "(여자)아이들": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=3717929&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "강다니엘": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=7946074&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "뉴이스트": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=6134770&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "레드벨벳": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=1161921&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "레드벨벳 아이린": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=8352992&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "레드벨벳 슬기": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=7690785&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "레드벨벳 조이": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=7662272&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "레드벨벳 웬디": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=8698641&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "레드벨벳 예리": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=7449501&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "마마무": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=750100&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "마마무 화사": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=11324282&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "몬스타엑스": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=948219&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "방탄소년단": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=2063917&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "BLACKPINK": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=1594362&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "BLACKPINK 로제": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=3634803&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "BLACKPINK 리사": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=3634802&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "BLACKPINK 제니": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=3634804&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "BLACKPINK 지수": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=3634835&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "BIGBANG": "",
            "BIGBANG 지드래곤": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=498252&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "샤이니": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=2173543&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "세븐틴": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=700570&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "슈퍼주니어": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=2084419&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "스트레이키즈": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=2716404&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "아스트로": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=1601005&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "아스트로 차은우": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=8290675&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "에스파": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=12888527&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "WINNER": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=546716&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "크래비티": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=11046726&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "트와이스": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=539004&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "AB6IX": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=7116257&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "에이티즈": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=4464212&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "엔하이픈": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=12560393&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "EXO": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=2430207&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "엑소 백현": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=516119&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "iKON": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=1608661&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "ITZY": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=7242503&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "NCT": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=3057855&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "NCT 127": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=1608113&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "NCT DREAM": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=2075142&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "NCT U": "",
            "더보이즈": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=2533648&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "TREASURE": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=6631235&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "TXT": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=6468950&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "WayV": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=6088359&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "청하": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=2059507&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "선미": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=538358&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "전소미": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=1588553&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "AKMU": "",
            "AKMU 이수현": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=546718&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "아이유": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=546887&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "헤이즈": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=722084&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "소녀시대": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=4768248&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "소녀시대 태연": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=499786&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "이하이": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=526346&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "정은지": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=650201&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "젝스키스": "",
            "백예린": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=731755&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "볼빨간사춘기": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=2090504&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "현아": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=499885&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "비투비": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=751103&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "SF9": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=2137066&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "스테이씨": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=13111105&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "오마이걸": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=950902&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "위클리": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=instagram_feed&accounts=11984315&brandedContentType=none&comparisonType=none&followersShowByType=total&graphType=subscriber_count&interval=day&platform=instagram&reportTimeframe=3months",
            "HYBE LABELS": "",
            "SM ENTERTAINMENT": "",
            "JYP ENTERTAINMENT": "",
        }

        for artist, url in artist_url.items():
            print("artist : {}, url : {}, url_len: {}".format(
                artist, url, len(url)))
            if len(url) > 0:
                yield scrapy.Request(url=url, callback=self.parse, encoding='utf-8', meta={'artist': artist})
            else:
                continue

    def parse(self, response):
        artist = response.meta['artist']
        follower_num = response.xpath(
            '/html/body/div[3]/div/div/div/div/div[3]/div[2]/div[1]/div/div[3]/div[2]/div/div[2]/div[1]/div/div[2]/div/span[1]/text()').extract()[0]
        item = CrowdtangleInstagramItem()
        item['artist'] = artist
        item['followers'] = follower_num.replace(',', '')
        item['url'] = response.url
        yield item
