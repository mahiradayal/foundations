# Mahira Dayal 
# Oct. 30, 2020 
# Homework 2, Part 2 

# Part Two: Lists
countries = ["France", "Germany", "Italy", "Spain", "United Kingdom", "Greece", "Switzerland"]
for x in countries:
  print(x)
countries.sort()
print ("First element on the list is", countries [0])
print ("Second to last element on the list is", countries [-2])
countries.remove('Italy')
for y in countries:
    y = y.upper()
    print(y)

#Part Two: Dictionaries
tree = {
    'name': 'Kongeegen',
    'species': 'Pedunculate oak',
    'age': 1200,
    'location_name': 'Denmark',
    'latitude': 55.8520,
    'longitude': 11.9919
}
print (tree['name'], "is a", tree['age'], "year old tree that is in", tree['location_name'])
nyc = {
    'latitude': 40.7128,
    'longitude': -74.0059
}
if tree['latitude']<nyc['latitude']:
    print ("The tree", tree['name'], "in", tree['location_name'], "is south of NYC")
else:
    print ("The tree", tree['name'], "in", tree['location_name'], "is north of NYC")
user_age = int(input("How old are you:"))
if user_age> tree['age']:
    print ("You are", (user_age-tree['age']), "years older than", tree['name'])
else:
    print (tree['name'], "was", tree['age']-user_age, "years old when you were born")

# Part two: Lists of dictionaries

world = [{
    'name': 'Moscow',
    'latitude': 55.7558,
    'longitude': 37.6173
}, 
{
    'name': 'Tehran',
    'latitude': 35.6892,
    'longitude': 51.3890
}, 
{
    'name': 'Flakland Islands',
    'latitude': -51.7963,
    'longitude': -59.5236
}, 
{
    'name': 'Seoul',
    'latitude': 37.5665,
    'longitude': 126.9780
}, 
{
    'name': 'Santiago',
    'latitude': -33.4489,
    'longitude': -70.6693
}]
print (world)
print ("-------")
for z in world:
    print (z['name'])
    if z['latitude']>0:
         print ("This one's above equator")
    elif z['latitude']<0:
        print ("This one's below equator")
    if z['name'] == 'Flakland Islands':
        print ("The Falkland Islands are a biogeographical part of the mild Antarctic zone")
    if z['latitude']>tree['latitude']:
        print ("This one's above the tree!")
    elif z['latitude']<tree['latitude']:
        print ("This one's below the tree!")