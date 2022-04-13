import unittest
import weather_station


class TestWeatherStation(unittest.TestCase):

    def test_str_to_float(self):
        self.assertEqual(weather_station.str_to_float("1.0"), 1.0)

    def test_str_to_int(self):
        self.assertEqual(weather_station.str_to_int("1"), 1)

    def test_weatherstation_members(self):
        weather_station_obj = weather_station.WeatherStation()
        json_data = {
            23: [
                {
                    "Timestamp": "Feb 2011",
                    "Value": "159.6"
                },
                {
                    "Timestamp": "Mar 2011",
                    "Value": "78.6"

                }
            ]
        }
        self.assertEqual(weather_station_obj.from_json(json_data), True)
        self.assertEqual(weather_station_obj.years(json_data), ['2011'])
        self.assertEqual(weather_station_obj.maximum_per_year(json_data),
                         {'2011': 159.6})


if __name__ == '__main__':
    unittest.main()
