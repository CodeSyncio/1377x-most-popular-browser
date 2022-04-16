
import pyperclip
from unicodedata import category
import requests
from bs4 import BeautifulSoup
from time import sleep
from linecache import getline as gl
import os

curdir = os.getcwd()
mainconfigdir = curdir + '/configs/config.txt'
LinkAmount = gl(mainconfigdir,2)
SleepAmount = gl(mainconfigdir,1)

def cls():                                         
    os.system('cls' if os.name=='nt' else 'clear')     

def chooser():
    cls()
    print('Choose a category:')
    categorys = ['games', 'movies','music','other']
    for x in range(len(categorys)):
        print (categorys[x]),

    category_choise = input('Choosen option: ')
    if category_choise in categorys:
        pass
    else:
        return chooser()
    indexcat = categorys.index(category_choise)
    
    global linkext
    if category_choise == categorys[0]:
        linkext = 'popular-'+categorys[0]
    elif category_choise == categorys[1]:
        linkext = 'popular-'+categorys[1]
    elif category_choise == categorys[2]:
        linkext = 'popular-'+categorys[2]
    elif category_choise == categorys[3]:
        linkext = 'popular-'+categorys[3]

chooser()

def mainf():
    cls()
    requrl = ('https://www.1377x.to/'+linkext)
    page = requests.get(requrl) # Getting page HTML through request
    soup = BeautifulSoup(page.content, 'html.parser') # Parsing content using beautifulsoup

    links = soup.select("table tbody tr td.coll-1.name a") # Selecting all of the anchors with titles
    Tracknumbr = 1
    toplist = []
    sidelist = []
    torrentlinksunfitered = []
    for anchor in links:
        toplist.append(anchor.text)
#print (toplist)
    for anchor in links:
        sidelist.append(anchor.attrs)

    for link in soup.find_all('a'):
        torrentlinksunfitered.append(link.get('href'))

    torrentlinks = [x for x in torrentlinksunfitered if x.startswith('/torrent/')]

    while("\n" in toplist) :
        toplist.remove("\n")

    counter = 1
    for x in range(len(toplist)):
        if counter != (int(LinkAmount) + 1):
            print (str(counter)+ '. '+toplist[x])
            counter = counter + 1

    chosenflwnmbr = input('choose a link:    [type "back" to choose another section] \n')
    cls()
    if chosenflwnmbr != 'back':
        
        if int(chosenflwnmbr) < int(LinkAmount) + 1:
            
            chosentorrenttext =(toplist[int(chosenflwnmbr) - 1])
            chosentorrentpath = (torrentlinks[int(chosenflwnmbr) - 1])
        else:
            return mainf()()
    else:
        chooser()
        mainf()()

    buildedlink = ('https://www.1377x.to'+ chosentorrentpath)

    magnetrequrl = (buildedlink)
    magnetpage = requests.get(magnetrequrl) # Getting page HTML through request
    magnetsoup = BeautifulSoup(magnetpage.content, 'html.parser') # Parsing content using beautifulsoup
    magnetunfiltered = []

    for link in magnetsoup.find_all('a'):
        magnetunfiltered.append(link.get('href'))

    magnetlink = [x for x in magnetunfiltered if x.startswith('magnet')]

    cls()

    pyperclip.copy(magnetlink[0])
    print('The magnet link has been copied to your clipboard, returning to torrent chooser in ' +str(SleepAmount)+ ' seconds' )
    sleep(int(SleepAmount))
    cls()
    mainf()()
    
mainf()()