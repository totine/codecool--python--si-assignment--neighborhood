import csv

class CsvImport:

    @staticmethod
    def open_csv(filepath):
        with open(filepath) as source:
            region_list = csv.DictReader(source, dialect='excel-tab')
            for region in region_list:
                if region['rgmi'] != '':
                    CommunityType.add_community_type(region['rgmi'], region['typ'])
                if region['pow'] == '' and region['rgmi'] == '' and region['gmi'] == '':
                    Province.add_region(region['woj'], region['nazwa'])
                elif region['pow'] != '' and region['rgmi'] == '' and region['gmi'] == '':
                    County.add_region(region['pow'], region['nazwa'], upper_region_code=region['woj'])
                    print(region['woj'])
                    if region['typ'] == 'miasto na prawach powiatu':
                        County.get_region_by_number(region['pow']).set_is_city_county(True)


                else:
                    Community.add_region(region['woj']+region['pow']+region['gmi']+region['rgmi'], region['nazwa'], upper_region_code=region['pow'])


class CommunityType:
    community_type_dict = {}
    community_type_list = []

    def __init__(self, code, name):
        self.code = code
        self.name = name
        self.community_type_list.append(self)
        self.community_type_dict[self.code] = self

    @classmethod
    def add_community_type(cls, code, community_type_name):
        cls(code, community_type_name)

    @classmethod
    def get_community_type(cls, code):
        return cls.community_type_dict[code]


class Region:
    region_dict = {}

    def __init__(self, code, name, upper_region_code=None):
        self.name = name
        self.code = code
        self.upper_region_code = upper_region_code
        self.inner_regions = []
        Region.region_dict[code]=self
        # self.region_dict[code] = self

    @property
    def subregions(self):
        print(Region.region_dict_to_list())
        print(list(filter(lambda x: x.upper_region == self, Region.region_dict_to_list())))
        return list(filter(lambda x: x.upper_region == self, Region.region_dict_to_list()))

    @classmethod
    def add_region(cls, code, name, upper_region_code=None):
        if code not in cls.region_dict:
            cls.region_dict[code] = cls(code, name, upper_region_code)

    @classmethod
    def get_region_by_number(cls, number):
        return cls.region_dict[number]

    @classmethod
    def region_dict_to_list(cls):
        return [region for index, region in cls.region_dict.items()]

    @classmethod
    def region_names_list(cls):
        return [region.name for region in cls.region_dict_to_list()]

    def add_inner_region(self, region):
        self.inner_regions.append(region)

    def get_subregions(self):
        return self.subregions


class Province(Region):
    region_dict = {}
    pass


class County(Province):
    region_dict = {}

    def __init__(self, code, name, upper_region_code):
        super().__init__(code, name, upper_region_code)
        self.is_city_county = None
        self.upper_region_code = upper_region_code

    def set_is_city_county(self, is_city_county):
        self.is_city_county = is_city_county

    @property
    def upper_region(self):
        print(super().region_dict, self.upper_region_code, self.name, County.region_dict)
        return Region.region_dict[self.upper_region_code]



class Community(County):
    region_dict = {}


    def __init__(self, code, name, upper_region_code):
        Region.__init__(self, code, name, upper_region_code)
        self.type_code = code[-1]


    @property
    def community_type(self):
        return CommunityType.get_community_type(self.type_code)





class Functions:
    functions_list = []

    def __init__(self, number, name, function):
        self.number = number
        self.name = name
        self.function = function
        Functions.functions_list.append(self)

    @staticmethod
    def list_statistic():
        print('województwo:', len(Province.region_dict))
        print('powiaty:', len(County.region_dict))
        for code, name in CommunityType.community_type_dict.items():
            print(name.name, len(list(filter(lambda x: x.type_code == code, Community.region_dict_to_list()))))
        print("miasto na prawach powiatu", len(list(filter(lambda x: x.is_city_county, County.region_dict_to_list()))))
    @classmethod
    def cities_with_longest_names(cls, number=3):
        return sorted(Community.region_names_list(), key=lambda x: len(x))[-number:]

    @classmethod
    def counties_with_largest_numbers_communities(cls):
        return [' '.join([comm.name for comm in (county.get_subregions())]) for county in County.region_dict_to_list()]

    @staticmethod
    def locations_with_more_than_one_category():
        region_list = Region.region_dict_to_list()
        region_name_list = Region.region_names_list()
        return sorted(list(map(lambda x: x.name, (filter(lambda x: region_name_list.count(x.name)>1, region_list)))))

    @staticmethod
    def advanced_search():
        phrase = UI.menu_phrase()
        return sorted(set(list(map(lambda x: x.name, filter(lambda y: phrase.lower() in y.name.lower(), Region.region_dict_to_list())))))

    @staticmethod
    def exit_program():
        pass

    @classmethod
    def get_function_list(cls):
        return cls.functions_list

    @classmethod
    def generate_menu(cls):
        menu_dict = {1: ('List statistics', cls.list_statistic),
                     2: ('Display 3 cities with longest names', cls.cities_with_longest_names),
                     3: ("Display county's name with the largest number of communities", cls.counties_with_largest_numbers_communities),
                     4: ('Display locations, that belong to more than one category', cls.locations_with_more_than_one_category),
                     5: ('Advanced search', cls.advanced_search)}
        for number, function in menu_dict.items():
            Functions(number, function[0], function[1])

    def get_number(self):
        return self.number

    def get_function(self):
        return self.function


class UI:

    @staticmethod
    def display_menu(menu_text):
        print(menu_text)

    @staticmethod
    def menu_input():
        option = input("Option: ")
        return int(option)

    @staticmethod
    def menu_phrase():
        phrase = input("Enter phrase to search: ")
        return phrase

    @staticmethod
    def display_list(list_to_display):
        print('\n'.join(list_to_display))


class Menu:
    def __init__(self, function_list, menu_intro, exit_number, output_format = '   ({}) {}'):
        self.function_list = function_list
        self.output_format = output_format
        self.menu_intro = menu_intro + '\n'
        self.exit_text = [exit_number, "Exit program"]

    def make_menu_text(self):
        return self.menu_intro + "\n".join([self.output_format.format(func.number, func.name) for func in self.function_list]) + self.output_format.format(*self.exit_text)

    def get_functions(self):
        return self.function_list



class Main:
    def __init__(self, menu):
        self.menu = menu
        self.is_asking = True

    def display_menu(self):
        UI.display_menu(self.menu.make_menu_text())

    def wait_for_menu_input(self):
        return UI.menu_input()

    def exec_function(self, option):
        for func in self.menu.get_functions():
            if func.get_number() == option:
                print(option, type(option), func.name)
                return func.function()

    def set_is_asking(self):
        self.is_asking = False


def main():
    CsvImport.open_csv('malopolska.csv')
    print(CommunityType.community_type_dict)
    print(County.region_dict)
    Functions.generate_menu()
    UI.display_list([province.name for province in County.region_dict_to_list()])
    UI.display_list([province.name for province in Province.region_dict_to_list()])
    UI.display_list([province.name for province in Community.region_dict_to_list()])
    menu = Menu(Functions.get_function_list(), "What would you like to do:", 0)
    asdf = Main(menu)
    while asdf.is_asking:
        asdf.display_menu()
        option = asdf.wait_for_menu_input()
        if option == 0:
            asdf.set_is_asking()
            print(asdf.is_asking)
        else:
            result = asdf.exec_function(option)
            UI.display_list(result)



main()







