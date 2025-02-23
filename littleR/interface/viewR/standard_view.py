from django.http import HttpRequest
from django.template import loader

from .models import Standard_Model as Std
from littleR.tree import Tree
from littleR.tree_filter import TreeFilter
from littleR.standard import Standard

class StdView(Standard):

    @staticmethod
    def toc(request, max_depth, pdf=False):
        # verify the input
        if not isinstance(request, HttpRequest):
            raise TypeError("The request must be an HttpRequest.")
        if not isinstance(max_depth, int):
            raise TypeError("The max depth must be an integer.")
        if max_depth <= 0:
            raise ValueError("The max depth must be a positive integer.")
        if not isinstance(pdf, bool):
            raise TypeError("The pdf flag must be a boolean.")
        
        # the template depends on the pdf flag
        if pdf:
            toc_item_template = loader.get_template("viewR/pdf_toc_item.html")
        else:
            toc_item_template = loader.get_template("viewR/toc_item.html")
        
        # get the tree data
        tree = Tree( Std.model(), TreeFilter({})) # no filter for now

        #start with the top
        tree_top = tree.top()
        view = []
        depth = 1
        for i,req in enumerate(tree_top):

            idx = str(i+1)
            view.append( toc_item_template.render({"depth": depth, 'req':req, 'idx':idx}, request) )

            for i,child in enumerate(tree.children(req)):
                child_idx = idx+"."+str(i+1)
                view.extend( StdView._toc_tree_child(request, toc_item_template,  tree, child,child_idx, depth+1, max_depth) )

        # toc
        toc_template = loader.get_template("viewR/toc.html")
        toc_content = { "toc_list": view }
        if pdf:
            toc_content["header"]= "Table of Contents"
        toc_html = toc_template.render(toc_content, request)

        return toc_html

    @staticmethod
    def summary(request, max_depth, pdf=False):
        # verify the input
        if not isinstance(request, HttpRequest):
            raise TypeError("The request must be an HttpRequest.")
        if not isinstance(max_depth, int):
            raise TypeError("The max depth must be an integer.")
        if max_depth <= 0:
            raise ValueError("The max depth must be a positive integer.")
        if not isinstance(pdf, bool):
            raise TypeError("The pdf flag must be a boolean.")

        # the template depends on the pdf flag
        if pdf:
            summary_item_template = loader.get_template("viewR/pdf_summary_item.html")
        else:
            summary_item_template = loader.get_template("viewR/summary_item.html")

        # get the tree data
        tree = Tree( Std.model(), TreeFilter({})) # no filter for now

        #start with the top
        tree_top = tree.top()
        view = []
        depth = 1
        for i,req in enumerate(tree_top):

            idx = str(i+1)
            view.append( summary_item_template.render({'depth': depth, 'depth_plus': depth+1, 'req':req, 'idx':idx}, request) )

            for i,child in enumerate(tree.children(req)):
                child_idx = idx+"."+str(i+1)
                view.extend( StdView._sum_tree_child(request, summary_item_template,  tree, child,child_idx, depth+1, max_depth) )

        # summary
        summary_template = loader.get_template("viewR/summary.html")
        summary_content = { "sum_list": view }
        if pdf:
            summary_content["header"]= "Requirements Summary"
        summary_html = summary_template.render(summary_content, request)

        return summary_html


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
    
    @staticmethod        
    def _sum_tree_child(request, template, tree, req, idx, depth, max_depth):
        # input verified elsewhere
        
        # handle the trivial case
        if depth > max_depth:
            return []
        
        view = []

        # render the child
        view.append( template.render({"depth": depth, 'depth_plus': depth+1, 'req':req, 'idx':idx}, request) )

        # keep going down recursively        
        for i,child in enumerate(tree.children(req)):
            child_idx = idx+"."+str(i+1)
            view.extend( StdView._sum_tree_child(request, template,  tree, child, child_idx, depth+1, max_depth) )
    
        return view