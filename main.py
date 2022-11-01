# -*- coding: utf-8 -*-

from requests import get
from datetime import date
from csv import writer, reader
import sys


class WeatherForecast:

    FILEPATH = "checked_days.csv"
    url = "https://weatherbit-v1-mashape.p.rapidapi.com/forecast/daily"

    # coordinates for Poznań
    latitude = 52.40692
    longitude = 16.92993
    querystring = {"lat": latitude, "lon": longitude}

    def __init__(self):
        self.api_key = input('Podaj klucz do API: ')
        self.csv_dates = self.read_csv()

    def get_headers(self):
        return {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "weatherbit-v1-mashape.p.rapidapi.com"
        }

    def read_csv(self):

        csv_file = reader(open(self.FILEPATH))
        lines_from_csv = list(csv_file)

        dictionary_CSV = {}

        for element in lines_from_csv:
            dictionary_CSV[f"{element[0]}"] = {
                'precip': float(element[1]),
                'snow': float(element[2])}
        return dictionary_CSV

    def parse_data(self, date_as_string, forecast):

        value = forecast.get('precip', -1)

        if value > 0:
            print(f"\nW dniu {date_as_string} w Poznaniu "
                  "będzie padać deszcz! Zabierz ze sobą parasol :)")
            return("Będzie padać deszcz")

        elif value == 0:
            print(f"\nW dniu {date_as_string} w Poznaniu nie"
                  " będzie padać! Miłego dnia :)")
            return("Nie będzie padać")

        else:
            print(f"\nNie wiem czy w dniu {date_as_string} będzie"
                  " padać w Poznaniu!")
            return

    def contact_with_api(self, date_as_string):
        print("\nPobieram dane z API.")

        dictionary_API = {}
        r = get(self.url, headers=self.get_headers(),
                params=self.querystring)
        response = r.json()
        weather_forecast_data = response['data']

        for day in weather_forecast_data:
            dictionary_API[f"{day['datetime']}"] = {
                'precip': day['precip'],
                'snow': day['snow']
            }
        return dictionary_API

    def write_csv(self, data, filepath):
        with open(filepath, 'w', newline='') as csv_file:
            write = writer(csv_file)
            for element in data:
                write.writerow(element.split(","))

    def get_data(self, date_as_string):

        # print(self.csv_dates)
        # print(self.csv_dates.keys())

        if not date_as_string:
            date_as_string = str(date.today())
        if date_as_string in self.csv_dates.keys():
            # self.csv_dates = {}
            return self.parse_data(date_as_string,
                                   self.csv_dates[date_as_string])
        else:
            data_from_api = self.contact_with_api(date_as_string)
            list_for_write_csv = []
            for key, day in zip(data_from_api.keys(), data_from_api):
                string = (f"{key},{data_from_api[day]['precip']},"
                          f"{data_from_api[day]['snow']}")
                list_for_write_csv.append(string)

            self.write_csv(list_for_write_csv, self.FILEPATH)
            return self.parse_data(date_as_string, data_from_api)

    def __getitem__(self, item):
        '''
        if not self.csv_dates.get(item):
            print({'precip': 'unknown', 'snow': 'unknown'})
        else:
            print(self.csv_dates.get(item))
        '''

        if not self.csv_dates.get(item):
            return {'precip': 'unknown', 'snow': 'unknown'}
        else:
            return self.csv_dates.get(item)

    def __iter__(self):
        yield from self.csv_dates.keys()

    def items(self):
        for day, precip in self.csv_dates.items():
            yield day, self.parse_data(day, precip)


# %%

user_input_date = input("Podaj datę: ")

if len(user_input_date) != 10 and len(user_input_date) != 0:
    print("\nNieprawidłowy format daty.\n"
          "Prawidłowy format to YYYY-MM-DD, np. 2022-10-10.\n\n"
          "Działanie programu zakończone.")
    sys.exit()


wf = WeatherForecast()
wf.get_data(user_input_date)

# %%

'''
wf[date] da odpowiedź na temat pogody dla podanej daty (według specyfikacji
z poprzedniego zadania)
'''
wf["2022-11-10"]
wf["2022-11-17"]

'''
wf.items() zwróci generator tupli w formacie (data, pogoda) dla
już zcache’owanych rezultatów przy wywołaniu
'''
zmienna = wf.items()
# print(zmienna)  # zwraca generator

# print(next(zmienna))
# print(next(zmienna))
# print(next(zmienna))

'''
wf to iterator zwracający wszystkie daty, dla których znana jest pogoda
'''
for day in wf:  # wf to obiekt, po którym można iterować
    print(day)

# %%
