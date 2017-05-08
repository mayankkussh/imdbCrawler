import requests, bs4
movie_links = []
movie_information = []
def parsePage(soup, url):
    global movie_information
    try:
            schema_div = soup.find('div', {'id': 'pagecontent'})
            if (not (schema_div.has_attr('itemtype') and schema_div['itemtype']== 'http://schema.org/Movie')):
                return;
            movie = {};
            content_div = soup.find('div', {'id': 'title-overview-widget'})
            movie['title'] = content_div.select('h1.header > span.itemprop')[0].text
            movie['year'] = content_div.select('h1.header > span.nobr > a')[0].text
            movie['rating'] = content_div.select('div.star-box-giga-star')[0].text
            movie['directors'] = []
            movie['url'] = url
            for i in content_div.select("div[itemprop=director] > a span"):
               movie['directors'].append(i.text)
            movie_information.append(movie)
            print(movie)
    except(Exception):
        pass
    return

def process_request(url):
    res = requests.get(url)
    print('request recieved')
    soup = bs4.BeautifulSoup(res.text)
    parsePage(soup, url)
    a_list = soup.find_all('a')
    #print ('length of anchor list is')
   # print(len(a_list))
    rel_movie_links = set()
    for anchor in a_list:
        if (anchor.has_attr('href')):
            url = anchor['href']
    #        print(url)
            if (url.find('/title/tt') == 0):
                url = url.split("?")[0];
                url = "/".join(url.split('/')[:3])
                rel_movie_links.add('http://www.imdb.com'+url);
    return rel_movie_links

count = 0;
movie_links = list(process_request('http://www.imdb.com'))
i = 0
while i < len(movie_links):
    
    temp = process_request(movie_links[i])
    if (len(movie_information) > 25):
        break;
    for j in temp:
        if (j not in movie_links):
            movie_links.append(j)
    i = i + 1

            





