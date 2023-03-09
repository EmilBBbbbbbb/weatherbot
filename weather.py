import requests
from pprint import pprint
from config import open_wether_token


def wether_day(data, day):
    dt=data["list"][8*day]["dt_txt"]
    temp=data["list"][8*day]["main"]["temp"]
    wind=data["list"][8*day]["wind"]["speed"]
    print(f"Погода на {dt}:\n"
              f"Температура: {temp}°С\n"
              f"Скорость ветра: {wind}м/с\n")

def get_wether(city, open_wether_token):
    try:

        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={open_wether_token}&units=metric"
        )

        data= r.json()

        wether_day(data, 0)
        #pprint(data) #all wether
        #pprint(data["list"][0])
        #pprint(data["list"][8]["dt_txt"])

    except Exception as ex:
        print(ex)
        print("Проверьте название города")



def main():
    city=input("Введите город: ")
    get_wether(city, open_wether_token)



if __name__ == "__main__":
    main()
