import sys
from bs4 import BeautifulSoup
import urllib.request

class returnObject:
    def __init__(self, forumURL = None, forumPost = None):
      self.forumURL = forumURL
      self.forumPost = forumPost

def getLatestForumPost():

    forumData = returnObject()

    # Get the HTML of the Iron Choobs forum page
    forumURL = 'https://secure.runescape.com/m=forum/c=zaAuPnMkWRg/forums?320,321,155,66237297,goto,'
    req = urllib.request.Request(url=forumURL, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()

    soup = BeautifulSoup(html, features="html.parser")

    # Retrieve the latest page on the forum from the bottom pagination boxes
    maxPaginationNumber = soup.find('input',class_="paginationWrap__number text")["max"]

    # Retrieve the HTML of the last page on the forum
    forumLastPageURL = forumURL + maxPaginationNumber
    req = urllib.request.Request(url=forumLastPageURL, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()

    soup = BeautifulSoup(html, features="html.parser")

    #Find the timestamp of the latest entry on the latest page 
    latestReplyTimestamp = soup.findAll('p', class_="forum-post__time-below")[-1].get_text()
    fp = open(r"PostTimestamp.txt", "r")
    latestReplySaved = fp.read()

    #Check if the timestamp matches that of the previously fetched latest message
    #If these do not match, it means a new message has been posted. Save the new timestamp
    # if(latestReplyTimestamp != latestReplySaved):
    fp = open(r"PostTimestamp.txt", "w+")
    fp.write(latestReplyTimestamp)

    forumData.forumURL = forumLastPageURL
    forumData.forumPost = soup.findAll('span', class_="forum-post__body")[-1].get_text()
    return forumData


