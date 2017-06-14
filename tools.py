import math
import classes


# Functions for read rule based system. <-------------------------------------------------------------------------------
def get_system_objects(system_file):
    """Return numpy array with integers that represent Rule Based System and dictionary to encode true values."""
    system_file.seek(0)  # return to beginning of file
    objects = []
    for line in system_file:
        system_object = line.strip().split(' ')
        objects.append(system_object)
    return objects


# Apriori functions. <--------------------------------------------------------------------------------------------------
def get_id3_tree(labels, system):
    """Return decision tree calculated by ID3 algorithm."""
    decisions = get_count_of_objects(system, -1)  # -1 is decision (one before last)
    system_entropy = get_entropy(decisions)

    nodes = get_nodes(system, labels, system_entropy)
    root = get_root(nodes, labels)
    find_leaves(root, labels)
    find_decisions(root)
    return root


def get_count_of_objects(system, nr_of_attribute):
    """Return values of attribute and number of theirs."""
    decisions = {}
    for decision_object in system:
        attribute_value = decision_object[nr_of_attribute]
        if attribute_value not in decisions:
            decisions[attribute_value] = 1
        else:
            decisions[attribute_value] += 1
    return decisions


def get_entropy(data):
    """Return entropy for values passed in argument."""
    number_of_objects = sum(data.values())
    entropy = 0
    for value in data.values():
        p = value / number_of_objects
        entropy += get_part_of_entropy(p)
    return entropy


def get_part_of_entropy(p):
    """Return part of sum to calculate entropy."""
    return -p*(math.log2(p))


def get_nodes(system, attributes, system_entropy):
    """Return nodes from system."""
    nodes = []
    for key, item in attributes.items():
        node = classes.Node(item, system, system_entropy)
        set_edges(node, key)
        nodes.append(node)
    return nodes


def set_edges(node, index):
    """Set profit in node and add their edges."""
    dictionary_edges = get_count_of_objects(node.data, index)
    for dictionary_edge in dictionary_edges:
        edge = classes.Edge(dictionary_edge, node.data, index, dictionary_edges)
        node.edges.append(edge)
    node.calculate_profit()


def is_edge_leaf(value_decisions):
    if len(value_decisions) == 1:
        return True
    return False


def get_data(system, value, index):
    """Return data with value from index attribute."""
    data = []
    for decision_object in system:
        if decision_object[index] == value:
            data.append(decision_object)
    return data


def get_root(nodes, labels):
    """Find node with highest profit."""
    root = nodes[0]
    for node in nodes[1:]:
        if node.profit > root.profit:
            root = node
    nodes.remove(root)
    remove_from_labels(labels, root.name)
    return root


def remove_from_labels(labels, name):
    to_remove = ''
    for key, item in labels.items():
        if item == name:
            to_remove = key
    del labels[to_remove]


def find_leaves(root, attributes):
    edges = [edge for edge in root.edges if edge.decision is None]
    if len(edges) == 0:
        return  # recurrence end
    else:
        for edge in edges:
            if len(attributes) == 0:
                return  # recurrence end
            next_nodes = get_nodes(edge.data, attributes, edge.entropy)
            next_root = get_root(next_nodes, attributes)
            edge.node = next_root
            find_leaves(next_root, attributes)


def get_labels(nodes):
    labels = []
    for node in nodes:
        labels.append(node.name)
    return labels


def find_decisions(element):
    if type(element) is classes.Node:
        for edge in element.edges:
            find_decisions(edge)
    else:
        if element.node is None and element.decision is None:
            element.decision = max(element.decisions, key=element.decisions.get)
            return
        if element.node is not None:
            find_decisions(element.node)


# Other functions. <----------------------------------------------------------------------------------------------------
def are_element_in_element(articles1, articles2):
    """Return true if all of articles from element1 are in element2."""
    for article in articles1:
        if article not in articles2:
            return False
    return True


def is_list_in_list_of_lists(array, list_of_lists):
    for row in list_of_lists:
        if are_element_in_element(row, array):
            return True
    return False


def add_unique(articles, c):
    if c:
        for candidate in c:
            if are_element_in_element(articles, candidate):
                return
    c.append(articles)


def get_fs(rules):
    scales = []
    for rule in rules:
        if (len(rule.predecessors) + 1) not in scales:
            scales.append(len(rule.predecessors) + 1)
    scales.sort()
    return scales


def get_f_length(rules, scale):
    rules_scale = [rule for rule in rules if (len(rule.predecessors) + 1) == scale]
    return len(rules_scale)


def f_rules(rules, scale):
    rules_scale = [rule for rule in rules if (len(rule.predecessors) + 1) == scale]
    for scale_rule in rules_scale:
        yield scale_rule.print_rule(), [scale_rule.support, scale_rule.trust, scale_rule.quality]


def get_quality_rules(rules, thresholds):
    quality_rules = []
    for rule in rules:
        if rule.is_rule_quality(thresholds):
            quality_rules.append(rule)
    return quality_rules
