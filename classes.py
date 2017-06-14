import tools
class_id = 1


class Node:
    def __init__(self, name, data, profit):
        global class_id
        self.name = name
        self.data = data
        self.profit = profit
        self.edges = []
        self.id = class_id
        class_id += 1

    def calculate_profit(self):
        for edge in self.edges:
            self.profit -= edge.profit


class Edge:
    def __init__(self, name, data, index, edges):
        global class_id
        self.name = name
        self.data = self.get_data(data, name, index)
        self.decisions = self.get_decisions()
        self.decision = self.get_decision()
        self.entropy = tools.get_entropy(self.decisions)
        self.profit = self.calculate_profit(edges[self.name], sum(edges.values()))
        self.node = None
        self.id = class_id
        class_id += 1

    def calculate_profit(self, counter, denominator):
        return self.entropy * counter / denominator

    def get_data(self, system, value, index):
        data = []
        for decision_object in system:
            if decision_object[index] == value:
                data.append(decision_object)
        return data

    def get_decisions(self):
        decisions = {}
        for decision_object in self.data:
            attribute_value = decision_object[-1]
            if attribute_value not in decisions:
                decisions[attribute_value] = 1
            else:
                decisions[attribute_value] += 1
        return decisions

    def is_edge_leaf(self):
        if len(self.decisions) == 1:
            return True
        return False

    def get_decision(self):
        if self.is_edge_leaf():
            return next(iter(self.decisions))
        else:
            return None
