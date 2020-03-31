# -*- coding: utf-8 -*-
import scrapy


class PurplePlanetSpider(scrapy.Spider):
    name = 'purple-planet'
    allowed_domains = ['www.purple-planet.com']
    start_urls = ['http://www.purple-planet.com/']

    def parse(self, response):
        song_slugs = response.css("script").re(r"\"pageUriSEO\":\"(.*?)\"")
        for slug in song_slugs:
            yield scrapy.Request(response.urljoin(slug), callback=self.parse_song)

    def parse_song(self, response):
        song_dropbox_url = response.xpath(
            "//a[contains(@href, 'dropbox')]/@href").get("")
        title = response.css("title::text").re_first("([\w\s'-]*) |")

        if not title:
            import ipdb; ipdb.set_trace()

        yield {
            "title": title,
            "download_url": song_dropbox_url.replace("dl=0", "dl=1"),
            "free_download": bool(song_dropbox_url)
        }
