import urllib.request as request
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import write_dot
from bs4 import BeautifulSoup
from re import match

def find_link(soup):
	for paragraph in soup.find(id='mw-content-text').find_all('p'):
		for link in paragraph.find_all('a'):
			href = link.get('href')
			if match('/wiki/[A-Za-z0-9\(\)_]*$', href) is not None:
				return href

def page_label(page):
	return page[6:]

def populate_graph():
	base_link = 'https://en.wikipedia.org'
	next_page = '/wiki/Freddie_Mercury'
	prev_page = None

	while next_page is not None and page_label(next_page) not in G.nodes:
		G.add_node(page_label(next_page))
		if prev_page is not None:
			G.add_edge(page_label(prev_page), page_label(next_page)) 
		with request.urlopen(base_link + next_page) as response:
			html = response.read()
		soup = BeautifulSoup(html, 'html.parser')

		prev_page = next_page
		next_page = find_link(soup)
		print(next_page)
	
	G.add_edge(page_label(prev_page), page_label(next_page))

G = nx.DiGraph()

populate_graph()
pos = nx.nx_agraph.graphviz_layout(G)
nx.draw(G, pos=pos)
write_dot(G, 'file.dot')
