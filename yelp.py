import requests
from bs4 import BeautifulSoup

base_site = "http://www.yelp.com"

def get_info(query):
    #search for keywords pass in 'query' on yelp.com
    r = requests.get(query)
    soup = BeautifulSoup(r.content, "html.parser")
    all_results = soup.find_all("span", {"class": "indexed-biz-name"})
    first_result = all_results[0].find("a", {"class": "biz-name js-analytics-click"})
    #go to the listing for the first search result
    first_listing = BeautifulSoup(requests.get(base_site + first_result.get("href")).content,"html.parser")
    #fill dict with info from html
    info = {}
    info['name'] = first_result.text.encode("utf-8").replace("&#8217", "'")
    try:
        info['street_address'] = first_listing.find("span", {"itemprop": "streetAddress"}).text
    except:
        pass
    try:
        info['locality'] = first_listing.find("span", {"itemprop": "addressLocality"}).text
    except:
        pass
    try:
        info['region'] = first_listing.find("span", {"itemprop": "addressRegion"}).text
    except:
        pass
    try:
        info['postal_code'] = first_listing.find("span", {"itemprop": "postalCode"}).text
    except:
        pass
    try:
        info['phone'] = first_listing.find("span", {"class": "biz-phone"}).text.strip()
    except:
        pass
    try:
        info['website'] = first_listing.find("div", {"class": "biz-website"}).find("a").text
    except:
        pass
    info['hours'] = []
    # Hours, complex lists
    for item in first_listing.find("div", {"class": "ywidget biz-hours"}).find_all("tr"):
        try:
            day = (item.find("th", {"scope": "row"}).text)
            start_time = item.find("span", {"class": "nowrap"}).text
            end_time = item.find_all("span", {"class": "nowrap"})[1].text
            info['hours'].append((day + ": " + start_time + " - " + end_time).encode("ascii"))
        except:
            pass
    return info

def build_query(search_info):
    query_list = []
    query = base_site + "/search?"
    for item in search_info:
        query_list.append(query + "find_desc=" + item[0].replace(" ", "%20") + "&find_loc=" + item[1].replace(" ", "%20"))
    return query_list

def build_searches(filename, loc):
    in_file = open(filename, 'r')
    searches = []
    for biz in in_file:
        searches.append([biz.replace("\n", ""), loc])
    in_file.close()
    return searches
        


query_list = build_query(build_searches("yelp_list1.txt", "44906"))
for query in query_list:
    result = get_info(query)
    for item in result:
        if not type(result[item]) is list:
            print str(item) + ": " + result[item]
        else:
            print str(item) + ":"
            for time in result[item]:
                print "  " + time
