import csv
from regions import *


class CsvImport:
    gmina_type_codes = {'1': UrbanGmina, '2': RuralGmina, '3': UrbanRuralGmina, '4': City, '5': RuralArea,
                        '9': Representation}

    @staticmethod
    def open_csv(file_path):
        with open(file_path) as source:
            regions = csv.DictReader(source, dialect='excel-tab')
            for region in regions:
                if region['pow'] == '' and region['rgmi'] == '' and region['gmi'] == '':    # adding voivodeships
                    voivodeship_code = region['woj']
                    voivodeship_name = region['nazwa']
                    Voivodeship.add_region(voivodeship_code, voivodeship_name)
                elif region['pow'] != '' and region['rgmi'] == '' and region['gmi'] == '':  # adding powiats
                    powiat_code = region['woj']+region['pow']
                    powiat_name = region['nazwa']
                    if int(region['pow']) > 60:  # adding cities with powiat status
                        CityPowiat.add_region(powiat_code, powiat_name, upper_region_code=region['woj'])
                    else:                        # adding plain powiats
                        PlainPowiat.add_region(powiat_code, powiat_name, upper_region_code=region['woj'])
                else:     # adding gminas
                    gmina_city_code = region['woj']+region['pow']+region['gmi']
                    gmina_city_name = region['nazwa']
                    Gmina.add_region(gmina_city_code, gmina_city_name, upper_region_code=region['woj']+region['pow'])
                    gmina_code = region['woj']+region['pow']+region['gmi']+region['rgmi']
                    gmina_name = region['nazwa']
                    CsvImport.gmina_type_codes[region['rgmi']].add_region(gmina_code, gmina_name,
                                                                          upper_region_code=gmina_city_code)
