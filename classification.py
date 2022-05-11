import copy

import numpy
import math

# Returns the target values by the splitting column
def getXAndLabels(xs, ys, splitter):
    buckets = dict()
    splitterVals = [item[splitter] for item in xs]
    # print(splitterVals)
    # splitterVals = set(splitterVals)
    for value in splitterVals:
        buckets[value] = list()
    for i in range(len(xs)):
        buckets[xs[i][splitter]].append(ys[i])

    return buckets


# These are suggested helper functions
# You can structure your code differently, but if you have
# trouble getting started, this might be a good starting point

# Create the decision tree recursively
def make_node(previous_ys, xs, ys, columns):
    # WARNING: lists are passed by reference in python
    # If you are planning to remove items, it's better 
    # to create a copy first
    columns = columns[:]
    xsCopy = copy.deepcopy(xs)
    # print('Columns:', columns)
    # print('xs:', xsCopy)
    # print('ys:', ys)

    # First, check the three termination criteria:

    # If there are no rows (xs and ys are empty): 
    #      Return a node that classifies as the majority class of the parent

    if len(xs) == 0 and len(ys) == 0:
        return {"type": "class", "class": previous_ys}
    
    # If all ys are the same:
    #      Return a node that classifies as that class
    elif len(set(ys)) == 1:
        return {"type": "class", "class": ys[0]}
    
    # If there are no more columns left:
    #      Return a node that classifies as the majority class of the ys

    elif len(columns) == 0:
        return {"type": "class", "class": majority(ys)}



    # Otherwise:
    # Compute the entropy of the current ys

    ent = entropy(ys)
    gains = list()
    # For each column:
    # Must do list(range(len())) because the columns used are preserved, but the program gets tripped up if we don't use
    # a column range starting at 0
    for column in list(range(len(columns))):
        # Getting a dictionary of all the items in the specified column ordered by their label
        splittingVals = getXAndLabels(xsCopy, ys, column)
        # print(splittingVals)

        # Calculating the entropy of each column's values
        totalEntropy = 0
        for val in splittingVals.values():
            # print('Entropy:', entropy(val))
            totalEntropy += (len(val) / len(ys)) * entropy(val)
        # print('Total entropy:', totalEntropy)

        # Storing the information gain from each column
        gains.append(ent - totalEntropy)
    # print(gains)
    split = gains.index(max(gains))
    splitValue = columns[split]
    # print('Splitting on', split)

    # Separating xsCopy into lists with the same split value
    splitterVals = [item[split] for item in xsCopy]
    # print('splitterVals:', splitterVals)

    # Value populated in following loop that is the set of nodes on the lower level
    children = {}
    del(columns[split])
    childNames = set(splitterVals)
    # print(childNames)
    newXsList = list()
    for name in childNames:
        newXs = list()
        newYs = list()
        for i in range(len(splitterVals)):
            # print(xs[i])

            if splitterVals[i] == name:
                # print('Before del operation, xs is:', xs)
                del (xsCopy[i][split])
                # print('After del operation, xs is:', xs)
                newXs.append(xsCopy[i])
                newYs.append(ys[i])
        # print('New Xs:', newXs)
        # print('New Ys:', newYs)
        children[name] = make_node(ys, newXs, newYs, columns)
        newXsList.append(newXs)

    return {
                "type": "split",
                "split": splitValue,
                "children": children
            }
    #     Perform a split on the values in that column 
    #     Calculate the entropy of each of the pieces
    #     Compute the overall entropy as the weighted sum 
    #     The gain of the column is the difference of the entropy before

    #        the split, and this new overall entropy 
    # Select the column with the highest gain, then:
    # Split the data along the column values and recursively call 
    #    make_node for each piece 
    # Create a split-node that splits on this column, and has the result 
    #    of the recursive calls as children.
    
    # Note: This is a placeholder return value

    
    

# Determine if all values in a list are the same 
# Useful for the second basecase above
def same(values):
    if not values: return True
    # if there are values:
    # pick the first, check if all other are the same
    if len(set(values)) == 1:
        return True
    return False


    
# Determine how often each value shows up 
# in a list; this is useful for the entropy
# but also to determine which values is the 
# most common
def counts(values):

    # placeholder return value 
    return {}
   

# Return the most common value from a list 
# Useful for base cases 1 and 3 above.
def majority(values):
    counter = 0
    mostCommon = values[0]

    for value in values:
        frequency = values.count(value)
        # If the count of this item is larger than the previous most common item, we save the count and the value
        if(frequency > counter):
            counter = frequency
            mostCommon = value

    return mostCommon
    
    
# Calculate the entropy of a set of values 
# First count how often each value shows up 
# When you divide this value by the total number 
# of elements, you get the probability for that element 
# The entropy is the negation of the sum of p*log2(p) 
# for all these probabilities.
def entropy(values):
    total = 0
    valSet = set(values)
    for value in valSet:
        p = values.count(value)/len(values)
        total += p * math.log(p, 2)
    # placeholder return value
    return -total

# This is the main decision tree class 
# DO NOT CHANGE THE FOLLOWING LINE
class DecisionTree:
# DO NOT CHANGE THE PRECEDING LINE
    def __init__(self, tree={}):
        self.tree = tree
    
    # DO NOT CHANGE THE FOLLOWING LINE    
    def fit(self, x, y):
    # DO NOT CHANGE THE PRECEDING LINE
        self.majority = majority(y)
        self.tree = make_node(y, x, y, list(range(len(x[0]))))
        
    # DO NOT CHANGE THE FOLLOWING LINE    
    def predict(self, x):
    # DO NOT CHANGE THE PRECEDING LINE    
        if not self.tree:
            return None


        predictions = list()
        for value in x:
            predictions.append(self.predictDriver(self.tree, value))
        return predictions
        # To classify using the tree:
        # Start with the root as the "current" node
        # As long as the current node is an interior node (type == "split"):
        #    get the value of the attribute the split is performed on 
        #    select the child corresponding to that value as the new current node 
        
        # NOTE: In some cases, your tree may not have a child for a particular value 
        #       In that case, return the majority value (self.majority) from the training set 
        
        # IMPORTANT: You have to perform this classification *for each* element in x 
        
        # placeholder return value
        # Note that the result is a list of predictions, one for each x-value
    def predictDriver(self, tree, x):
        if tree['type'] == 'split':
            try:
                return self.predictDriver(tree['children'][x[0]], x[1:])
            except KeyError:
                return self.majority
        elif tree['type'] == 'class':
            return tree['class']
    
    # DO NOT CHANGE THE FOLLOWING LINE
    def to_dict(self):
    # DO NOT CHANGE THE PRECEDING LINE
        # change this if you store the tree in a different format
        return self.tree
       