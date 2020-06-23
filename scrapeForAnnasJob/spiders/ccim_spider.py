#written by Anna Bugankova

import scrapy
import time
import re
from urllib2 import urlopen


class CCIM(scrapy.Spider):
	name = "CCIM"
	allowed_domains = ['findaccim.com']
	start_urls = ["http://www.findaccim.com/pub/ccim-find/results.cfm?my_location=&radius=20&location=&specialization=Agent%2FBroker%2FAll&designation=&name=&company="]

	#code taken from https://www.datacamp.com/community/tutorials/making-web-crawlers-scrapy-python
	#other tutorial: https://blog.scrapinghub.com/price-intelligence-with-python-scrapy-sql-pandas
	#While in "View Profile" scrape information below

	
	def parse_profile_page(self, response):

	  def do_cleaning(dirtyFullName):

		  cleanFullNameStep1 = re.sub("^\s+","",dirtyFullName)
		  cleanFullNameStep2 = cleanFullNameStep1[:cleanFullNameStep1.find(",")]
		 # cleanFullNameFinal = re.sub(cleanFullNameStep2)

		  print "ddd", cleanFullNameStep2
		  return cleanFullNameStep2


	  FullName =response.xpath('//*[@class="xm-sidebar"]//text()').extract()[2]
	  Designations =response.xpath('//*[@class="box"]/h3[text()="Designations:"]/../ul/li//text()').extract()
	  Company =response.xpath('//*[@class="row"]//text()').extract()[0]
	  Address =response.xpath('//*[@class="row"]//text()').extract()[1]
	  Location =response.xpath('//*[@class="row"]//text()').extract()[2]
	  Phone =response.xpath('//*[@class="phone-link"]/text()').extract()
	  PropertyTypes =response.xpath('//*[@class="box"]/h3[text()="Property Types:"]/../ul/li//text()').extract()
	  Specialization =response.xpath('//*[@class="box"]/h3[text()="Professional Specializations:"]/../ul/li//text()').extract()
	  SubSpecialization =response.xpath('//*[@class="box"]/h3[text()="Sub-Specializations:"]/../ul/li//text()').extract()

	  cleanFullNameFinal = do_cleaning(FullName)

	  scraped_info = {
		    	'itemFullName' : cleanFullNameFinal, #item[0] means product in the list and so on, index tells what value to assign
		    	'itemDesignations' : Designations,
		     	'itemCompany' : Company,
		     	'itemAddress' : Address,
		     	'itemLocation' : Location,
		     	'itemPhone' : Phone,
		     	'itemPropertyTypes' : PropertyTypes,
		     	'itemSpecialization' : Specialization,
		     	'itemSubSpecialization' : SubSpecialization
		    }



	  yield scraped_info





	def click_profile_links(self, response, links):

	  viewProfileXpath = '//*[@class="website"][text()="View Profile"]//@href'
	  
	  if links == []:
	  	links = response.xpath(viewProfileXpath).extract()

	  if len(links) == 1:
	  	return scrapy.Request(
		    response.urljoin(links[0]),
		    callback=self.parse,
		    meta={'dont_redirect': True})

	  else:
	  	return scrapy.Request(
		    response.urljoin(links[0]),
		    callback=self.parse,
		    meta={'dont_redirect': True}), self.click_profile_links(response, links[1:])

	def click_next_page(self, response):


	  nextPageXPath = '//a[contains(text(),"next")]//@href'
	  next_page = response.xpath(nextPageXPath).extract_first()
	  nextPageUrl = 'http://www.findaccim.com/pub/ccim-find/results.cfm?SPECIALIZATION=&name=&radius=20&my_location=&company=&location=&designation=&page=5'

	  return scrapy.Request(
	      response.urljoin(next_page),
	      callback=self.parse,
	      meta={'dont_redirect': True}) 


	def parse(self, response):

	  if 'member_id' in response.url:
	    return self.parse_profile_page(response) 
	  else:
	    print 'super'
	    return self.click_next_page(response), self.click_profile_links(response, [])

#<a href="https://www.powells.com/category/arts-and-entertainment?pg=2" id="ctl00_SearchBody_NavigationBottom_lnkNext"
#//div[@id="images"]
#to run call
'scrapy crawl --set="ROBOTSTXT_OBEY=False" powellsSpider'
#to activate call
'source env/bin/activate'


# To change settings: anna$ scrapy crawl --set="ROBOTSTXT_OBEY=False" --set="FEED_URI=output.csv" --set="REFERRER_POLICY=no-referrer" CCIM --set="FEED_FORMAT=csv"
