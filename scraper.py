import scrapy
import json
import re


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://www.nrsr.sk/web/Default.aspx?sid=poslanci/zoznam_abc&ListType=0&CisObdobia=9",
    ]

    def parse(self, response):
        poslanci_list =  response.xpath('//div[@class="mps_list_block"]//li/a')
    
        for p in poslanci_list:
            profile_link = p.xpath('@href').get()
            if profile_link is not None:
                yield response.follow(profile_link, callback=self.parse_profile)
        
        self.count_rozpravy() 
               
            
    def count_rozpravy(self):
        with open('raw.jsonl') as f:
           for line in f:
                record = json.loads(line)
                print("type>>>>>>>>" + str(type(record)))
                print("one ine when opening json >>>>>>>>>>>>" )
                print(record)
        
    
    def parse_profile(self, response):
        membership = response.xpath('//div[@class="box"]//li/text()').get()
        personal_info = [
            response.xpath('//div[@class="grid_4 omega"]//span').get(),
            response.xpath('//div[@class="grid_4 alpha"]//span').get(),
            response.xpath('//div[@class="grid_8 alpha omega"]//span').get()]
        
        partial_link_to_rozpravy = response.xpath('//div[@class="box"]/ul[@class="aktivity"]/li').getall()
        link_to_rozpravy = "https://www.nrsr.sk/web/" + re.search(r'href="([^"]*)"', partial_link_to_rozpravy[0]).group(1)
        
        for i in range(len(personal_info)):
            if personal_info[i] is None: #if tperson has no title replace none with empty string
                personal_info[i] = ""
            else:
                personal_info[i] = re.sub(r'<[^>]*>', '', personal_info[i]).strip()
                

        yield {
        "party": membership.split("(")[0].strip(),
        "name_and_title": str(personal_info),
        "link_to_rozpravy" :link_to_rozpravy   
    }
    
        
    
        
        

    

            
