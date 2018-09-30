
# coding: utf-8

# # Homework 1

# Ben Smith
# 
# ECON 213R
# 
# 9/19/18

# First, I will call the three files that I will use.
# 
# "csvfile" comes from https://fred.stlouisfed.org/series/UNRATE/,
# "xlsxfile" comes from https://data.bls.gov/timeseries/LNS14000000, and
# "txtfile" comes from a csv file downloaded from https://crime-data-explorer.fr.cloud.gov/downloads-and-docs, under "Arrest Data"

# In[540]:

#Import necessary libraries
import os
import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas.util.testing as tm; tm.N = 3
import time

sns.set(style='ticks', palette='Set2')
get_ipython().magic('matplotlib inline')

wrkdir = 'C:/Users//Ben Smith//Downloads'

os.chdir(wrkdir)

#Assign dataframes for each file
csvfile = pd.read_csv('UNRATE (6).csv') #from FRED
xlsxfile = pd.read_excel('unemp_bls.xlsx') #from BLS
txtfile = pd.read_csv('arrests_national.txt', sep="\t", header=None) #csv from FBI, then saved as txt


# Now, I will look at each of my files.

# In[541]:

csvfile[:3]


# In[542]:

xlsxfile[:3]


# In[543]:

txtfile[:3]


# Now, I will begin to work with each of my files, one after the other. I begin with "csvfile."

# ### Cleaning The CSV File

# I start by cleaning "csvfile." It actually looks pretty clean, so what I'll do is separate the "Date" variable into year, month, and day.

# In[544]:

#Here, I'm creating a function that splits the Date variable into year, month, and day for any files formatted like the csv file
def date_splitter(file):     
    file['year'] = file.DATE.str.split('-').str[0]
    file['month'] = file.DATE.str.split('-').str[1]
    file['day'] = file.DATE.str.split('-').str[2]
    
    return file


# In[545]:

#Here, I'm using the above function to create columns on the csv file with values for the years, months, and days

csvfile = date_splitter(csvfile)

print(csvfile['year'][:3])
print(csvfile['month'][:3])
print(csvfile['day'][:3])

print(csvfile[:3])


# In[546]:

#I want to find outliers among the unemployment rates my csv file has

#Let's see summary statistics

csvfile.describe()


# The min and max values look reasonable. Let's see what a box-and-whisker plot would look like for this data

# In[547]:

bbox = csvfile['UNRATE'].plot(kind="box")


# In[548]:

#Let's see if there are any missing values

csvfile.columns[csvfile.isnull().any()]


# There aren't any! 
# 
# This data looks pretty clean, so I will use it to answer a question.
# 
# My question: is there a correlation between month and unemployment?

# In[549]:

#First, lets convert days, months, and years into integers (they are in string format for some reason)

def to_num(obj):
    obj = pd.to_numeric(obj, errors='coerce')
    return obj


# In[550]:

csvfile.day = to_num(csvfile.day)
csvfile.month = to_num(csvfile.month)
csvfile.year = to_num(csvfile.year)

#This command will give the correlation coefficient between month and unemployment

csvfile['UNRATE'].corr(csvfile['month'])


# This correlation coefficient is quite small; a regression analysis will likely show that month has an insignificant effect on unemployment rates. Just for fun, let's see what the correlation would be between year and unemployment.

# In[551]:

csvfile['UNRATE'].corr(csvfile['year'])


# Notice that unemployment is much more correlated with year than with month, which makes a lot of sense.

# ### Describing The CSV File

# Now let's describe the data in our csv file.

# In[552]:

csvfile.describe()


# Let's take a look at some other percentiles as well.

# In[553]:

csvfile.describe(percentiles=[.01,.05,.95,.99])


# Notice that it only really makes sense to consider the above statistics with respect to the unemployment rate. But, I've included the above table for those interested in the statistics this file has for dates. Notice that "day" is always 1. This will make our next command interesting.

# In[554]:

#Let's check out our correlation coefficient matrix
csvfile.corr()


# Notice that there are no valid coefficients for "day." That's because, as we just saw, "day" has a standard deviation of 0. Recall from ECON 378 that correlation coefficients are calculated with standard deviations in the denominator. Thus, if the standard deviation of one variable is 0, then correlation is impossible to calculate.

# Now let's create an indicator for whether the year is later or earlier than 1990. Then, we'll see how the summary statistics compare for the unemployment rate before and after 1990.

# In[555]:

#This function will create the indicator just described for any file
def split_years(file, year):
    file['late'] = file['year'] >= year
    
    #Change "late" from boolean to an integer value
    file.late = file.late.astype(int)
    
    return file


# In[556]:

#Divide the csvfile into before and after 1990
csvfile = split_years(csvfile, 1990)

#Check that "late" looks the way it should
print(csvfile['late'][:3])
print(csvfile['late'][-3:])


# The beginning and end look good! I have checked further and all of "late" seems to look the way it should.
# 
# Now let's see what unemployment looks like before and after 1990.

# In[557]:

csvfile.groupby('late')['UNRATE'].describe()


# Recall that "1" means after 1990 and "0" means before 1990. So, we see here that the mean unemployment rate has been higher since 1990, but the standard deviation has been lower. In fact, both the minimum and maximum were both before 1990. One particularly interesting observation is that the median (the 50th percentile) in both time periods is the same.

# ### Visualizing The CSV File

# Now let's visualize our data in lots of different ways. We start with a scatter plot.

# In[558]:

sns.lmplot(x="year", y="UNRATE", data=csvfile)


# Wow! Isn't that cool? This scatter plot shows a well-defined cycle of rising and falling unemployment rates over the past 70 years. 
# 
# Using this plot, it is clear that the maximum unemployment rate attained in this dataset was in the 1980's and the minimum was in the 1950's. 
# 
# It is interesting that the fastest rise and the largest fall in unemployment in this data both appear to have come following to the Great Recession in 2008.
# 
# Also notice that the regression line has a positive slope. This begs the questions: will unemployment continue to rise on average, or will we be able to bring it back down? And, why has unemployment increased with time over the last several decades?
# 
# The slope may actually become negative if the data included the Great Depression, so more data might be nice. However, Keynes' theories changed public policy after the Great Depression. So, I would argue that this data is quite useful, since it offers a near-comprehensive look at trends in unemployment rates in the modern era of post-Depression policy.

# Here are some more ways to visualize the data.

# A histogram:

# In[559]:

sns.distplot(csvfile.UNRATE, kde=True)


# Here we see that the unemployment rate has most frequently fallen near 6% within the range of our dataset.

# Here's a joint plot:

# In[560]:

sns.jointplot(csvfile.year, csvfile.UNRATE, kind="hex")


# This plot looks a lot like the scatter plot -- only using hexagons instead of dots.

# Here's a line chart!

# In[561]:

plt.plot(csvfile['year'],csvfile['UNRATE'])


# This chart connects the dots from the scatter plot. That is useful because with the line chart, it becomes easier to quickly draw conclusions about time trends.

# Last but not least, I present a heat map of unemployment over months and years.

# In[562]:

data = csvfile.pivot("month", "year", "UNRATE")

f, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(data, annot=False, linewidths=.5, ax=ax, cmap='Blues')


# Thus, I make an end to my analysis of the unemployment rates given over the last 70 years by the csv file I downloaded. We have found that the unemployment rate has followed a cycle of ups and downs over the years, but it seems to be increasing in average over time.

# ### Cleaning The XLSX File

# I now commence my analysis of the xlsx file I downloaded, which also focuses on unemployment rates, although it is from a different source and only contains the past ten years. Will this file's results be similar to those we found from my last file? We'll find out.

# We again start by cleaning the file. A quick survey of the numbers shows that there are no extreme outliers. Notice, however from the portion shown near the top of this file that the first several rows contain no data. We'll start by finding which rows we don't need and getting rid of them.

# In[563]:

xlsxfile[:15]


# It looks like we don't need rows 0-9, and row 10 gives variables

# In[564]:

#Drop rows 0-9

xlsxfile = xlsxfile.iloc[10:]
xlsxfile


# Now we want row 10 to become the column names. Let's make that happen now.

# In[565]:

#Here, we define a function to reset the index so that it starts at 0 and ascends from there
#This function is small enough that its only purpose is to save time and space typing in the future, every time I want to reset a file's index

def reset_ind(file):
    file2 = file.reset_index(drop=True)
    return file2

#This function takes the first row and turns it into columns' names, and then drops that first row
def var_adopt(file):
    #Make the first row into the column names
    file.columns = file.iloc[0]

    #Drop the first row
    file = file.reindex(file.index.drop(0))
    
    #The index is now starting at 1, so let's reset the index
    file = reset_ind(file)
    
    return file


# In[566]:

#First, make the index of the dataframe start at 0 again
xlsxfile = reset_ind(xlsxfile)

xlsxfile = var_adopt(xlsxfile)


# Let's take a look at the file now.

# In[567]:

xlsxfile


# Now let's make it so the month variables become one. To do this, I will first set the index equal to the years and then use Prof. Folkman's handy unpivot function to create a "month" variable and a "UNRATE"

# In[568]:

#Step 1: Set the index equal to the years
xlsxfile.set_index('Year', inplace=True)

xlsxfile


# In[569]:

#Step 2: Unpivot

def unpivot(frame):
    N, K = frame.shape
    data = {'UNRATE' : frame.values.ravel('F'),
            'month' : np.asarray(frame.columns).repeat(N),
            'year' : np.tile(np.asarray(frame.index), K)}
    return pd.DataFrame(data, columns=['year', 'month', 'UNRATE'])

xlsxfile = unpivot(xlsxfile)

xlsxfile[:3]


# Voila! (Thanks for the function, Prof. Folkman.)
# 
# We now set the months equal to numbers.

# In[570]:

def num_months(file):
    d = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12, }

    try:
        file.month = file.month.map(d)
    except:
        print("Exception")
        
    return file
    

xlsxfile = num_months(xlsxfile)
xlsxfile[:3]


# Now let's get the dataframe into chronological order by rearranging the index.

# In[571]:

#The following command sorts the rows, first by year, then by month within each year
xlsxfile = xlsxfile.sort_values(by=['year','month'])

xlsxfile = reset_ind(xlsxfile)

print(xlsxfile[:3])
print(xlsxfile[-5:])


# The last 4 values for UNRATE are nonexistent, since data for those months aren't available yet. So, the last thing we'll do to clean this file is drop those missing values.

# In[572]:

xlsxfile = xlsxfile.drop(xlsxfile.index[128:])

#UNRATE is currently a string, so let's make it an int variable
xlsxfile.UNRATE = to_num(xlsxfile.UNRATE)


# We now have no more missing values, our index is in chronological order, and our variables are all numerical now. So now, let's describe our data.

# ### Describing The XLSX File

# In[573]:

xlsxfile.describe()


# Notice that a much larger portion of this dataset involves the Recession than in the csv file and as a result, this dataset has a much higher mean than the first. This data's standard deviation is also higher.

# Let's look at other percentiles

# In[574]:

xlsxfile.describe(percentiles=[.01,.05,.95,.99])


# Notice that once again, the unemployment rate is the only particularly interesting variable described in the above two tables.

# Let's look at our correlation coefficients now.

# In[575]:

xlsxfile.corr()


# The correlation between unemployment and the year is negative for the past decade.

# Now let's divide up our data into before and after 2013 (I choose 2013 to divide the data into a "Recession" part and a "post-Recession" part), and see the differences in the two time periods' unemployment rates.

# In[576]:

#Create an indicator called "late" for whether or not a certain observation is before or after 2012
xlsxfile = split_years(xlsxfile, 2013)


# In[577]:

xlsxfile.groupby('late')['UNRATE'].describe()


# The mean unemployment in the "Recession" part is 8.3%, and the median is 8.9%! Those are really high numbers. There is a point in that period where the rate is 4.9%, but that was the best it got.
# 
# Meanwhile, the "post-Recession" part isn't so bad. Its mean is at about 5.4%, much better than the first period. Furthermore, the second period's median is even lower than its own mean.

# ### Visualizing The XLSX File

# Now let's visualize our data, using the 5 graphs I used before. I will make comments in between plots, which is why I have forgone making a function to run through all 5 at once.

# In[578]:

#Scatter plot
sns.lmplot(x="year", y="UNRATE", data=xlsxfile)


# We see here and in the next several plots that during these ten years, unemployment rates seem to rise rapidly in 2008 and 2009, then begin to fall until in 2018, we see lower rates than we saw at the beginning of 2008. 
# 
# The regression line shows a strong negative correlation between years and unemployment.

# In[579]:

#Histogram
sns.distplot(xlsxfile.UNRATE, kde=True)


# In this histogram, we see an interesting contrast to the csv file. In that file, the unemployment rate values were concentrated in the middle, around 6%. Here, we actually see rates concentrated along both extremes, between 4% and 5% and between 9% and 10%.

# In[580]:

#Joint plot
sns.jointplot(xlsxfile.year, xlsxfile.UNRATE, kind="hex")


# In[581]:

#Line chart
plt.plot(xlsxfile['year'],xlsxfile['UNRATE'])


# Here we see lines traced out to estimate the changes in unemployment from year to year. This line graph shows us the same trend discussed above.

# In[582]:

#Heat map
data = xlsxfile.pivot("month", "year", "UNRATE")
f, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(data, annot=False, linewidths=.5, ax=ax, cmap='Blues')


# This heat map is very appealing to the eyes, in my opinion -- and is still easily intuitive. An extra advantage to this plot is that it shows months and years. It is clear that unemployment shot up between the end of 2008 and early 2009, and then it stayed high for years. Only in 2015 do unemployment levels return to the level they were at before the Recession.

# ### Cleaning The TXT File

# We now begin to analyze our txt file. 

# First, let's make it so the columns get their variables from the first row.

# In[583]:

txtfile = var_adopt(txtfile)

txtfile[:3]


# Now let's look for missing values in the data.

# In[584]:

txtfile.columns[txtfile.isnull().any()]


# There aren't any.

# Let's make sure all variables become numbers.

# In[589]:

for column in txtfile:
    txtfile[column] = to_num(txtfile[column])


# Let's see if there are any outliers by finding summary statistics.

# In[590]:

txtfile.describe()


# There are so many variables that some variables are cut from the above table, so lets look at minimum and maximum of all the variables.

# In[591]:

txtfile.max()


# Seeing as this is crime data, these maxima are unfortunate, but they don't look too high. Just to test total_arrests, let's see what the value of 3 times total_arrest's standard deviation would be and add that to its mean.

# In[592]:

std_dev = txtfile['total_arrests'].std()

max_outlier = txtfile['total_arrests'].mean() + (std_dev * 3)
max_outlier


# This is greater than the maximum, so let's keep all our observations for total_arrests. Since no individual category comes near the total number's maximum, it makes sense that their maxima are correct, too.
# 
# Let's check the minima now.

# In[593]:

txtfile.min()


# Again, nothing calls my attention here. So, let's conclude that there are no outliers and continue with our analysis.

# This file was pretty clean, but since we had to do some work in the beginning to get the variables right and we did a thorough check for outliers and missing values, let's move on to the description part of our analysis.

# ### Describing The TXT File

# We've already seen summary statistics for the data, so let's look at the summary statistics using extreme percentiles.

# In[603]:

txtfile.describe(percentiles=[.01,.05,.95,.99])


# Now let's take a look at correlations.

# In[600]:

txtfile.corr()


# This shows some good news! Total arrests, homicides, rapes, DUI's, and most other crimes are strongly, negatively correlated with year.
# 
# There is only one crime that is positively correlated with year. Drug abuse is weakly, but positively correlated with year. Which is certainly not good news.
# 
# There are also interesting relationships between crimes. Homicide, aggravated assault, and rape, for example are highly, positively correlated with each other. Again, the crime that seems to have the least correlation with other crimes is drug abuse.

# I couldn't see the correlation between drug abuse and DUI. Let's look at that.

# In[602]:

txtfile['drug_abuse'].corr(txtfile['dui'])


# So there is a positive relationship (about .33), but it's not nearly as strong as the ones I mentioned just above.

# ### Visualizing The TXT File

# Now let's visualize the data in this file.

# First, let's take a look at total arrests over time.

# In[604]:

sns.lmplot(x="year", y="total_arrests", data=txtfile)


# The path hasn't been perfectly smooth, but there is a clear decline in total_arrests over the given years.

# Has the path of homicides over time been similar?

# In[605]:

sns.lmplot(x="year", y="homicide", data=txtfile)


# What about rapes?

# In[606]:

sns.lmplot(x="year", y="rape", data=txtfile)


# Aggravated assault?

# In[607]:

sns.lmplot(x="year", y="aggravated_assault", data=txtfile)


# Notice that all three types of crimes follow the same downward trend as total arrests. That is, until about 2013, when all three jump up and continue to rise for the next three years. Could it be that we are on a new path towards more brutal crime, despite the fall in arrests?

# Let's take a look at drug abuse now.

# In[608]:

sns.lmplot(x="year", y="drug_abuse", data=txtfile)


# That's a really interesting pattern. Let's look at a line graph of that trend.

# In[609]:

plt.plot(txtfile['year'],txtfile['drug_abuse'])


# Now the trend is easier to discern. There seems to have been a huge spike in drug abuse arrests between about 2002 and 2011. Before and after that spike, there seems to be a trend to fluctuate between about 1.5 and 1.6 million cases. At the height of the spike, around 2006, there were nearly 1.9 million cases.

# Hence, there is good news and bad news in this data. The good news is that arrests have been going down over the past decade, and that drug abuse has fallen from its peak.
# 
# The bad news is that drug abuse could rise again and has been somewhat positively correlated with time. Also, murders, rapes, and aggravated assaults have risen over the past 5 years, which is an extremely worrisome trend.

# In[ ]:



