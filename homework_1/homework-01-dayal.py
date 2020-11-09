#Mahira Dayal
#09/27/2020
#Homework 1
birth_year = input("What year were you born: ")
birth_year_int = int(birth_year)
if 2020-birth_year_int<0:
    print ("Unless you're from the future, try again because you aren't born yet. If you're from the future, tell me when COVID ends -- md3936@columbia.edu")
else: 
    age=2020-birth_year_int
#According to WebMD, the human heart beats 100,000 times per day. 
human_heart_year=100000*356
heartbeat=age*human_heart_year
print ("Your heart has beaten", heartbeat, "times")
#The Smithsonian Magazine says a wild blue whale's heartbeat ranges from 2bpm to 37bpm. I'll say it averages 19bpm.
whale_heart_year= 19*60*24*365
whale_heartbeat= whale_heart_year*age
print ("Meanwhile a blue whale's heart has beaten", whale_heartbeat, "times")
#According to medivet.co.uk, a rabbit's resting heart beat is between 140 and 180bpm. I'll average to 160 beats per minute. 
rabbit_heart_year= 160*60*24*365
rabbit_heartbeat= rabbit_heart_year*age
rabbit_heartbeat_millions= rabbit_heartbeat/1000000
print ("And a rabbit's", rabbit_heartbeat_millions, "million times")
#According to universetoday.com (very reputable, I'm sure) one year on Venus is about 0.6152 Earth years
venus_age= 0.6152*age
print ("If you lived on Venus, you'd be", venus_age, "years old")
#NASA says a year in Neptune is 165 Earth years
neptune_age=165/age
print ("And you'd be", neptune_age, "on Neptune.") 
if birth_year_int==1998:
    print ("Wow we're the same age")
elif birth_year_int>1998:
    print ("Aw, you're", birth_year_int-1998, "years younger than me")
elif birth_year_int<1998:
    print ("In case you were wondering, you're", 1998-birth_year_int, "years older than me")
if (birth_year_int % 2 == 0): 
    print ("And you were born in an even year")
else:
    print ("You were born in an odd year")
if birth_year_int==1960:
    print ("Eisenhower was the president the year you were born, and there was one Republican presdient between 1960 and the year you were born")
if birth_year_int==1961 or birth_year_int==1962:
    print ("JFK was the president and there has been 1 Democratic president")
if birth_year_int>1962 and birth_year_int<1969:
    print ("Johnson was president and there have been 2 democrats")
if birth_year_int>1968 and birth_year_int<1974:
    print ("Nixon was president and there have been 2 democrats")
if birth_year_int>1973 and birth_year_int<1977:
    print ("Ford was president and there have been 2 democrats")
if birth_year_int>1976 and birth_year_int<1981:
    print ("Carter was president and there have been 3 democrats")
if birth_year_int>1980 and birth_year_int<1989:
    print ("Reagan was president and there have been 3 democrats")
if birth_year_int>1988 and birth_year_int<1993:
    print ("Bush was president and there have been 3 democrats")
if birth_year_int>1992 and birth_year_int<2001:
    print ("Clinton was president and there have been 4 democrats")
if birth_year_int>2000 and birth_year_int<2009:
    print ("Bush was president and there have been 4 democrats")
if birth_year_int>2008 and birth_year_int<2017:
    print ("Obama was president and there have been 5 democrats")
if birth_year_int>2016 and birth_year_int<2021:
    print ("Trump is president and there have been 5 democrats")


