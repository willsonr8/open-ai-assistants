from functionality import find_restaurants_near_me

response = find_restaurants_near_me(keyword='burger', min_price=1, max_price=4, name=None, open_now=True, radius=5000)
for i in range(len(response['results'])):
    print(f"{i}. {response['results'][i]['name']}\n")