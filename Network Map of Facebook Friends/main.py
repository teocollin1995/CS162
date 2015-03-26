from urllib2 import URLError
import mechanize
import cookielib
from bs4 import BeautifulSoup
import re
import networkx as nx
import pygraphviz
from random import randint
from time import sleep
import unicodedata
from unidecode import unidecode
from itertools import chain

graph = nx.Graph()
br = mechanize.Browser() # set up browser

# sets up cookie handling
br.set_handle_robots(False)
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)


br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True) # The three are to do deal with login redirects


br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')] # set browser id
br.open('https://m.facebook.com/') # gets us to the login page
br.select_form(nr=0)

your_username = '' # set it
your_password = ''  # set it

def print_response(br):
    """
    :argument mechanize browser
    :return None

    Prints the text of a mechanize page in raw html
    """
    print br.response().read()
    return ()


def login(email, password, br):
    """
    :argument: string for email, string for password, and mechanize browser
    :return None
    Logins into Facebook
    """
    br.form['email'] = email
    br.form['pass'] = password
    br.submit()


def say_yes_basic(br):
    """
    :argument mechanize browser
    :return None
    Hits a simple continue button

    """
    br.form = list(br.forms())[0]
    control = br.form.find_control("submit[Continue]")
    br[control.name]
    br.submit()


def say_this_is_okay(br):
    """
    :argument Mechanize browser
    :return None
    Hits a simple submit This is Okay button
    """
    br.form = list(br.forms())[0]
    control = br.form.find_control("submit[This is Okay]")
    br[control.name]
    br.submit()


def control_something(br, something):
    """
    :argument Mechanize browser, string with name of a control
    Hits the stated control
    """
    br.form = list(br.forms())[0]
    control = br.form.find_control(something)
    br[control.name]


# cite http://www.pythonforbeginners.com/cheatsheet/python-mechanize-cheat-sheet


def control_explore(br):
    """
    :argument Mechanize browser
    :return None
    Prints the list of controls

    """
    br.form = list(br.forms())[0]
    for form in br.forms():
        print form
    for control in br.form.controls:
        print (control, control.type, control.name, br[control.name])

def request_to_soup(br):
    """
    :argument A mechanize browser
    :return None
    Takes the current mechanize browser and turns its raw html in to a bs4 object

    """
    try:
        return (BeautifulSoup(br.response().read()))
    except AttributeError:
        print "Nonetype for response"
        print(br.geturl())
        print (br.get_data())
        br.open(br.geturl())
        print "Trying again"
        return (BeautifulSoup(br.response().read()))



def ncontrols(br):
    """
    :argument Mechanize Browser
    :return A list of controls

    """
    br.form = list(br.forms())[0]
    return [control.name for control in br.form.controls]


def go_to_profile(br, name):
    """
    :argument A mechanize browser, a text arguemt such as a user uid or profile name
    :returns None
    Takes the browser to a specific profile

    """
    print name
    sleep(randint(1,20))
    print "going"
    try:
        br.open('https://m.facebook.com/' + name)
    except URLError:
        print "Wifi lost, trying again"
        sleep(randint(200,400))
        br.open('https://m.facebook.com/' + name)


def control_control(br):
    """
    :argument A mechanise browser
    :return None
    Loggs into facebook
    """
    soup_response = request_to_soup(br)

    br.form = list(br.forms())[0]
    n = len(ncontrols(br))
    print n
    print soup_response.title.text
    if n > 10:
        print "Bypassed Facebook security"
        return ()
    if soup_response.title.text == "Remember Browser":
        print "not remembering"
        say_yes_basic(br)
        control_control(br)
    if soup_response.title.text == "Review Recent Login": #Two almost identicial options...
        try:
            print "reviewing"
            say_yes_basic(br)
            control_control(br)
        except mechanize.ControlNotFoundError:
            try:
                say_this_is_okay(br)
                control_control(br)
            except mechanize.ControlNotFoundError:
                try:
                    say_yes_basic(br)
                    control_control(br)
                except mechanize.ControlNotFoundError:
                    print "Abnormal security settings"


def go_to_my_friends(br):
    """
    :argument Mechanise browser
    :return None
    Goes to the location where facebook stores your firends i.e the contents of degree one
    """
    br.open('https://m.facebook.com/friends/center/friends/?ref=bookmark')

def get_my_friends(br):
    """
    :argument Mechanise Browser
    :return A list of bs4 objects each corresponding to an entry for a friend
    This may not work based on somethings that I'm not sure of, mainly the class_ = ""
    """
    soup = request_to_soup(br)
    return soup.find_all('div', class_='x e y')  # I have really know idea why facebook decided to use these letters... and it might need to be changed...

def my_friend_to_uid(soup):
    """
    :argument A bs4 object containing a link to your friend... not a friend of a friend
    :return a uid corresponding to the facebook profile that the bs4 object came from

    """
    return re.search('(?<=uid=)[0-9]*', soup.a.get('href')).group(0)
    # gets the UID because the link we are given is a redirect which is annoying to archive

def my_frend_to_name(soup):
    """
    :argument a bs4 object containing a link to your friend, not a friend of a friend
    :return The friend's name

    This is probably unneccesary
    """
    return soup.span.text

def friends_friends_page(br, uid):
    sleep(randint(1,2))
    go_to_profile(br, uid)
    actual_profile_url = br.geturl().replace('?_rdr','')
    print actual_profile_url + '?v=friends&startindex=00'
    sleep(randint(1,10))
    br.open(actual_profile_url + '?v=friends&startindex=00')
    print br.geturl()


def more_friends(br):
    strip = re.compile('=[0-9]*')
    current_url = br.geturl()
    index_location = request_to_soup(br).find_all('div', id="m_more_friends")[0].a.get('href')
    newindex = re.search('(?<=startindex=)[0-9]*', index_location).group(0)
    tempurl = re.sub(strip, '=', current_url)
    newurl = tempurl + newindex
    print newurl
    br.open(newurl)

def print_line(ss):
    for x in range(0,len(ss)):
        print '====================================================================,' + str(x)
        print ss[x]
        print '====================================================================, x'


def is_a_friend(tag):
    a = tag.has_attr('class')
    b = len(tag.find_all('a')) == 2 or len(tag.find_all('a')) == 1
    c = tag.img == None
    d = tag.table == None
    e = not tag.has_attr('id')
    return a and b and c and d and e


def get_friends_of_friends(br):
    soups = request_to_soup(br)
    return filter(is_a_friend, (soups.find_all('div')))

class user_id_keeping:

    def __init__(self):
        self.keeper = []
    def adds(self, records):
        self.keeper += records
    def soup_uid_check(self,soup):
        return (soup.a.get('href').replace('?fref=fr_tab', '').lstrip('/')) in self.keeper
    def uid_check(self, uid):
        return uid in self.keeper

all_uids = user_id_keeping()

def get_rest_friends_of_friends(br, initial_friends):
    soup = request_to_soup(br)
    index_locations = soup.find_all('div', id="m_more_friends")
    # print index_locations
    if len(index_locations) != 0:
        strip = re.compile('=[0-9]*')
        current_url = (br.geturl())
        # print current_url
        index_location = index_locations[0].a.get('href')
        newindex = re.search('(?<=startindex=)[0-9]*', index_location).group(0)
        tempurl = re.sub(strip, '=', current_url)
        newurl = tempurl + newindex
        print newurl
        try:
            br.open(newurl)
        except URLError:
            print "Network problems"
            sleep(randint(150,300))
            try:
                br.open(newurl)
            except URLError:
                sleep(randint(800,1600))
                br.open(newurl)
        initial_friends += get_friends_of_friends(br)
        #print initial_friends
        sleep(randint(0, 2))
        get_rest_friends_of_friends(br, initial_friends)
    return initial_friends




def get_all_friends(br, id):
    friends_friends_page(br, id)
    sleep(randint(1,2))
    return get_rest_friends_of_friends(br, get_friends_of_friends(br))



def friends_graph(br, n, id, name,):
    print ('id is', id)
    print ('name is', name)
    friends_friends = get_all_friends(br, id)
    if friends_friends is None:
        print "Reached End"
    try:
        friends_friends_names = [a1.span.text for a1 in friends_friends if not all_uids.soup_uid_check(a1)]
        friends_friends_ids = [a1.a.get('href').replace('?fref=fr_tab', '').lstrip('/') for a1 in friends_friends if not all_uids.soup_uid_check(a1)]
    except NameError:
        print "Security settings"
        return ()
    except AttributeError:
        print "security settings"
        return ()
    # print friends_friends_ids
    all_uids.adds(friends_friends_ids)
    graph.add_edges_from([(name, a1) for a1 in friends_friends_names])
    #nx.draw(graph)
    #plt.savefig('crap.png')
    nx.write_dot(graph, 'resultst.dot')
    if n - 1 == 0:
        print "Reached End"
        return ()
    map(lambda ids, names: friends_graph(br, (n - 1), ids, names), friends_friends_ids, friends_friends_names)
    print "we have completed" + str(name)
    nx.write_dot(graph, 'temp.dot')






def main():
    profile_name = "set it"
    login('set it', 'set it', br)
    control_control(br)
    go_to_my_friends(br)
    a = get_my_friends(br)
    graph.add_edges_from([(profile_name, a1.span.text) for a1 in a]) # investiage if this is getting blank profile page people
    my_friends_uid = [my_friend_to_uid(a2) for a2 in a]
    all_uids.adds(my_friends_uid)
    my_friends_names = [a1.span.text for a1 in a]
    # print type(my_friends_uid[0])
    # friends_graph(br, 2, my_friends_uid[0], a[0].span.text)
    map(lambda uids, names: friends_graph(br, 2, uids, names), my_friends_uid, my_friends_names)
    print "Just needs to be drawn"
    nx.write_dot(graph, 'results.dot')
    #nx.draw(graph)
    #plt.savefig('crap.png')
    print "done"


#run this once to convert the dotfile
def correct():
    file = open('results.dot','r')
    all = file.read()
    file.close()
    allb = unicode(all, 'utf-8')
    allc = unidecode(allb)
    alla = unicode(allc, 'utf-8')
    b = unicodedata.normalize('NFKD', alla).encode('ascii', 'ignore')
    f = open('try.dot','w')
    f.write(b)

# use this to recover the graph from the converted dot file
def setup():
    A = pygraphviz.AGraph(file='try.dot', encoding='ascii')
    a = nx.DiGraph(nx.from_agraph(A))
    return a

#finds the max centrality of any node
def centrality_max(a):
    print((max(nx.degree_centrality(a).values())))


def friendship_paradox(graph):
    """
    :param graph digraph
    :return returns the average dif between the number of friends that a node has and the average number of friends
    the node's friends have

    """
    for x in graph.nodes():
        graph.node[x]['nf'] = len(graph.successors(x)) # computes number of friends
    for x in graph.nodes():
        graph.node[x]['nff'] = sum([graph.node[z]['nf'] for z in graph.successors(x)]) / (1 + len(graph.successors(x)))
        # computers the average number of friends that one's friends have
    return sum([graph.node[x]['nff'] - graph.node[x]['nf'] for x in graph.nodes()])/len(graph.nodes())
    # returns average dif between the two numbers over all nodes.


def all_sucs_not(graph, start, exclude, n):
    """
    :param graph a digraph
    :start The person you are centering on
    :exclude The person you are excluding, probably where the graph started
    :n depth from start
    :return a list of nodes to be made into a sub graph
    """
    stuff = [x for x in graph.successors(start) if x is not exclude]
    if n == 0:
        return stuff
    else:
        return stuff + list(chain.from_iterable([all_sucs_not(graph, x, exclude, (n-1)) for x in stuff]))


def all_sucs_not_xlist(graph, start, exclude, n):
    """
    :param graph a digraph
    :start The person you are centering on
    :exclude The list of persons you are excluding, probably where the graph started
    :n depth from start
    :return a list of nodes to be made into a sub graph
    """
    stuff = [x for x in graph.successors(start) if x not in exclude ]
    if n == 0:
        return stuff + [start]
    else:
        return stuff + list(chain.from_iterable([all_sucs_not_xlist(graph, x, exclude, (n-1)) for x in stuff]))

def all_sub_graphs(graph, start, depth):
    """
    :param graph a digraph
    :param start the center of the graph or the node you want to have all these graphs link back to
    :depth depth of each from the neighboring nod
    :return a list of all subgraphs

    This function takes a digraph and a start and a depth. It takes the start and finds all the nodes around it. For
    each of those nodes it creates a subgraph going out to the depth specified. It writes a dot file for each of these
    dot files.
    """
    for x in range(0, len(graph.successors(start))):
        results = []
        new = graph.subgraph(all_sucs_not(graph, graph.successors(me)[x], me, depth)) #creates a subgraph
        results.append(new)
        nx.write_dot(new, graph.successors(me)[x] + '.dot') # write it
    return new

def all_sub_graphs_xlist(graph, start, depth):
    """
    Same as above but using lists to exlude
    :param graph a digraph
    :param start the center of the graph or the node you want to have all these graphs link back to
    :depth depth of each from the neighboring nod
    :return a list of all subgraphs

    This function takes a digraph and a start and a depth. It takes the start and finds all the nodes around it. For
    each of those nodes it creates a subgraph going out to the depth specified. It writes a dot file for each of these
    dot files.
    """
    for x in range(0, len(graph.successors(start))):
        results = []
        new = graph.subgraph(all_sucs_not_xlist(graph, graph.successors(me)[x], [me] + graph.successors(me) - graph.successors[x], depth))
        #creates a subgraph
        results.append(new)
        nx.write_dot(new,graph.successors(me)[x] + '.dot') # write it
    return new




#run like this:
#graph = setup()
#me = "Teodoro Fields Collin"
#all_sub_graphs_xlist(graph, me, 2)
#all_sub_graphs(graph, me, 2)
#print friendship_paradox(graph)
#result of this is 495














