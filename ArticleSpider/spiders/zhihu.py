import re
import scrapy
import json

try:
    import urlparse as parse
except:
    from urllib import parse

class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['http://www.zhihu.com/']

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhihu.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    def parse(self, response):

        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = filter(lambda x:True if x.startswith("https") else False, all_urls) #exclude javascript file
        for url in all_urls:
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:    
                request_url = match_obj.group(1)
                question_id = match_obj.group(2)

                yield scrapy.Request(request_url, headers=self.headers, callback=)


    def parse_question(self, response):
        # deal with question page, extract specific question item
        if "QuestionHeader-title" in response.text:  
            # deal with new version
        else    
            # deal with old version
            

    def start_requests(self):  
        return [scrapy.Request('https://www.zhihu.com/#signin', headers=self.headers, callback=self.login)]

    def check_login(self, response):
        text_json = json.loads(response.text)
        if "msg" in text_json and text_json["msg"] == "登录成功": # login success
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers)

    def login(self, response):
        response_text = response.text 
        match_obj = re.match('.*name="_xsrf" value="(.*?)"', response_text, re.DOTALL)
        xsrf = ''
        if match_obj:
            xsrf = (match_obj.group(1))
        if xsrf:
            post_url = "https://www.zhihu.com/login/phone_num"
            post_data = {
                "_xsrf": xsrf,
                "phone_num": "18782902568",
                "password": "admin123"
            }

            return [scrapy.FormRequest(
                url = "https://www.zhihu.com/login/phone_num",
                formdata = post_data, 
                headers = self.headers,
                callback = self.check_login
            )]      