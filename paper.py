 # -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import deque
import urllib
from bs4 import BeautifulSoup
import time, random
import json

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
        page = urllib.urlopen(node.link)
        outgoing_citations = self._parse_html(page.read())
        node.outgoing_citations = outgoing_citations
        return outgoing_citations
        
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
        return papers 
                
class Paper(object):

    urlbase = 'http://clair.eecs.umich.edu/aan/'

    def __init__(self, id_, title, year, link_type='outgoing'):
        self.id_ = id_
        self.title = title
        self.year = year
        if link_type == 'outgoing':
            self.link = Paper.urlbase +\
                        'outgoing_citations.php?paper_id=' + self.id_
        if link_type == 'incoming':
            self.link = Paper.urlbase +\
                        'incoming_citations.php?paper_id=' + self.id_
        self.incoming_citations = []
        self.outgoing_citations = []

def to_json(papers):
    '''Writes paper to the following format:
    { paper_id : "",
      title : "",
      year : ""
    }

    Paper citations are represented in an adjaceny list:
    {
      paper_id : "",
      incoming : [ <list of paper ids> ],
      outgoing : [ <list of paper ids> ]
    }
    '''
    out = []
    adjancey_list = []
    for paper in papers:
        out.append({'paper_id': paper.id_, 'title': paper.title, 
                    'year': paper.year })
        adjancey_list.append(
            { 'paper_id': paper.id_,
              'incoming': [p.id_ for p in paper.incoming_citations],
              'outgoing': [p.id_ for p in paper.outgoing_citations]})

    with open("papers.json", 'w') as f:
        json.dump(out, f, indent = 4)
    with open("graph.json", 'w') as f:
        json.dump(adjancey_list, f, indent = 4)

if __name__ == '__main__':
    paper = Paper(id_='D10-1007', title='', year='', link_type='outgoing')
    result = PaperBFS(start_node=paper, iterations=3)
    print len(result._visited), 'papers'
    to_json(result._visited)
