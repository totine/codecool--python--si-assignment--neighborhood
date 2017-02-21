from csvimport import CsvImport
from queries import Queries
from ui import UI


class Menu:
    menu_queries_dict = {1: ('List statistics', Queries.list_statistic),
                         2: ('Display 3 cities with longest names', Queries.cities_with_longest_names),
                         3: ("Display county's name with the largest number of communities",
                             Queries.counties_with_largest_numbers_communities),
                         4: ('Display locations, that belong to more than one category',
                             Queries.locations_with_more_than_one_category),
                         5: ('Advanced search', Queries.advanced_search)}

    def __init__(self, menu_intro, exit_number=0, output_format='   ({}) {}'):
        self.output_format = output_format
        self.menu_intro = menu_intro
        self.menu_functions = []
        self.exit_text = [exit_number, "Exit program"]

    def make_menu_text(self):
        return '{}\n{}\n{}'.format(self.menu_intro,
                                   "\n".join([self.output_format.format(key, query_text[0])
                                              for key, query_text in Menu.menu_queries_dict.items()]),
                                   self.output_format.format(*self.exit_text))

    @classmethod
    def get_queries_dict(cls):
        return cls.menu_queries_dict


class Main:
    def __init__(self, menu):
        self.menu = menu
        self.is_asking = True

    def display_menu(self):
        UI.display_menu(self.menu.make_menu_text())

    def wait_for_menu_input(self):
        return UI.menu_input()

    def exec_function(self, option):
        if option in Menu.get_queries_dict():
            return Menu.get_queries_dict()[option][1]()

    def set_is_asking(self):
        self.is_asking = False


def main():
    CsvImport.open_csv('malopolska.csv')
    menu = Menu("What would you like to do:")
    main_menu = Main(menu)
    while main_menu.is_asking:
        main_menu.display_menu()
        option = main_menu.wait_for_menu_input()
        if option == 0:
            main_menu.set_is_asking()
        else:
            result = main_menu.exec_function(option)
            UI.simple_print(result)

if __name__ == "__main__":
    main()
