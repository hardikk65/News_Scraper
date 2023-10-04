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
                'Url' : "https:://news.google.com" + title.css('a').attrib['href']}
    
    def parse_indian_express(self,response):
        titles = response.css('div.img-context')
        for title in titles:
            relative_url = title.css('h2 a').attrib['href']
            yield response.follow(relative_url,callback=self.parse_indianexpress_relative_url)

        next_page = response.css('a.next.page-numbers').attrib['href']
        if "16" not in next_page:
            next_page_url = next_page + ''
            yield response.follow(next_page_url,callback = self.parse_indian_express)
    
    
    def parse_india_today(self,response):
        titles = response.css('div.B1S3_content__thumbnail__wrap__iPgcS.content__thumbnail__wrap')
        for title in titles:
            relative_url = "https://www.indiatoday.in" + title.css('h2 a').attrib['href']
            yield response.follow(relative_url,callback=self.parse_indiatoday_relative_url)
    
    
    def parse_scroll(self,response):
        titles = response.css('li.row-story')
        for title in titles:
            relative_url = title.css('a').attrib['href']
            yield response.follow(relative_url,callback=self.parse_scroll_relative_url)



    def parse_indiatoday_relative_url(self,response):
        content_path = response.css('div.content__section p')
        content = ""
        for text in content_path:
            content = content + text.css('::text').get()
        
        yield{
            "Url":response.url,
            "Title": response.css('div.content__section h1::text').get(),
            "Description":response.css('div.content__section h2::text').get(),
            "Content":content,
            "Image_Url":response.css('div.content__section img').attrib['src']

        }
    def parse_indianexpress_relative_url(self,response):
        content_path = response.css('div.story-details')
        content = ""
        for text in content_path:
            content = content + text.css('p ::text').get()

        yield{
            "Url":response.url,
            "Title":response.css('div.heading-part h1::text').get(),
            "Description":response.css('div.heading-part h2::text').get(),
            "Content":content,
            "Image_Url":response.css('div.story-details img').attrib['src']
        }
    
    
    def parse_scroll_relative_url(self,response):
        content_path = response.xpath("//*[@id='article-contents']/p")
        content = ""
        for text in content_path:
            content = content + text.css("::text").get()
        
        yield{
            "Url":response.url,
            "Title" : response.css('div.main-container h1::text').get(),
            "Description" : response.css('div.main-container h2::text').get(),
            "Content": content,
            "Image_Url":response.css("div.main-container img").attrib['src']
        }