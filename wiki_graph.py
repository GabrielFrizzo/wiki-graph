import urllib.request as request
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import write_dot
from bs4 import BeautifulSoup
from re import match

BASE_LINK = 'https://en.wikipedia.org'

def valid_link(link):
	if match('/wiki/[A-Za-z0-9\(\)_]*$', link) is not None:
		return True
	return False

def find_links(current_page):
	with request.urlopen(BASE_LINK + current_page) as response:
		html = response.read()
	soup = BeautifulSoup(html, 'html.parser')

	for paragraph in soup.find(id='mw-content-text').find_all('p'):
		return [link for link in paragraph.find_all('a') if valid_link(link)]

def page_label(page):
	return page[6:]

def add_page(depth, curr_page, prev_page = None):
	G.add_node(page_label(curr_page))
	if prev_page is not None:
		G.add_edge(page_label(prev_page), page_label(curr_page))

	if depth > 0:
		for next_page in find_links(curr_page):
			print(curr_page, next_page)
			add_page(depth-1, next_page, curr_page) 


def populate_graph():
	first_page = '/wiki/Freddie_Mercury'

	add_page(1, first_page)

G = nx.DiGraph()

populate_graph()
pos = nx.nx_agraph.graphviz_layout(G)
nx.draw(G, pos=pos)
write_dot(G, 'file.dot')
