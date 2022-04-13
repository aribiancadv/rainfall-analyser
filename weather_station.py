import json
import datetime


def str_to_int(p):
    '''This function accepts a string and returns and integer.'''
    try:
        i = int(p)
        return i

    except ValueError:
        return -1


def str_to_float(p):
    '''This function accepts a string and returns a float.'''
    try:
        i = float(p)
        return i

    except ValueError:
        return -1.0


def month_to_int(p):
    '''This function accepts month prefixes from JSON data
    and returns the month as an integer using the datetime
    module.'''
    try:
        date_object = datetime.datetime.strptime(p, "%b")
        month_no = int(date_object.month)
        return month_no

    except ValueError:
        return -1


class Measurement:
    def __init__(self):
        self.year = 0
        self.month = 0
        self.value = 0.0

    def __repr__(self):
        '''This function returns the data members as a single string.'''
        s = "{"
        s += f"year={self.year}, month={self.month}, value={self.value}mm"
        s += "}"
        return s

    def from_strings(self, year_str, month_str, value_str):
        '''Assign inputs to data members and attempt converting them.
        If it fails, handle the exception.'''
        try:
            self.year = str_to_int(year_str)
            self.month = month_to_int(month_str)
            self.value = str_to_float(value_str)
            return True

        except ValueError:
            return False


class WeatherStation:
    def __init__(self):
        self.id = 0
        self.measurements = []

    def __repr__(self):
        '''This function returns the data members as a single string.'''
        s = "{"
        s += f"id={self.id}, measurements={self.measurements}"
        s += "}"
        return s

    def from_json(self, json_data):
        '''This function loads the JSON data, verifying first that there's
        only one key in the top level of the file.'''
        if len(json_data.keys()) == 1:
            pass

        station_id = next(iter(json_data.keys()))
        self.id = str_to_int(station_id)

        try:
            for measurement in next(iter(json_data.values())):
                year = measurement['Timestamp'][4:]
                month = measurement['Timestamp'][:3]
                value = measurement['Value']
                measurement_obj = Measurement()
                measurement_obj.from_strings(year, month, value)
                self.measurements.append(measurement_obj)

            return True

        except ValueError:
            return False

    def years(self, json_data):
        '''Create a list of years from json data.'''
        self.years_lst = []
        for measurement in next(iter(json_data.values())):
            year = measurement['Timestamp'][4:]
            if year not in self.years_lst:
                self.years_lst.append(year)

        return self.years_lst

    def maximum_per_year(self, json_data):
        '''Create dict containing years as keys and measurements as values.'''
        max_yearly_dict = dict.fromkeys(self.years_lst, 0.0)

        for measurement in next(iter(json_data.values())):
            year = measurement['Timestamp'][4:]
            value = str_to_float(measurement['Value'])

            if year in max_yearly_dict and value > max_yearly_dict[year]:
                max_yearly_dict[year] = value

        return max_yearly_dict


if __name__ == "__main__":

    input_file = open("rainfall.json")
    all_rainfall_data = json.load(input_file)
    input_file.close()

    weather_station_obj = WeatherStation()
    weather_station_obj.from_json(all_rainfall_data)
    print(weather_station_obj.years(all_rainfall_data))
    print(weather_station_obj.maximum_per_year(all_rainfall_data))
