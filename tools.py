import itertools as it
import copy
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


def get_maximum_phi_size(paragon_system):
    """Return number of most frequency value in paragon system."""
    frequencies = {}
    for paragon in paragon_system:
        for article in paragon:
            if article not in frequencies:
                frequencies[article] = 1
            else:
                frequencies[article] += 1
    return max(frequencies.values())


# Apriori functions. <--------------------------------------------------------------------------------------------------
def get_apriori_rules(paragon_system, phi):  # main Apriori function
    """Classify tst_system by trn_system."""
    rules = []
    frequencies = get_frequencies(paragon_system)
    f = get_start_f(frequencies, phi)

    while True:
        c = get_c(f)
        f = get_f(c, phi, paragon_system)
        if len(f) != 0:
            rules.append(copy.copy(f))
        if len(f) < 2:
            return get_associative_rules(rules, paragon_system)


def get_frequencies(paragon_system):
    """Set frequencies for paragon system in dictionary."""
    frequencies = {}
    for paragon in paragon_system:
        for article in paragon:
            if article not in frequencies:
                frequencies[article] = 1
            else:
                frequencies[article] += 1
    return frequencies


def get_start_f(frequencies, phi):
    """Return sorted list with values more frequency then phi."""
    f = []
    for item, value in frequencies.items():
        if value >= phi:
            f.append([item])
    f.sort()
    return f


def get_c(f):
    """Get candidates for next F."""
    c = []
    combination_length = len(f[0]) + 1  # f is list of list, f[0] is first list;
    combinations = it.combinations(f, 2)
    for combination in combinations:  # some transform are needed; c = [[value1, value2], [value3, value4], ...]
        c_combination = []
        for element in combination:
            for article in element:
                if article not in c_combination:
                    c_combination.append(article)
        if len(c_combination) == combination_length and apriori_intersection(c_combination, f):
            add_unique(c_combination, c)
    return c


def get_f(c, phi, paragon_system):
    """Get candidates with frequency greater then f."""
    f = []
    for candidate in c:
        frequency = get_number_of_occurrence(candidate, paragon_system)
        if frequency >= phi:
            f.append(candidate)
    return f


def get_number_of_occurrence(articles, paragon_system):
    """Return number of occurrence of element in paragon."""
    counter = 0
    for paragon_articles in paragon_system:
        if are_element_in_element(articles, paragon_articles):
            counter += 1
    return counter


def apriori_intersection(articles, f):
    combinations = it.combinations(articles, len(f[0]))
    for combination in combinations:
        if not is_list_in_list_of_lists(combination, f):
            return False
    return True


def get_associative_rules(rules, paragon_system):
    associative_rules = []
    for row in rules:
        for rule in row:
            for index in range(len(rule)):
                predecessors = rule[:]
                del predecessors[index]
                consequent = rule[index]
                associative_rule = classes.AssociativeRule(predecessors, consequent)
                associative_rule.calculate_quality(paragon_system)
                associative_rules.append(associative_rule)
    return associative_rules


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
