import scrapy

class NewsspiderSpider(scrapy.Spider):
    name = "newsspider"
    allowed_domains = ["news.google.com","indianexpress.com","indiatoday.in","scroll.in"]
    start_urls = ["https://news.google.com/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNRE55YXpBU0JXVnVMVWRDS0FBUAE?hl=en-IN&gl=IN&ceid=IN%3Aen","https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx1YlY4U0JXVnVMVWRDR2dKSlRpZ0FQAQ?hl=en-IN&gl=IN&ceid=IN%3Aen","https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx6TVdZU0JXVnVMVWRDR2dKSlRpZ0FQAQ?hl=en-IN&gl=IN&ceid=IN%3Aen","https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGRqTVhZU0JXVnVMVWRDR2dKSlRpZ0FQAQ?hl=en-IN&gl=IN&ceid=IN%3Aen","https://news.google.com/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNR3QwTlRFU0JXVnVMVWRDS0FBUAE?hl=en-IN&gl=IN&ceid=IN%3Aen"]
    categories = ['cities','sports','lifestyle','education','india']
    new_categories = ['india','world','business','technology','health','environment','law-today','education-today']
    
    scroll = ["76/politics","105/india","77/business-and-economy"]

    for category in scroll:
        url = "https://scroll.in/category/%s"%category
        start_urls.append(url)
    
    for category in new_categories:
        url = "https://www.indiatoday.in/%s"%category
        start_urls.append(url)
    
    
    for category in categories:
        url = 'https://indianexpress.com/section/%s/'%category
        start_urls.append(url)
    
    
    
    def parse(self, response):

        if "news.google.com" in response.url:
            return self.parse_google_news(response)
        elif "indianexpress.com" in response.url:
            return self.parse_indian_express(response)
        elif "indiatoday.in" in response.url:
            return self.parse_india_today(response)
        elif "scroll.in" in response.url:
            return self.parse_scroll(response)
        else:
            self.logger.warning("Unexpected url: %s",response.url)
    
    
    def parse_google_news(self,response):
        titles = response.css('div.W8yrY') + response.css('div.f9uzM')
        for title in titles:
            yield{
                'Title': title.css('h4 ::text').get(),
                'date' : '',
                'Url' : "https:://news.google.com" + title.css('a').attrib['href']}
    
    
    
    def parse_indian_express(self,response):
        titles = response.css('div.img-context')
        for title in titles:

            yield{
                'Title':title.css('h2 a::text').get(),
                'date':title.css('.date::text').get(),
                'Content':title.css('p::text').get(),
                'Url':title.css('h2 a').attrib['href']
            }
        next_page = response.css('a.next.page-numbers').attrib['href']
        if "16" not in next_page:
            next_page_url = next_page + ''
            yield response.follow(next_page_url,callback = self.parse_indian_express)
    
    
    def parse_india_today(self,response):
        titles = response.css('div.B1S3_content__thumbnail__wrap__iPgcS.content__thumbnail__wrap')
        load_more = response.css('div.viewall__bnt')
        for title in titles:
            yield{
                'Title':title.css('h2 a::text').get(),
                'Description':title.css('p ::text').get(),
                'date': '',
                'Image_url':title.css('img').attrib['src'],
                'Url':"https://www.indiatoday.in" + title.css('h2 a').attrib['href']
            }
    
    
    def parse_scroll(self,response):
        titles = response.css('li.row-story')

        for title in titles:
            yield{
                'Title' : title.css('h1 ::text').get(),
                'Description' : title.css('h2 ::text').get(),
                'Url' : title.css('a').attrib['href'],
                'Image_url' : title.css('img').attrib['src']
            }