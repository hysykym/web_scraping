import requests
from bs4 import BeautifulSoup
import pprint

def sort_stories_by_votes(hnlist):
    # sorted by key 'votes' in list(which save dicts objects) and reverse
    return sorted(hnlist, key= lambda k:k['votes'], reverse=True)

def create_custom_hn(links, subtext):
    hn = []
    # return index and item
    for idx, item in enumerate(links):
        # get text which = title
        title = item.getText()
        # get href if not defaul = None
        href = item.get('href', None)
        # select attribute=score from subtext
        vote = subtext[idx].select('.score')
        # if vote is not None
        if len(vote):
            # discard ' points' and turn into int
            points = int(vote[0].getText().replace(' points', ''))
            # pick point > 99's news
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes':points})
    return hn

# scrap
def scrap_pages(url, page):
    hn = []
    for i in range(page):
        # first page
        if i == 0:
            # get res
            res = requests.get(url)
            # work with bs4
            soup = BeautifulSoup(res.text, 'html.parser')
            # select attribute=titlelink
            links = soup.select('.titlelink')
            # select attribute=subtext
            subtext = soup.select('.subtext')
        else:
            # turn pages
            html_link2 = url + f'?p={i+1}'
            res = requests.get(html_link2)
            soup = BeautifulSoup(res.text, 'html.parser')
            links = soup.select('.titlelink')
            subtext = soup.select('.subtext')

        hn.extend(create_custom_hn(links, subtext))

    return sort_stories_by_votes(hn)

if __name__ == '__main__':
    print('-----start-----')

    # hacker news url
    url = 'https://news.ycombinator.com/news'
    # how many page u r goinf to scrap
    page = 5

    # print prettier
    pprint.pprint(scrap_pages(url, page))