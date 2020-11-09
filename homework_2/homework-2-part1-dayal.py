# Mahira Dayal 
# Oct 30, 2020
# Homework 2, Part 1

# Part One: Lists
Numbers = [22, 90, 0, -10, 3, 22, 48]
print(len (Numbers))
print(Numbers[3])
print(Numbers[1]+Numbers[3])
print(sorted(Numbers, reverse=True) [1])
print(Numbers [-1])
print((sum (Numbers))/2)
import statistics
# I didn't want to add and divide, thought this was quicker. 
if (statistics.mean(Numbers))>(statistics.median(Numbers)):
    print ("Mean is larger")
else:
    print ("Median is larger")

#Part One: Dictionaries
movie = {
    'title': 'The Parent Trap',
    'year': '1998',
    'director': 'Nancy Meyers'
}
print("My favorite movie is", movie['title'], "which was released in", movie['year'], "and was directed by", movie['director'])
movie['budget'] = 15500000
movie['revenue'] = 92000000
print ("The difference between revenue and budget is $",movie['revenue']-movie['budget'])
if movie['budget']>movie['revenue']:
    print ("That was a bad investment")
elif movie['revenue']>(5*movie['budget']):
    print ("That was a great investment")
else:
    print("That was an okay investment")
population = {
    'Manhattan': 1.6,
    'Brooklyn': 2.6,
    'Bronx': 1.4,
    'Queens': 2.3,
    'Staten Island': 0.5
}
print (population['Brooklyn'])
print (sum(population.values()))
print ((population['Manhattan']/(sum(population.values())))*100, "%")
