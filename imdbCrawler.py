__author__ = 'mayankkush'
import requests, bs4, json, pprint, csv, traceback
from csv import DictWriter

site_url = "http://www.imdb.com"
universaldata = {}
mynewlist = {}
list = []
noofrecords=5000
limit=10
ittr=0

def writeToFile():
    with open('mycsvfile.csv', 'w') as f:  # Just use 'w' mode in 3.x
        for i in universaldata:

            data=universaldata[i]
            #header=next(csv.reader(f))
            w = csv.DictWriter(f, data.keys())

            if(i==2):
                w.writeheader()
            w.writerow(data)
            #f.close()

try:
    def getImdb(url, iterator,count):
        global ittr
        print("Loading data for entry "+str(iterator))
        data = {}  # stores current values of data
        r = requests.get(url)  # sends get request from the url
        if str(r)=="<Response [200]>":
            soup = bs4.BeautifulSoup(r.text, 'lxml')  # parsing the text as xml
            url_list = soup.find_all('a')  # lists all <> with anchor tags

            genre = []
            # sample url http://www.imdb.com/title/tt3715320/?ref_=hm_otw_t2
            id=""
            try:
                id = soup.find('link', {'rel': 'canonical'})['href'].split('/')[4]  # finds the id of the movie
            except(Exception):
                print("unable to get id")
            tempList = soup.find_all('h1', {'class': 'header'})  # header h1 contains title and year
            title=""
            year=""
            try:
                title = tempList[0].find('span', {
                'class': 'itemprop'}).text  # extracts title from templist, tempist[0] is first occurance in header

            except(Exception):
                print("Title not specified")
            try:year = tempList[0].find('a').text
            except(Exception):
                print("Year not specified")
            rating=""
            try:
                rating = soup.find('div', {'class': 'titlePageSprite star-box-giga-star'}).text  # extract rating from the class
            except(Exception):
                print("No ratings found")
            poster_src=""
            try:
                poster_src = soup.find('img', {'itemprop': 'image'})[
                    'src']  # value of source tag in img, contains poster of the movie
            except(Exception):
                print("No poster found")
            description=""
            try:
                description = soup.find_all('p', {'itemprop': 'description'})[0].text
            except(Exception):
                print("No description found")
            genrelist = soup.find_all('span', {'itemprop': 'genre'})
            for i in genrelist:
                try:
                    genre.append(i.text)
                except(Exception):
                    print("Genre not specified")


            director_name = []

            for link in url_list:
                if link.has_attr('href'):  # checks if link has attribute href
                    if len(link['href'].split('/')) > 3:  #checks if link has 3 parts

                        if link['href'].split('/')[3] == "?ref_=tt_ov_dr":  #if the link is director of movie
                            try:
                                director_name.append(link.find('span').text)
                            except(Exception):
                                print("Director not specified")

                        if link['href'].split('/')[3] == "?ref_=tt_rec_tti":  #if link is of another movie
                            abc=link['href'].split('/')[2]
                            if mynewlist.__contains__(
                                    (str(abc))):  #if is already in list or has been visited
                                continue
                            else:
                                mynewlist[str(abc)] = site_url + link[
                                    'href']  #adds link with a unique hascode for future references
                                list.append(site_url + link[
                                    'href'])  #adds link to the list of link of new movies as dict.values() does not support iteration by index

            #Example - my_list = ["Hello", "world"]
            #print "-".join(my_list)
            # Produce: "Hello-world"
            data['id'] = id
            data['title'] = title
            data['year'] = year
            data['director'] = ",".join(director_name)
            data['genre'] = ",".join(genre)
            data['rating'] = rating
            data['description'] = description
            data['poster'] = poster_src

            universaldata[iterator+1] = data  # universal data contains key value pair for movie and id, used only for print checking

            if count >= limit:  # if change value to get data for no of movies.
                #pprint.pprint(universaldata)  #preety prints nothing else
                return
            else:
                ittr=ittr+1
                try:getImdb(list[iterator], iterator+1,count+1)  # calls with next link in the list

                except(Exception):
                    traceback.print_exc()
                    print("UnExpected Error. Saving data to file...")
                    return


        else:
            print("cannot connect to link "+list[iterator])
            ittr=ittr+1
            getImdb(url,iterator+1,count)




    lowerBound=ittr
    upperBound=ittr+10
    a=1;
    list.append("http://www.imdb.com/title/tt0111161/?ref_=chttp_tt_1")
    while(upperBound<noofrecords+10):
        print("iteration "+str(a))

        getImdb(list[lowerBound], lowerBound+1,1)
        a+=1
        lowerBound=upperBound
        upperBound=upperBound+10
except(KeyboardInterrupt):
    print("Unexpected Termination, Saving Loaded Data in file...")
except(BaseException):
    print("Ye to samajh se pare ho lio")
finally:
    try:writeToFile()
    except(IOError):
        pprint("OH!!! You Are Doomed....")







