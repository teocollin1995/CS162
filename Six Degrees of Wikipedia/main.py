import networkx as nx
import sys
import requests
from bs4 import BeautifulSoup
from collections import deque

toSort = True

wikgraph = nx.DiGraph()

arg1 = sys.argv[1]
arg2 = sys.argv[2]


def page_eval_sort(links):
    look_for = ((arg2.replace('/wiki/','').replace('(','').replace(')','')).split('_')) + ['list' ]
    pre_sort = [[0,x] for x in links]
    for x in look_for:
        for y in pre_sort:
            if x in y[1]:
                y[0] = y[0] + 1

    pre_sort.sort(key=lambda a: a[0])
    return [x[1] for x in pre_sort]


def get_wiki_page_soup(old):
    new = 'https://en.wikipedia.org' + old
    print(new)
    r = requests.get(new)
    print(r)
    if r.status_code == 404:
        print(old + " 404'd")
        return()
    return BeautifulSoup(r.text)


def get_all_page_urls(soup):
    a = soup.find_all('a')
    rawa = [x.get('href') for x in a]
    rawn = [x for x in rawa if x is not None and 'org' not in x and '/wiki/' in x and ':' not in x and 'Main_Page' not in x]
    return rawn


def tree_append(page):
    print("page: " + page)
    soup = get_wiki_page_soup(page)
    newpages = get_all_page_urls(soup)
    print(newpages)
    wikgraph.add_edges_from([(page, x) for x in newpages if x not in wikgraph.nodes_iter()])
    if toSort:
        return page_eval_sort(newpages)
    return newpages


def tree_construct_search_breadth_limited(page1, page2):
    que = deque([page1])
    while que:
        considering = que.pop()
        print(considering)
        new = tree_append(considering)
        if page2 in new:
            print("Done!")
            print("Path:")
            print(nx.shortest_path(wikgraph, arg1, arg2))
            sys.exit(0)
        print("Extending")
        que.extendleft(new)


tree_construct_search_breadth_limited(arg1, arg2)

