
import re 
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class CCIM(CrawlSpider):

    #define your item template here
    class CCIM_DATA_ITEM(scrapy.Item):
        PageLink = scrapy.Field()
        FullName = scrapy.Field()
        Designations = scrapy.Field()
        Company = scrapy.Field()
        Address = scrapy.Field()
        Location = scrapy.Field()
        Phone = scrapy.Field()
        PropertyTypes = scrapy.Field()
        Specialization = scrapy.Field()
        SubSpecialization = scrapy.Field()

    name = 'CCIM_scrape'
    allowed_domains = ['findaccim.com']
    start_urls = ['http://www.findaccim.com/pub/ccim-find/results.cfm?my_location=&radius=20&location=&specialization=Investments&designation=&name=&company=']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(restrict_xpaths='//a[contains(text(),"next")]')),
        Rule(LinkExtractor(restrict_xpaths='//*[@class="website"][text()="View Profile"]'), callback='parse_item'),
    )


    def parse_item(self, response):

        def do_cleaning(dirtyFullName):

          cleanFullNameStep1 = re.sub("^\s+","",dirtyFullName)
          cleanFullNameStep2 = cleanFullNameStep1[:cleanFullNameStep1.find(",")]
         # cleanFullNameFinal = re.sub(cleanFullNameStep2)
          return cleanFullNameStep2

#['Cushman ', '189 bridge', '']
        def extract_company_address_and_location(xPathResults):
            
            incorrectList = ['#', 'floor', 'Floor', 'Apt', 'Street', 'Ave',
                            '0-9 (only numbers)', 'Suite', 'suite', 'ste', 
                            'Ste ', 'STE', 'P.O.', 'P.O', 'box', 'Box']
            
            xPathResultsFixed = ''
            if any(word in xPathResults[2] for word in incorrectList):
                xPathResultsFixed = xPathResults[0:2] + xPathResults[3:]
            elif len(xPathResults) <= 4:
                company_x = ''
                address_x = xPathResults[0]
                location_x = xPathResults[1]
                return company_x, address_x, location_x
            else:
                xPathResultsFixed = xPathResults

            company_x = xPathResultsFixed[0]
            address_x = xPathResultsFixed[1]
            location_x = xPathResultsFixed[2]
            return company_x, address_x, location_x
        


        dirtyFullName = response.xpath('//*[@class="xm-sidebar"]//text()').extract()[2]
        cleanFullName = do_cleaning(dirtyFullName)

        xpathRes = response.xpath('//*[@class="row"]//text()').extract()
        company, address, location = extract_company_address_and_location(xpathRes)

        item = self.CCIM_DATA_ITEM()
        item['PageLink'] = response.url
        item['FullName'] = cleanFullName
        item['Designations'] = response.xpath('//*[@class="box"]/h3[text()="Designations:"]/../ul/li//text()').extract()
        item['Company'] = company
        item['Address'] = address
        item['Location'] = location
        item['Phone'] = response.xpath('//*[@class="phone-link"]/text()').extract()
        item['PropertyTypes'] = response.xpath('//*[@class="box"]/h3[text()="Property Types:"]/../ul/li//text()').extract()
        item['Specialization'] = response.xpath('//*[@class="box"]/h3[text()="Professional Specializations:"]/../ul/li//text()').extract()
        item['SubSpecialization'] = response.xpath('//*[@class="box"]/h3[text()="Sub-Specializations:"]/../ul/li//text()').extract()

        return item







