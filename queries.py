from regions import *
from ui import UI, Table


class Queries:

    @staticmethod
    def list_statistic():
        voivodeships = [len(Voivodeship.get_region_list()), Voivodeship.get_region_type_name()]
        powiats = [len(Powiat.get_region_list()), Powiat.get_region_type_name()]
        urban_gminas = [len(UrbanGmina.get_region_list()), UrbanGmina.get_region_type_name()]
        rural_gminas = [len(RuralGmina.get_region_list()), RuralGmina.get_region_type_name()]
        urbanrural_gminas = [len(UrbanRuralGmina.get_region_list()), UrbanRuralGmina.get_region_type_name()]
        rural_areas = [len(RuralArea.get_region_list()), RuralArea.get_region_type_name()]
        cities = [len(City.get_region_list()), City.get_region_type_name()]
        city_powiats = [len(CityPowiat.get_region_list()), CityPowiat.get_region_type_name()]
        representations = [len(Representation.get_region_list()), Representation.get_region_type_name()]
        all_regions = [voivodeships, powiats, urban_gminas, rural_gminas, urbanrural_gminas, rural_areas,
                       cities, city_powiats, representations]
        first_row = ['Number', 'Małopolskie']
        return Table(first_row, all_regions)

    @classmethod
    def cities_with_longest_names(cls, number=3):
        description = 'Cities with longest names:\n'
        return description+"\n".join(sorted(Gmina.region_names_list(), key=lambda x: len(x))[-number:])

    @classmethod
    def counties_with_largest_numbers_communities(cls):
        max_community_number = max([county.get_number_of_subregions() for county in Powiat.region_dict_to_list()])
        counties_with_max_numbers = list(filter(lambda x: x.get_number_of_subregions() == max_community_number, Powiat.region_dict_to_list()))
        description = 'County with largest numbers of communities:\n'
        return description + Queries.region_list_to_string_list(counties_with_max_numbers)[0] + ' ({} communities)'.format(counties_with_max_numbers[0].get_number_of_subregions())

    @staticmethod
    def locations_with_more_than_one_category():
        table_body = sorted(list(filter(lambda x: x.get_number_of_subregions() > 1, Gmina.get_region_list())), key=lambda x: x.get_name())
        table_body = list(map(lambda x: [x.get_name(), x.get_number_of_subregions()], table_body))
        first_row = ['NAME', 'NUMBER OF CATEGORY']
        return Table(first_row, table_body)

    @staticmethod
    def advanced_search():
        phrase = UI.menu_phrase()
        first_row = ['LOCATION', 'TYPE']
        body = sorted((list(map(lambda x: [x.get_name(), x.get_region_type_name()], filter(lambda y: phrase.lower() in y.get_name().lower() and y.get_class_name() != "Gmina", Region.get_region_list())))))
        return Table(first_row, body)

    @staticmethod
    def region_list_to_string_list(region_list):
        return [str(region) for region in region_list]






