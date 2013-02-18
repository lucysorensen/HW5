import urllib2
from BeautifulSoup import *
from nltk.util import clean_html
import time
import csv
import re

class BlogScraper(object):
  def __init__(self, filename):
			self.filename = filename
			self.headers = ["is_post", "publish_date","author","url","post_title","comment_count"]
			self.readFile = open(self.filename, "wb")
			self.csvwriter = csv.writer(self.readFile)
			self.csvwriter.writerow(self.headers)
			self.i = 0

	def crawl(self, current_page):
		while self.i<5:
			time.sleep(.5)
			webpage=urllib2.urlopen(current_page)
			soup = BeautifulSoup(webpage.read())
			soup.prettify()
			
			posts = soup.findAll('div', {"class" : "post-content"})
			for post in posts:
				for link in post('a', rel="bookmark"): url = str(link['href'])
				time.sleep(.5)
				openpost = urllib2.urlopen(url)
				soup = BeautifulSoup(openpost.read())
				soup.prettify()
				if len(soup.findAll("div", {"class": "post "})) > 0: is_post = 1 
				elif len(soup.findAll("div", {"class": "post "})) == 0: is_post = 0
				post_title = clean_html(str(soup.find('title')))
				p = re.compile(r'Posted on ')
				publish_date = p.split(clean_html(str(soup.find('p', {"class": "post-details"}))))[1]
				author = "N/A"
				if clean_html(str(soup.find('h2', id = "comments-title"))) == "Be the first to leave a comment":
					comment_count = 0
				elif clean_html(str(soup.find('h2', id = "comments-title"))) == "What Others Are Saying":
					comment_list = soup.findAll('div', {"class" : "comment-meta"})
					comment_count = len(comment_list)
				self.csvwriter.writerow([is_post, publish_date, author, url, post_title, comment_count])	
		
			time.sleep(.5)
			webpage=urllib2.urlopen(current_page)
			soup = BeautifulSoup(webpage.read())
			soup.prettify()
			navigate = soup.find('div', {"class": "nav-previous"})
			for link in navigate('a'): new_url= str(link['href'])
			self.i += 1
			self.crawl(new_url)

hw5 = BlogScraper("hw5_results.csv")
hw5.crawl('http://dailyotter.org/')
