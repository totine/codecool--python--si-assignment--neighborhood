class UI:

    @staticmethod
    def display_menu(menu_text):
        print(menu_text)

    @staticmethod
    def menu_input():
        option = input("Option: ")
        while not option.isnumeric():
            option = input("Option (enter number): ")
        return int(option)

    @staticmethod
    def menu_phrase():
        phrase = input("Enter phrase to search: ")
        return phrase

    @staticmethod
    def display_list(list_to_display):
        print('\n'.join(list_to_display))

    @staticmethod
    def simple_print(string):
        print(string)


class Table:
    def __init__(self, first_row, table_body):
        self.first_row = first_row
        self.rows = table_body
        self.separator = '|'
        self.border_char = '-'

    @property
    def columns(self):
        columns = [[cell] for cell in self.first_row]
        for row in self.rows:
            for i in range(len(columns)):
                columns[i].append(row[i])
        return columns

    @property
    def longest_cells_list(self):
        cells_lengths = []
        for column in self.columns:
            cells_lengths.append(list(map(lambda x: len(str(x)), column)))
        return list(map(lambda x: max(x), cells_lengths))

    @property
    def table_width(self):
        return len(self.make_row(self.first_row))

    @property
    def column_count(self):
        return len(self.first_row)

    @property
    def empty_row(self):
        return ['']*self.column_count

    def __str__(self):
        return self.make_table()

    def make_table(self):
        upper_border = self.make_upper_border()
        bottom_border = self.make_bottom_border()
        middle_border = self.make_middle_border()
        first_row = self.make_row(self.first_row)
        table_body = self.make_table_body()
        all_table = [upper_border, first_row, middle_border, *table_body, bottom_border]
        return '\n'.join(all_table)

    def make_row(self, row):
        formatted_row = self.justify_cells(row)
        formatted_row = self.join_cells(formatted_row)
        return self.add_border_to_row(formatted_row)

    def make_table_body(self):
        table_body = []
        for row in self.rows:
            table_body.append(self.make_row(row))
            table_body.append(self.make_middle_border())
        return table_body[:-1]

    def make_upper_border(self):
        return '/{}\\'.format(self.border_char*(self.table_width-2))

    def make_bottom_border(self):
        return '\\{}/'.format(self.border_char*(self.table_width-2))

    def make_middle_border(self):
        middle_border = list(map(lambda x, y: x.center(self.longest_cells_list[y], self.border_char),
                                 self.empty_row, range(len(self.longest_cells_list))))
        middle_border = self.join_cells(middle_border)
        return self.add_border_to_row(middle_border)

    def justify_cells(self, row):
        return list(map(lambda x, y: str(x).center(self.longest_cells_list[y]), row,
                        range(len(self.longest_cells_list))))

    def join_cells(self, row):
        return self.separator.join(row)

    def add_border_to_row(self, row):
        return '{}{}{}'.format(self.separator, row, self.separator)


class TableWithJoinedRows(Table):
    pass
