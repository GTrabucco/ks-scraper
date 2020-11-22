import requests, json 
  
base_url = "http://api.openweathermap.org/data/2.5/weather?"
  
cities = {'Bears': '3582383',
          'Bengals': '4508722',
          'Bills': '5129951',
          'Broncos': '5419384', 
          'Browns': '4422106',
          'Buccaneers': '4174757',
          'Cardinals': '5295985',
          'Chiefs': '4393217',   
          'Colts': '4861716',                
          'Cowboys': '4671240',
          'Dolphins': '4164166',
          'Eagles': '4440906', 
          'Falcons': '4883772',
          '49ers': '4568200',
          'Giants Jets': '5097459',
          'Jaguars': '4160021',
          'Lions': '4990729', 
          'Packers': '4580391', 
          'Panthers': '4460243',
          'Patriots': '4937222',
          'Rams Chargers': '5344994', 
          'Ravens': '4505716',
          'Saints': '4335045',
          'Seahawks': '5809844',
          'Texans': '4699066',
          'Titans': '5003243',
          'Vikings': '5037649',
          'Washington': '4360287',
          }

def check_data(response, city):
    x = response.json() 
    if x["cod"] != "404": 
        print(city)
        y = x["main"] 
        wind = x['wind']
        current_temperature = y["feels_like"] 
        current_humidiy = y["humidity"] 
        z = x["weather"] 
        weather_description = z[0]["description"] 
        wind_speed = wind['speed']
        f = (current_temperature - 273.15) * 9/5 + 32

        if current_humidiy > 80:
            print('current humidiy:', current_humidiy)
        if f > 90 or f < 40:
            print('current temperature:', str(round(f, 2)))
        if wind_speed > 5:
            print('wind speed', wind_speed)

        print(weather_description)
      
    else: 
        print(" City Not Found ") 

for city in cities:
    complete_url = base_url + "appid=" + api_key + "&id=" + cities[city]
    response = requests.get(complete_url) 
    check_data(response, city)
    print()

