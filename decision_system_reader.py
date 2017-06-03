import tools
from tkinter import _setit
from tkinter import *
from tkinter import ttk
import tkinter.filedialog as filedialog


class MainFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.system_file_path = ''
        self.type_filename = ''
        self.__init_ui()

        self.associative_rules = None
        self.is_system_calculated = False

    def __init_ui(self):
        self.parent.title("Decision System Reader")
        self.pack(fill=BOTH, expand=True)

        trn_system_load_frame = Frame(self)  # 1st frame // load trn
        trn_system_load_frame.pack(fill=X)

        self.load_system_button = Button(trn_system_load_frame, text="Load paragon system",
                                         command=self.__get_system_filename, width=18)
        self.load_system_button.pack(side=LEFT, padx=5, pady=5)

        self.system_text_box = Entry(trn_system_load_frame)
        self.system_text_box.pack(fill=X, padx=5, expand=True)
        self.system_text_box.configure(state=DISABLED)

        options_frame = Frame(self)  # 2nd frame // combobox and GO!
        options_frame.pack(fill=X)

        self.phi_label = Label(options_frame, text="Select Φ:")
        self.phi_label.pack(side=LEFT, padx=5, pady=5)

        self.phi = IntVar()
        self.phi.set('')
        self.phi_menu = OptionMenu(options_frame, self.phi, '')
        self.phi_menu.config(width=5)
        self.phi_menu.pack(side=LEFT, padx=5, pady=5)
        self.phi.trace('w', self.__set_system_status)  # when option menu is used, call function

        self.support_label = Label(options_frame, text="Support threshold:")
        self.support_label.pack(side=LEFT, padx=5, pady=5)

        self.support_text_box = Entry(options_frame, width=4)
        self.support_text_box.pack(fill=X, padx=5, side=LEFT)

        self.trust_label = Label(options_frame, text="Trust threshold:")
        self.trust_label.pack(side=LEFT, padx=5, pady=5)

        self.trust_text_box = Entry(options_frame, width=4)
        self.trust_text_box.pack(fill=X, padx=5, side=LEFT)

        self.quality_label = Label(options_frame, text="Quality threshold:")
        self.quality_label.pack(side=LEFT, padx=5, pady=5)

        self.quality_text_box = Entry(options_frame, width=4)
        self.quality_text_box.pack(fill=X, padx=5, side=LEFT)

        self.start_button = Button(options_frame, text="SHOW RULES", state=DISABLED, command=self.__start_apriori)
        self.start_button.pack(padx=5, pady=5, fill=X)

        tree_frame = Frame(self)  # 3rd frame // tree
        tree_frame.pack(fill=BOTH, expand=True)

        scrollbar = Scrollbar(tree_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.tree = ttk.Treeview(tree_frame, selectmode=NONE)
        self.tree.pack(padx=5, pady=5, fill=BOTH, expand=True)

        scrollbar.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.heading('#0', text='Rules')
        columns = ["Count", "Support", "Trust", "Quality"]
        self.tree["columns"] = columns
        for column in columns:
            self.tree.column(column, width=60, stretch=False)
            self.tree.heading(column, text=column)

    def __get_system_filename(self):
        self.trn_system_file_path = filedialog.askopenfilename(filetypes=[('Txt files', '*.txt')])
        self.system_text_box.configure(state=NORMAL)
        self.system_text_box.delete(0, "end")
        self.system_text_box.insert(0, self.trn_system_file_path)
        self.system_text_box.configure(state=DISABLED)
        if self.trn_system_file_path != '':
            with open(self.trn_system_file_path) as file:
                self.paragon_system = tools.get_system_objects(file)
            self.__refresh_list()
        self.start_button.config(state=NORMAL)
        self.is_system_calculated = False
        self.quality_text_box.delete(0, "end")
        self.tree.delete(*self.tree.get_children())

    def __refresh_list(self):
        apriori_options = list(range(1, tools.get_maximum_phi_size(self.paragon_system) + 1))
        self.phi_menu["menu"].delete(0, "end")
        for number in apriori_options:
            self.phi_menu["menu"].add_command(label=number, command=_setit(self.phi, number))
        self.phi.set(apriori_options[0])

    def __start_apriori(self):
        if not self.is_system_calculated:
            self.associative_rules = tools.get_apriori_rules(self.paragon_system, self.phi.get())
            self.is_system_calculated = True
        self.insert_rules()

    def insert_rules(self):
        thresholds = self.__get_thresholds()
        quality_rules = tools.get_quality_rules(self.associative_rules, thresholds)
        self.tree.delete(*self.tree.get_children())
        self.tree.insert("", 1, 1, text="All F sets", values=len(quality_rules))
        scales = tools.get_fs(quality_rules)
        for scale in scales:
            self.tree.insert(1, scale + 1, scale + 1, text="F{}".format(scale),
                             values=tools.get_f_length(quality_rules, scale))
            for string_rule, data in tools.f_rules(quality_rules, scale):
                values = [""]
                for i in ["{0:0.2f}".format(i) for i in data]:
                    values.append(i)
                self.tree.insert(scale+1, scale+1, text=string_rule,
                                 values=values)

    def __get_thresholds(self):
        thresholds = list()
        thresholds.append(float(self.support_text_box.get()) if self.support_text_box.get() != '' else 0)
        thresholds.append(float(self.trust_text_box.get()) if self.trust_text_box.get() != '' else 0)
        thresholds.append(float(self.quality_text_box.get()) if self.quality_text_box.get() != '' else 0)
        return thresholds

    def __set_system_status(self, *args):
        self.is_system_calculated = False


def main():
    main_frame = Tk()
    ex = MainFrame(main_frame)
    main_frame.geometry("800x600+380+100")
    main_frame.mainloop()


if __name__ == '__main__':
    main()
