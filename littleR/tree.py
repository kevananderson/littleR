from littleR.standard import Standard
from littleR.tree_filter import TreeFilter
from littleR.requirement import Requirement

class Tree():

    def __init__(self, standard, tree_filter):
        # verify the input
        if not isinstance(standard, Standard):
            raise TypeError("The standard must be a Standard.")
        if not isinstance(tree_filter, TreeFilter):
            raise TypeError("The tree_filter must be a TreeFilter.")
        
        self._standard = standard
        self._tree_filter = tree_filter
    
    def config(self):
        """Return the configuration."""
        return self._standard.config

    def top(self):
        """Return the top of the tree."""
        # find the top of the tree
        tree_top = []
        for req in self._standard.requirements_iter():
            if self._tree_filter.top(req):
                tree_top.append(req)
        return tree_top

    def children(self, req):
        """Return a list of filtered child requirements.
        
        This only filters based on customer, label, and not_label.
        """
        children = []
        matched, unmatched = self._tree_filter.child_labels(req)
        for child in req.child:
            # exclude on customer first
            if not self._tree_filter.project_or_customer(child):
                continue
            
            # find the matching labels if any
            if TreeFilter.has_label(child, matched):
                children.append(child)
                continue
            
            # exclude on unmatched labels
            if TreeFilter.has_label(child, unmatched):
                continue

            # take what has no labels
            children.append(child)

        return children

    def __str__(self):
        return "Tree"
    
    def __repr__(self):
        return "Tree"

