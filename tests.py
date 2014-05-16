import unittest
from paper import Paper, BFS, PaperBFS

class BFSTest(unittest.TestCase):

    def test_simple_bfs_with_cycle(self):
        # Graph Layout
        #  2 - 5
        #  |   |
        #  1 - 3 - 6
        #  |
        #  4
        graph_ = { '1': ['2', '3', '4'],
                   '2': ['1', '5'],
                   '3': ['1', '5', '6'],
                   '4': ['1'],
                   '5': ['2', '3'],
                   '6': ['3']
               }
        result = BFS(graph=graph_, start_node='1')
        traversal_order = result._visited
        expected_traversal_order = ['1', '2', '3', '4', '5', '6']
        self.assertEquals(traversal_order, expected_traversal_order)

        result = BFS(graph=graph_, start_node='3')
        traversal_order = result._visited
        expected_traversal_order = ['3', '1', '5', '6', '2', '4']
        self.assertEquals(traversal_order, expected_traversal_order)

        result = BFS(graph=graph_, start_node='6')
        traversal_order = result._visited
        expected_traversal_order = ['6', '3', '1', '5', '2', '4']
        self.assertEquals(traversal_order, expected_traversal_order)
        
    def test_bfs_no_start_node(self):

        self.assertRaises(ValueError, BFS)

    def test_paper_bfs(self):
        
        paper = Paper(id_='A00-1031', 
                      title='TnT - A Statistical Part-Of-Speech Tagger',
                      year='2000', link_type='outgoing')
        paper.outgoing_citations = [
            Paper(id_='A92-1018', title='A Practical Part-Of-Speech Tagger', 
                  year='1992'),
            Paper(id_='A97-1014', 
                  title='An Annotation Scheme For Free Word Order Languages',
                  year='1997'),
            Paper(id_='J93-2004',
                title='Building A Large Annotated Corpus Of English: '\
                  'The Penn Treebank', year='1993'),
            Paper(id_='P98-1081', title='Improving Data Driven Wordclass '\
                  'Tagging by System Combination', year='1998'),
            Paper(id_='W96-0102', title='MBT: A Memory-Based Part Of Speech '\
                  'Tagger-Generator', year='1996'),
            Paper(id_='W96-0213', title='A Maximum Entropy Model For '\
                  'Part-Of-Speech Tagging', year='1996')
        ]
        result = PaperBFS(start_node=paper, iterations=1)
        for p in paper.outgoing_citations:
            for paper in result._visited:
                if p.id_ == paper.id_:
                    self.assertEquals(p.title, paper.title)

if __name__ == '__main__':
    unittest.main()
