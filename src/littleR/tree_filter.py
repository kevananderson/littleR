import os
from littleR.requirement import Requirement

class TreeFilter():
    """A filter to tell us how to build a tree of requirements.
    
    Attributes:
        customer (str): The customer of the requirements. Without this,
            the tree will not include customer requirements. At most one 
            customer can be specified.
        label (set): The labels of the requirements. Any group of children
            with no labels will be included. If the filter has the matching
            label, the child will be included. If a child has a label but it
            does not include the listed label, it will not be included.
        not_label (set): The labels that the requirements should not have.
            Any group of children with the not_label listed will be excluded.
    """

    def __init__(self, filter_config):
        # verify the input
        if not isinstance(filter_config, dict):
            raise TypeError("The filter configuration must be a dictionary.")
        
        # customer
        customer = filter_config.get("customer", "")
        if not isinstance(customer, str):
            raise TypeError("The customer must be a string.")
        #TODO: verify that the customer is valid.
        self._customer = customer.lower()

        # label
        self._label = set()
        label = filter_config.get("label", set())
        if not isinstance(label, set):
            raise TypeError("The label must be a set.")
        for l in label:
            if not isinstance(l, str):
                raise TypeError("The label must be a list of strings.")
            self._label.add(l.lower())
        
        # not label
        self._not_label = set()
        not_label = filter_config.get("not_label", set())
        if not isinstance(not_label, set):
            raise TypeError("The not_label must be a set.")
        for l in not_label:
            if not isinstance(l, str):
                raise TypeError("The not_label must be a list of strings.")
            self._not_label.add(l.lower())

        # verify that the label and not_label do not overlap
        for l in self._label:
            if l in self._not_label:
                raise ValueError("The label and not_label must not overlap.")
        
        # component
        self._component = filter_config.get("component", "")
        if not isinstance(self._component, str):
            raise TypeError("The component must be a string.")
        
    def top(self, req):
        """Return True if the requirement is a top level req.

        A top level requirement is one that:
        - The length of the parents is 0 and req is in the product or customer set.
        - All of the parents are customers that do not match the customer filter.
        """
        if len(req.parent) == 0 and self.project_or_customer(req):
            return True
        
        for parent in req.parent:
            if self.project_or_customer(parent):
                return False

        return True
        
    def project_or_customer(self,req):
        """Return true if the requirement is project or matching customer."""
        
        return self.project(req) or self.customer(req)
    
    def project(self,req):
        """Return True if the requirement is not a customer requirement."""
        if req.type != "customer":
            return True
        return False
    
    def customer(self,req):
        """Return True if the requirement is a matching customer requirement."""
        if req.type != "customer":
            return False
        file_name = os.path.basename(req.path())
        customer = os.path.splitext(file_name)[0]
        return self._customer == customer

    def label(self, req):
        """Return True if the requirement has a matching label."""
        for l in req.label:
            if l in self._label:
                return True
        return False
        
    def not_label(self, req):
        """Return True if the requirement does not match a not_label."""
        for l in req.label:
            if l in self._not_label:
                return False
        return True
    
    def component(self, req):
        """Return True if the requirement is in the component.
        
        Something is part of the component if it:
        - Has the component.
        - One of its parents, recursive, is part of the component.
        - It is not part of another component.
        """
        if self._component == req.component:
            return True
        parents = req.parent
        while len(parents) > 0:
            parent = parents.pop()
            if self._component == parent.component:
                return True
            if parent.component != "": #matches any component not in the filter
                return False
            parents.extend(parent.parent())
        return False


    @staticmethod
    def has_label(req, labels):
        """Return True if the requirement has a label in the list.
        
        Args:
            req (Requirement): The requirement to check.
            labels (list): The list of labels to check. Should be lower case.
        """

        for l in req.label:
            if l in labels:
                return True
        return False

    def __str__(self):
        return "TreeFilter: customer: {}, label: {}, not_label: {}".format(
            self._customer, self._label, self._not_label)
    
    def __repr__(self):
        # do we have a customer
        cu = 0
        if self._customer != "":
            cu = 1
        
        # do we have a label or not?
        label = len(self._label)
        not_label = len(self._not_label)

        #do we have a component
        co = 0
        if self._component != "":
            co = 1

        return f"TreeFilter: cu[{cu}], l[{label}], nl[{not_label}], co[{not_label}]"
    