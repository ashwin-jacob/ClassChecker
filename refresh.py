from bs4 import BeautifulSoup
from urllib2 import urlopen
import time
import re
import sys
from string import strip
from smtplib import SMTP

department = raw_input('What department you want? (e.g RLST) ')
department = department.upper()
if not re.match("^[A-Z]*$", department):
	print "Invalid Department " + department
	sys.exit(0)

courseNumber = raw_input('What course number is it? (e.g. 110) ')
if not re.match("^[0-9]*$", courseNumber):
	print "Invalid Course Number " + courseNumber
	sys.exit(0)

URL = "https://courses.illinois.edu/cisapp/dispatcher/schedule/2013/spring/" + department + "/" + courseNumber
print URL

section = raw_input('What section you looking to get into? ')
section = section.upper()

class_status = 'section closed'
sleep_time = 5

while class_status != 'section open':
	fh = urlopen(URL)
	soup = BeautifulSoup(fh, "lxml")
	tBody = soup.tbody
	trType =  tBody.findAll('tr', {'class': re.compile('highlight-item-row')})
	for rowTables in trType:
		tdType = rowTables.findAll('td', {'class': re.compile('w55')})
		if strip(tdType[0].contents[2]) == section :
			imgFile =  rowTables.find('span')
			class_status = imgFile.string
			print class_status
	if class_status != 'section open':
		time.sleep(sleep_time)

courseName = department + ' ' + courseNumber
fromaddr = 'XXXXXXX' #froaddr = 'example@gmail.com'
toaddr = 'XXXXXX' #toaddr = 'example@gmail.com'
msg = 'Subject: %s\n\n%s has opened! ' % (courseName, courseName)

username = 'XXXXX' #username = 'example'
password = 'XXXXXX' #password = 'something'

server = SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.ehlo()
server.login(username, password)
server.sendmail(fromaddr, toaddr, msg)
server.quit()

print 'Message sent from "%s" to "%s"' % (fromaddr, toaddr)