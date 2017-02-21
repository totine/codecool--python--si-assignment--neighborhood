class Region:
    region_name = None
    region_dict = {}

    def __init__(self, code, name, upper_region_code=None):
        self.name = name
        self.code = code
        self.upper_region_code = upper_region_code
        self.inner_regions = []
        Region.region_dict[code] = self  # adds region to all region dictionary - region_dict in Region class

    @classmethod
    def get_region_list(cls):
        """Returns list with region instances made from the class region dict."""
        return cls.region_dict_to_list()

    @classmethod
    def add_region(cls, code, name, upper_region_code=None):
        """Makes new region instance and adds it to self class region dict:
           index - region code, value - region instance"""
        if code not in cls.region_dict:
            new_region = cls(code, name, upper_region_code)
            cls.region_dict[code] = new_region
            Region.region_dict[code] = new_region

    @classmethod
    def get_region_by_number(cls, number):
        return cls.region_dict[number]

    @classmethod
    def region_dict_to_list(cls):
        return [region for index, region in cls.region_dict.items()]

    @classmethod
    def region_names_list(cls):
        return [region.name for region in cls.region_dict_to_list()]

    @classmethod
    def region_codes_list(cls):
        return [region.code[:-1] for region in cls.region_dict_to_list()]

    @classmethod
    def get_region_type_name(cls):
        return cls.region_name

    @property
    def subregions(self):
        """Property with list with region subregions instances (for example list of gminas in powiat)."""
        return list(filter(lambda x: x.upper_region == self, Region.get_region_list()))

    @property
    def number_of_subregions(self):
        """Property with numbers of subregions in region (for example numbers of gminas in powiat)"""
        return len(self.subregions)

    @property
    def upper_region(self):
        """Property that stores instance of upper region in hierarchy (for example powiat that gmina belongs to).
           It is searched in main region dict in Region class by self.upper_region_code attribute.
           For voivodeship, that don't have an upper region returns None"""
        return Region.region_dict[self.upper_region_code] if self.upper_region_code else None

    def __str__(self):
        return self.name

    def add_inner_region(self, region):
        self.inner_regions.append(region)

    def get_subregions(self):
        return self.subregions

    def get_number_of_subregions(self):
        return self.number_of_subregions

    def get_name(self):
        return self.name

    def get_class_name(self):
        return self.__class__.__name__


class Voivodeship(Region):  # Województwo
    region_name = 'Województwo'
    region_dict = {}
    pass


class Powiat(Region):  # Powiat
    region_name = 'Powiat'
    region_dict = {}

    def __init__(self, code, name, upper_region_code):
        super().__init__(code, name, upper_region_code)
        Powiat.region_dict[code] = self


class PlainPowiat(Powiat):
    region_name = 'Powiat'
    region_dict = {}


class CityPowiat(Powiat):  # miasto na prawach powiatu (city with powiat status)
    region_name = 'Miasto na prawach powiatu'
    region_dict = {}


class Gmina(Region):
    region_name = 'Gmina'
    region_dict = {}


class UrbanGmina(Gmina):  # Gmina miejska
    region_name = 'Gmina miejska'
    region_dict = {}


class Representation(UrbanGmina):  # Delegatura
    region_name = 'Delegatura'
    region_dict = {}


class RuralGmina(Gmina):  # Gmina wiejska
    region_name = 'Gmina wiejska'
    region_dict = {}


class UrbanRuralGmina(Gmina):  # Gmina miejsko-wiejska
    region_name = 'Gmina miejsko-wiejska'
    region_dict = {}


class City(UrbanRuralGmina):  # Miasto
    region_name = 'Miasto'
    region_dict = {}


class RuralArea(UrbanRuralGmina):  # Obszar wiejski
    region_name = 'Obszar wiejski'
    region_dict = {}
