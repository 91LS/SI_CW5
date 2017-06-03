import tools


class AssociativeRule:
    def __init__(self, predecessors, consequent):
        self.predecessors = predecessors
        self.consequent = consequent
        self.support = None
        self.trust = None
        self.quality = None

    def calculate_quality(self, paragon_system):
        """Calculate support, trust and quality for Associative Rule."""
        predecessor_consequent_count, predecessor_count = self.__get_data_for_quality(paragon_system)
        self.__calculate_support(predecessor_consequent_count, len(paragon_system))
        self.__calculate_trust(predecessor_consequent_count, predecessor_count)
        self.quality = self.support * self.trust

    def __get_data_for_quality(self, paragon_system):
        """Return data for calculate quality."""
        predecessor_consequent_count = 0
        predecessor_count = 0
        for articles in paragon_system:
            predecessor_consequent = self.predecessors[:]
            predecessor_consequent.append(self.consequent)
            if tools.are_element_in_element(predecessor_consequent, articles):
                predecessor_consequent_count += 1
            if tools.are_element_in_element(self.predecessors, articles):
                predecessor_count += 1
        return predecessor_consequent_count, predecessor_count

    def __calculate_support(self, predecessor_consequent_count, number_of_objects):
        """Calculate support of rule."""
        self.support = predecessor_consequent_count / number_of_objects

    def __calculate_trust(self, predecessor_consequent_count, predecessor_count):
        """Calculate support of rule."""
        self.trust = predecessor_consequent_count / predecessor_count

    def print_rule(self):
        a = ""
        for predecessor in self.predecessors:
            a += "{} ^ ".format(predecessor)
        a = a[:-3]
        a += " => {}".format(self.consequent)
        return a

    def is_rule_quality(self, thresholds):
        if self.support >= thresholds[0] and self.trust >= thresholds[1] and self.quality >= thresholds[2]:
            return True
        return False
