from typing import Any
import scrapy
from scrapy.http import Response
import numpy as np
import os
from pathlib import Path
from datetime import datetime
import requests


class CarAuction(scrapy.Spider):
    name = 'car_auction'
    start_urls = ['https://bringatrailer.com/convertible/']
    allowed_domains = ['www.bringatrailer.com', 'bringatrailer.com']


    current_datetime = datetime.now().strftime("%Y-%m-%d")
    _abs_path  = "/".join(os.path.abspath(__file__).split('/')[:-1])
    image_path = Path(_abs_path).parent.joinpath('data/Pictures')
    if not os.path.exists(str(image_path)):
        os.makedirs(str(image_path))
    custom_settings = {
        "DOWNLOAD_DELAY" : 0.3,
        'FEEDS': { f'data/BringATrailer_CarAuctionData_{current_datetime}.csv': { 'format': 'csv', 'overwrite': True }},
        # 'ITEM_PIPELINES' : { "auction.pipelines.AuctionPipeline": 301 },
        'FILES_STORE' : image_path,
        'DOWNLOADER_MIDDLEWARES': {
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
        }
        # 'LOG_LEVEL' : 'ERROR'         
    }

    def parse(self, response):
        cars_url = response.css('.listings-container.items-container.auctions-grid .content-main >h3> a::attr(href)').extract()[:10]

        for url in cars_url:
            yield scrapy.Request(url=url, callback=self.parse_details)

    def parse_details(self, response):

        out = car_data = {
            "Car Name": np.nan,
            "Make": np.nan,
            "Model": np.nan,
            "Era": np.nan,
            "Origin": np.nan,
            "Seller": np.nan,
            "Location": np.nan,
            "Chassis Number": np.nan,
            "Lot Number": np.nan,
            "Price": np.nan,
            "Picture Path": np.nan
        }

        car_name = response.css('.post-title.listing-post-title::text').get()
        out['Car Name'] = car_name
        price = int(response.css('.listing-available-info > span > strong::text').get().replace('$','').replace(',',''))
        out['Price'] = price
        items_selector = response.css('.group-item')
        for item in items_selector:
            key = item.css('strong::text').get()
            val = item.css('button::text').get()
            if key in out.keys():
                out[key]  =  val

        seller = response.css('.item.item-seller > a::text').get()
        out['Seller'] = seller
        location = response.css('.essentials > a::text').get()
        out['Location'] = location
        chassis_number =  response.css('.essentials .item > ul > li')[0].css('a::text').get()
        out['Chassis Number'] =  chassis_number

        lot_number =  response.css('.essentials .item::text').extract()[-1].strip()
        out['Lot Number'] = lot_number
        out['Picture Path'] = self.image_path._str+'/'+lot_number+'.jpg'
        
        # Download image
        image_url = response.css('.post-image.wp-post-image::attr(src)').get()
        if image_url:
            image_path = os.path.join(str(self.image_path), out['Picture Path'])
            self.download_image(image_url, image_path)

        yield out

    def download_image(self, url, path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(path, 'wb') as f:
                f.write(response.content)

