import requests
import robotexclusionrulesparser
from urllib.parse import urlparse
from bs4 import BeautifulSoup

sitemaps = []
pages = []

def Start():
    startingpage = input().strip()
    parsedUrl = urlparse(startingpage)
    actualUrl = '{}://{}/robots.txt'.format(parsedUrl.scheme,parsedUrl.netloc)
    RoParser = robotexclusionrulesparser.RobotExclusionRulesParser()
    RoParser.fetch(actualUrl)
    return startingpage, RoParser


def GrabSitemaps(sitemap):
    r = requests.get(sitemap)
    soup = BeautifulSoup(r.text,'html.parser')
    locs = soup.findAll('loc')
    for loc in locs:
        if '.xml' in (loc.text):
            UrlLocation = loc.text
            sitemaps.append(UrlLocation)
        else:
            correctPage = loc.text
            pages.append(correctPage)

def CheckUrlStatus(RoParser):
    for sitepage in pages:
        r = requests.head(sitepage)
        status = r.status_code
        pages.remove(sitepage)
        if RoParser.is_allowed('*',sitepage):
            robots = 'Crawlable'
        else:
            robots = 'Non-Crawlable'
        with open('Results.csv','a',encoding='utf-8') as file:
            String = '"{}","{}","{}"\n'.format(sitepage,status,robots)
            file.write(String)

def main():
    StartURL,Robots = Start()
    GrabSitemaps(StartURL)
    CheckUrlStatus(Robots)
    while len(sitemaps) > 0:
        for sitemap in sitemaps:
            GrabSitemaps(sitemap)
            sitemaps.remove(sitemap)
        CheckUrlStatus(Robots)

main()
