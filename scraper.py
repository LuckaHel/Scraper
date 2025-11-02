import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://www.nrsr.sk/web/Default.aspx?sid=poslanci/zoznam_abc&ListType=0&CisObdobia=9",
    ]

    def parse(self, response):
        poslanci_list =  response.xpath('//div[@class="mps_list_block"]//li/a')
        member_dic = {}
        for p in poslanci_list:
            # print(p)
            name = p.css('a::text').get()
            # print(name)
            profile_link = p.xpath('@href').get()
            if profile_link is not None:
                yield response.follow(profile_link, callback=self.parse_profile)
        # print(member_dic)
    
    def parse_profile(self, response):
        membership = response.xpath('//div[@class="box"]//li/text()').get()
        print(membership.split("(")[0])

            
