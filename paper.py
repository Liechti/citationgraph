 # -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import deque
import urllib
from bs4 import BeautifulSoup
import time, random

class BFS(object):
    '''
    Classic BFS algorithm, with an iterations parameter to stop it early.
    '''
    def __init__(self, graph=None, start_node=None, iterations=None):
        self.graph = graph
        self.iterations = iterations
        if start_node is None:
            raise ValueError('BFS must have a start node.')
        self.start_node = start_node
        self._visited = []
        self._traverse()

    def _traverse(self):
        self.queue = deque()
        self.queue.append(self.start_node)
        self._visited.append(self.start_node)
        while len(self.queue) > 0:
            if self._should_exit_early():
                break
            node = self.queue.popleft()
            for child in self._get_children(node):
                if isinstance(child, str):
                    if child not in self._visited:
                        self._visited.append(child)
                        self.queue.append(child)
                else:
                    seen = [n.id_ for n in self._visited]
                    if child.id_ not in seen:                
                        self._visited.append(child)
                        self.queue.append(child)
                    
    def _get_children(self, node):
        return self.graph[node]

    def _should_exit_early(self):
        if self.iterations is not None:
            if self.iterations == 0:
                return True
            self.iterations -= 1
        return False


class PaperBFS(BFS):
    '''
    A Paper-specific BFS. Overrides the _get_children method to crawl
    the links for incoming and outcoming citations.
    '''
    def _get_children(self, node):
        print 'this is node:', node.id_, node.title
        time.sleep(random.randint(4,15))
        page = urllib.urlopen(node.outgoing_link)
        return self._parse_html(page.read())
        
    def _parse_html(self, html):
        papers = []
        soup = BeautifulSoup(html)
        for row in soup.find_all('tr'):
            cells = [cell for cell in row.find_all('td')]
            if len(cells) == 3:
                id_ = cells[0].a.text
                title = cells[1].a.text
                year = cells[2].div.text
                print id_
                papers.append(Paper(id_, title, year))
        print 'Here are children', len(papers)
        return papers 
                
class Paper(object):

    urlbase = 'http://clair.eecs.umich.edu/aan/'

    def __init__(self, id_, title, year):
        self.id_ = id_
        self.title = title
        self.year = year
        self.outgoing_link = Paper.urlbase + 'outgoing_citations.php?paper_id='+\
                             self.id_
        self.incoming_link = Paper.urlbase + 'incoming_citations.php?paper_id='+\
                             self.id_
        self.incoming_citations = []
        self.outgoing_citations = []


if __name__ == '__main__':
    #paper = Paper(id_='A00-1031', 
    #            title='TnT - A Statistical Part-Of-Speech Tagger',
    #              year='2000')
    paper = Paper(id_='D10-1007', title='', year='')
    result = PaperBFS(start_node=paper)
    for paper in result._visited:
        print paper.year, ':', paper.id_
    print len(result._visited), 'papers'