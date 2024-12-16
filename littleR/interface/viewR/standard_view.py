from django.http import HttpRequest
from django.template import loader

from littleR.tree import Tree
from littleR.standard import Standard
class StdView(Standard):

    @staticmethod
    def toc_tree(request, tree, max_depth):
        # verify the input
        if not isinstance(request, HttpRequest):
            raise TypeError("The request must be an HttpRequest.")
        if not isinstance(tree, Tree):
            raise TypeError("The standard must be a Standard.")
        if not isinstance(max_depth, int):
            raise TypeError("The max depth must be an integer.")
        if max_depth <= 0:
            raise ValueError("The max depth must be a positive integer.")

        toc_template = loader.get_template("viewR/toc_item.html")


        #start with the top
        tree_top = tree.top()
        view = []
        depth = 1
        for i,req in enumerate(tree_top):
            idx = str(i+1)
            view.append( toc_template.render({"depth": depth, 'req':req, 'idx':idx}, request) )
            for i,child in enumerate(tree.children(req)):
                child_idx = idx+"."+str(i+1)
                view.extend( StdView._toc_tree_child(request, toc_template,  tree, child,child_idx, depth+1, max_depth) )

        return view

    @staticmethod        
    def _toc_tree_child(request, template, tree, req,idx, depth, max_depth):
        # input verified elsewhere
        
        # handle the trivial case
        if depth > max_depth:
            return []
        
        view = []


        # render the child
        view.append( template.render({"depth": depth, 'req':req, 'idx':idx}, request) )

        # keep going down recursively        
        for i,child in enumerate(tree.children(req)):
            child_idx = idx+"."+str(i+1)
            view.extend( StdView._toc_tree_child(request, template,  tree, child,child_idx, depth+1, max_depth))
    
        return view