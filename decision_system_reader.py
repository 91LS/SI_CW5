import tools
import classes
from tkinter import *
from tkinter import ttk
import tkinter.filedialog as filedialog
import copy


class MainFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.system_file_path = ''
        self.type_filename = ''
        self.__init_ui()

    def __init_ui(self):
        self.parent.title("Decision System Reader")
        self.pack(fill=BOTH, expand=True)

        trn_system_load_frame = Frame(self)  # 1st frame // load trn
        trn_system_load_frame.pack(fill=X)

        self.load_system_button = Button(trn_system_load_frame, text="Load system",
                                         command=self.__get_system_filename, width=18)
        self.load_system_button.pack(side=LEFT, padx=5, pady=5)

        self.system_text_box = Entry(trn_system_load_frame)
        self.system_text_box.pack(fill=X, padx=5, expand=True)
        self.system_text_box.configure(state=DISABLED)

        options_frame = Frame(self)  # 2nd frame // combobox and GO!
        options_frame.pack(fill=X)

        self.ignore_label = Label(options_frame, text="Index of attributes to ignore (comma is delimiter):")
        self.ignore_label.pack(side=LEFT, padx=5, pady=5)

        self.ignore_text_box = Entry(options_frame, width=10)
        self.ignore_text_box.pack(fill=X, padx=5, side=LEFT)
        self.ignore_text_box.insert(0, "0")

        self.start_button = Button(options_frame, text="SHOW TREE", state=DISABLED, command=self.__start_id3)
        self.start_button.pack(padx=5, pady=5, fill=X)

        tree_frame = Frame(self)  # 3rd frame // tree
        tree_frame.pack(fill=BOTH, expand=True)

        scrollbar = Scrollbar(tree_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.tree = ttk.Treeview(tree_frame, selectmode=NONE)
        self.tree.pack(padx=5, pady=5, fill=BOTH, expand=True)

        scrollbar.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.heading('#0', text='ID3 Tree')

    def __get_system_filename(self):
        self.system_file_path = filedialog.askopenfilename(filetypes=[('Txt files', '*.txt')])
        self.system_text_box.configure(state=NORMAL)
        self.system_text_box.delete(0, "end")
        self.system_text_box.insert(0, self.system_file_path)
        self.system_text_box.configure(state=DISABLED)
        if self.system_file_path != '':
            with open(self.system_file_path) as file:
                self.system = tools.get_system_objects(file)
        self.start_button.config(state=NORMAL)

    def __start_id3(self):
        classes.class_id = 1
        ignore_indexes = [int(i) for i in self.ignore_text_box.get().split(',') if i != '']
        cut_system = self.__get_cut_system(ignore_indexes)
        labels = self.__get_labels(cut_system)
        system = cut_system[1:]
        self.root = tools.get_id3_tree(labels, system)
        self.insert_rules()

    def __get_cut_system(self, ignored_indexes):
        cut_system = copy.deepcopy(self.system)
        for decision_object in cut_system:
            for index in sorted(ignored_indexes, reverse=True):
                del decision_object[index]
        return cut_system

    def __get_labels(self, cut_system):
        labels = {}
        for index, label in enumerate(cut_system[0][:-1]):
            labels[index] = label
        return labels

    def insert_rules(self):
        self.tree.delete(*self.tree.get_children())
        self.tree.insert("", 1, 1, text=self.root.name)
        self.insert_element(self.root)

    def insert_element(self, element):
        if type(element) is classes.Node:
            for edge in element.edges:
                self.tree.insert(element.id, 0, edge.id, text=edge.name)
                self.insert_element(edge)
        else:
            if element.node is None:
                self.tree.insert(element.id, 0, text=element.decision if element.decision is not None else "?")
                return
            self.tree.insert(element.id, 0, element.node.id, text=element.node.name)
            self.insert_element(element.node)


def main():
    main_frame = Tk()
    ex = MainFrame(main_frame)
    main_frame.geometry("800x600+380+100")
    main_frame.mainloop()


if __name__ == '__main__':
    main()
