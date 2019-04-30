#!/usr/bin/env python
# coding: utf-8

# ## World Progress

# In this project, you'll explore data from [Gapminder.org](http://gapminder.org), a website dedicated to providing a fact-based view of the world and how it has changed. That site includes several data visualizations and presentations, but also publishes the raw data that we will use in this project to recreate and extend some of their most famous visualizations.
# 
# The Gapminder website collects data from many sources and compiles them into tables that describe many countries around the world. All of the data they aggregate are published in the [Systema Globalis](https://github.com/open-numbers/ddf--gapminder--systema_globalis/blob/master/README.md). Their goal is "to compile all public statistics; Social, Economic and Environmental; into a comparable total dataset." All data sets in this project are copied directly from the Systema Globalis without any changes.
# 
# This project is dedicated to [Hans Rosling](https://en.wikipedia.org/wiki/Hans_Rosling) (1948-2017), who championed the use of data to understand and prioritize global development challenges.

# ### Logistics
# 
# **Deadline.** This project is due at 11:59pm on Friday 3/1. Projects will be accepted up to 2 days (48 hours) late; a project submitted less than 24 hours after the deadline will receive 2/3 credit, a project submitted between 24 and 48 hours after the deadline will receive 1/3 credit, and a project submitted 48 hours or more after the deadline will receive no credit. It's **much** better to be early than late, so start working now.
# 
# **Checkpoint.** For full credit, you must also complete the first 8 questions and submit them by 11:59pm on Friday 2/22. You will have some lab time to work on these questions, but we recommend that you start the project before lab and leave time to finish the checkpoint afterward.
# 
# **Partners.** You may work with one other partner; your partner must be from your assigned lab section. Only one of you is required to submit the project. On [okpy.org](http://okpy.org), the person who submits should also designate their partner so that both of you receive credit.
# 
# **Rules.** Don't share your code with anybody but your partner. You are welcome to discuss questions with other students, but don't share the answers. The experience of solving the problems in this project will prepare you for exams (and life). If someone asks you for the answer, resist! Instead, you can demonstrate how you would solve a similar problem.
# 
# **Support.** You are not alone! Come to office hours, post on Piazza, and talk to your classmates. If you want to ask about the details of your solution to a problem, make a private Piazza post and the staff will respond. If you're ever feeling overwhelmed or don't know how to make progress, email your TA or tutor for help. You can find contact information for the staff on the [course website](http://data8.org/sp19/staff.html).
# 
# **Tests.** The tests that are given are **not comprehensive** and passing the tests for a question **does not** mean that you answered the question correctly. Tests usually only check that your table has the correct column labels. However, more tests will be applied to verify the correctness of your submission in order to assign your final score, so be careful and check your work! You might want to create your own checks along the way to see if your answers make sense. Additionally, before you submit, make sure that none of your cells take a very long time to run (several minutes).
# 
# **Free Response Questions:** Make sure that you put the answers to the written questions in the indicated cell we provide. Check to make sure that you have a [Gradescope](http://gradescope.com) account, which is where the scores to the free response questions will be posted. If you do not, make sure to reach out to your assigned (u)GSI.
# 
# **Advice.** Develop your answers incrementally. To perform a complicated table manipulation, break it up into steps, perform each step on a different line, give a new name to each result, and check that each intermediate result is what you expect. You can add any additional names or functions you want to the provided cells. Make sure that you are using distinct and meaningful variable names throughout the notebook. Along that line, **DO NOT** reuse the variable names that we use when we grade your answers. For example, in Question 1 of the Global Poverty section, we ask you to assign an answer to `latest`. Do not reassign the variable name `latest` to anything else in your notebook, otherwise there is the chance that our tests grade against what `latest` was reassigned to.
# 
# You **never** have to use just one line in this project or any others. Use intermediate variables and multiple lines as much as you would like!  
# 
# To get started, load `datascience`, `numpy`, `plots`, and `ok`.

# In[1]:


from datascience import *
import numpy as np

get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plots
plots.style.use('fivethirtyeight')

from client.api.notebook import Notebook
ok = Notebook('project1.ok')


# Before continuing the assignment, select "Save and Checkpoint" in the File menu and then execute the submit cell below. The result will contain a link that you can use to check that your assignment has been submitted successfully. If you submit more than once before the deadline, we will only grade your final submission. If you mistakenly submit the wrong one, you can head to okpy.org and flag the correct version. There will be another submit cell at the end of the assignment when you finish!

# In[2]:


_ = ok.submit()


# ## 1. Global Population Growth
# 

# The global population of humans reached 1 billion around 1800, 3 billion around 1960, and 7 billion around 2011. The potential impact of exponential population growth has concerned scientists, economists, and politicians alike.
# 
# The UN Population Division estimates that the world population will likely continue to grow throughout the 21st century, but at a slower rate, perhaps reaching 11 billion by 2100. However, the UN does not rule out scenarios of more extreme growth.
# 
# <a href="http://www.pewresearch.org/fact-tank/2015/06/08/scientists-more-worried-than-public-about-worlds-growing-population/ft_15-06-04_popcount/"> 
#  <img src="pew_population_projection.png"/> 
# </a>
# 
# In this section, we will examine some of the factors that influence population growth and how they are changing around the world.
# 
# The first table we will consider is the total population of each country over time. Run the cell below.

# In[3]:


population = Table.read_table('population.csv')
population.show(3)


# **Note:** The population csv file can also be found [here](https://github.com/open-numbers/ddf--gapminder--systema_globalis/raw/master/ddf--datapoints--population_total--by--geo--time.csv). The data for this project was downloaded in February 2017.

# ### Bangladesh
# 
# In the `population` table, the `geo` column contains three-letter codes established by the [International Organization for Standardization](https://en.wikipedia.org/wiki/International_Organization_for_Standardization) (ISO) in the [Alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3#Current_codes) standard. We will begin by taking a close look at Bangladesh. Inspect the standard to find the 3-letter code for Bangladesh.

# **Question 1.** Create a table called `b_pop` that has two columns labeled `time` and `population_total`. The first column should contain the years from 1970 through 2015 (including both 1970 and 2015) and the second should contain the population of Bangladesh in each of those years.

# In[4]:


temp = np.arange(1970, 2016)
bgd = ["bgd"]
holder = population.where("geo", are.contained_in(bgd))
b_pop = holder.where("time", are.contained_in(temp))
b_pop = b_pop.drop("geo")
b_pop


# In[5]:


_ = ok.grade('q1_1')


# Run the following cell to create a table called `b_five` that has the population of Bangladesh every five years. At a glance, it appears that the population of Bangladesh has been growing quickly indeed!

# In[6]:


b_pop.set_format('population_total', NumberFormatter)

fives = np.arange(1970, 2016, 5) # 1970, 1975, 1980, ...
b_five = b_pop.sort('time').where('time', are.contained_in(fives))
b_five


# **Question 2.** Assign `b_1970_through_2010` to a table that has the same columns as `b_five` and has one row for every five years from 1970 through 2010 (but not 2015). Then, use that table to assign `initial` to an array that contains the population for every five year interval from 1970 to 2010. Finally, assign `changed` to an array that contains the population for every five year interval from 1975 to 2015.
# 
# *Hint*: You may find the `exclude` method to be helpful ([Docs](http://data8.org/datascience/_autosummary/datascience.tables.Table.exclude.html)).

# In[7]:


b_1970_through_2010 = b_five.where("time", are.contained_in(np.arange(1970, 2015, 5)))
initial = b_1970_through_2010.column("population_total")
changed = b_five.where("time", are.above_or_equal_to(1975)).column("population_total")


# We have provided the code below that uses `b_1970_through_2010`, `initial`, and `changed` in order to add a column to the table called `annual_growth`. Don't worry about the calculation of the growth rates; run the test below to test your solution.
# 
# If you are interested in how we came up with the formula for growth rates, consult the [growth rates](https://www.inferentialthinking.com/chapters/03/2/1/growth) section of the textbook.

# In[8]:


b_five_growth = b_1970_through_2010.with_column('annual_growth', (changed/initial)**0.2-1)
b_five_growth.set_format('annual_growth', PercentFormatter)


# In[9]:


_ = ok.grade('q1_2')


# While the population has grown every five years since 1970, the annual growth rate decreased dramatically from 1985 to 2005. Let's look at some other information in order to develop a possible explanation. Run the next cell to load three additional tables of measurements about countries over time.

# In[10]:


life_expectancy = Table.read_table('life_expectancy.csv')
child_mortality = Table.read_table('child_mortality.csv').relabel(2, 'child_mortality_under_5_per_1000_born')
fertility = Table.read_table('fertility.csv')


# The `life_expectancy` table contains a statistic that is often used to measure how long people live, called *life expectancy at birth*. This number, for a country in a given year, [does not measure how long babies born in that year are expected to live](http://blogs.worldbank.org/opendata/what-does-life-expectancy-birth-really-mean). Instead, it measures how long someone would live, on average, if the *mortality conditions* in that year persisted throughout their lifetime. These "mortality conditions" describe what fraction of people at each age survived the year. So, it is a way of measuring the proportion of people that are staying alive, aggregated over different age groups in the population.

# Run the following cells below to see `life_expectancy`, `child_mortality`, and `fertility`. Refer back to these tables as they will be helpful for answering further questions!

# In[11]:


life_expectancy


# In[12]:


child_mortality


# In[13]:


fertility


# **Question 3.** Perhaps population is growing more slowly because people aren't living as long. Use the `life_expectancy` table to draw a line graph with the years 1970 and later on the horizontal axis that shows how the *life expectancy at birth* has changed in Bangladesh.

# In[14]:


bgd_graph = life_expectancy.where("geo", are.equal_to("bgd"))
bgd_graph = bgd_graph.where("time", are.above_or_equal_to(1970))
bgd_graph.plot("time", "life_expectancy_years")


# **Question 4.** Assuming everything else stays the same, does the graph above help directly explain why the population growth rate decreased from 1985 to 2010 in Bangladesh? Why or why not? What happened in Bangladesh in 1991, and does that event explain the change in population growth rate?

# The graph above doesn't explain why the population growth rate decreased from 1985 to 2010 in Bangladesh because though a drop in the rate is present around 1991, the graph shows a steadily increasing trend. In 1991, Bangladesh had a cyclone, which could explain the resulting dip in the graph but still doesn't explain the assocition between life expectancy and population growth rate.

# The `fertility` table contains a statistic that is often used to measure how many babies are being born, the *total fertility rate*. This number describes the [number of children a woman would have in her lifetime](https://www.measureevaluation.org/prh/rh_indicators/specific/fertility/total-fertility-rate), on average, if the current rates of birth by age of the mother persisted throughout her child bearing years, assuming she survived through age 49. 

# **Question 5.** Write a function `fertility_over_time` that takes the Alpha-3 code of a `country` and a `start` year. It returns a two-column table with labels `Year` and `Children per woman` that can be used to generate a line chart of the country's fertility rate each year, starting at the `start` year. The plot should include the `start` year and all later years that appear in the `fertility` table. 
# 
# Then, in the next cell, call your `fertility_over_time` function on the Alpha-3 code for Bangladesh and the year 1970 in order to plot how Bangladesh's fertility rate has changed since 1970. Note that the function `fertility_over_time` should not return the plot itself. **The expression that draws the line plot is provided for you; please don't change it.**

# In[15]:


def fertility_over_time(country, start):
    """Create a two-column table that describes a country's total fertility rate each year."""
    country_fertility = fertility.where("geo", are.equal_to(country))
    country_fertility_after_start = country_fertility.where("time", are.above_or_equal_to(start)).drop("geo")
    return Table().with_columns("Year", country_fertility_after_start.column("time"), "Children per woman", country_fertility_after_start.column("children_per_woman_total_fertility"))
    
    
    
    
    


# In[16]:


bangladesh_code = "bgd"
fertility_over_time(bangladesh_code, 1970).plot(0, 1) # You should *not* change this line.


# In[17]:


_ = ok.grade('q1_5')


# **Question 6.** Assuming everything else is constant, does the graph above help directly explain why the population growth rate decreased from 1985 to 2010 in Bangladesh? Why or why not?

# The graph above does help directly explain why the population growth rate decreased from 1985 to 2010 as it shows a decreasing trend in fertility over the years. However, it is important to remember that this doesn't show a direct explanation for the decreased population growth, but rather, an association between the two. There could still be confounding variables present that need to be controlled for before concluding the cause of the phenomenon.

# It has been observed that lower fertility rates are often associated with lower child mortality rates. The link has been attributed to family planning: if parents can expect that their children will all survive into adulthood, then they will choose to have fewer children. We can see if this association is evident in Bangladesh by plotting the relationship between total fertility rate and [child mortality rate per 1000 children](https://en.wikipedia.org/wiki/Child_mortality).

# **Question 7.** Using both the `fertility` and `child_mortality` tables, draw a scatter diagram with one point for each year, starting with 1970, that has Bangladesh's total fertility on the horizontal axis and its child mortality on the vertical axis. 
# 
# **The expression that draws the scatter diagram is provided for you; please don't change it.** Instead, create a table called `post_1969_fertility_and_child_mortality` with the appropriate column labels and data in order to generate the chart correctly. Use the label `Children per woman` to describe total fertility and the label `Child deaths per 1000 born` to describe child mortality.

# In[18]:


bgd_fertility = fertility.where("geo", are.equal_to("bgd"))
bgd_child_mortality = child_mortality.where("geo", are.equal_to("bgd"))
fertility_and_child_mortality = bgd_fertility.join("time", bgd_child_mortality, "time")
post_1969_fertility_and_child_mortality = fertility_and_child_mortality.where("time", are.above_or_equal_to(1970)).drop("geo_2").relabeled("children_per_woman_total_fertility", "Children per woman")
post_1969_fertility_and_child_mortality = post_1969_fertility_and_child_mortality.relabeled('child_mortality_under_5_per_1000_born', 'Child deaths per 1000 born')
post_1969_fertility_and_child_mortality.scatter('Children per woman', 'Child deaths per 1000 born') # You should not change this line.


# In[19]:


_ = ok.grade('q1_7')


# **Question 8.** In one or two sentences, describe the association (if any) that is illustrated by this scatter diagram. Does the diagram show that reduced child mortality causes parents to choose to have fewer children?

# The diagram displays a strong positive correlation between child mortality and thechildren per woman. Thus, we can infer that reduced child mortality resutls in a reduction in the number of children per woman, which could potentially explain the decreasing growth rate.

# ### The World
# 
# The change observed in Bangladesh since 1970 can also be observed in many other developing countries: health services improve, life expectancy increases, and child mortality decreases. At the same time, the fertility rate often plummets, and so the population growth rate decreases despite increasing longevity.

# Run the cell below to generate two overlaid histograms, one for 1960 and one for 2010, that show the distributions of total fertility rates for these two years among all 201 countries in the `fertility` table.

# In[20]:


Table().with_columns(
    '1960', fertility.where('time', 1960).column(2),
    '2010', fertility.where('time', 2010).column(2)
).hist(bins=np.arange(0, 10, 0.5), unit='child')
_ = plots.xlabel('Children per woman')
_ = plots.xticks(np.arange(10))


# **Question 9.** Assign `fertility_statements` to a list of the numbers of each statement below that can be correctly inferred from these histograms.
# 1. About the same number of countries had a fertility rate between 3.5 and 4.5 in both 1960 and 2010.
# 1. In 2010, about 40% of countries had a fertility rate between 1.5 and 2 (inclusive).
# 1. In 1960, less than 20% of countries had a fertility rate below 3.
# 1. More countries had a fertility rate above 3 in 1960 than in 2010.
# 1. At least half of countries had a fertility rate between 5 and 8 (inclusive) in 1960.
# 1. At least half of countries had a fertility rate below 3 in 2010.

# In[21]:


fertility_statements = [4, 5, 6]


# In[22]:


_ = ok.grade('q1_9')


# **Question 10.** Draw a line plot of the world population from 1800 through 2005. The world population is the sum of all the country's populations. 

# In[23]:


world_pop_by_year = population.drop("geo")
world_pop_by_year = world_pop_by_year.where("time", are.between_or_equal_to(1800,2005)).group("time", sum)
world_pop_by_year.plot("time")


# **Question 11.** Create a function `stats_for_year` that takes a `year` and returns a table of statistics. The table it returns should have four columns: `geo`, `population_total`, `children_per_woman_total_fertility`, and `child_mortality_under_5_per_1000_born`. Each row should contain one Alpha-3 country code and three statistics: population, fertility rate, and child mortality for that `year` from the `population`, `fertility` and `child_mortality` tables. Only include rows for which all three statistics are available for the country and year.
# 
# In addition, restrict the result to country codes that appears in `big_50`, an array of the 50 most populous countries in 2010. This restriction will speed up computations later in the project.
# 
# *Hint*: The tests for this question are quite comprehensive, so if you pass the tests, your function is probably correct. However, without calling your function yourself and looking at the output, it will be very difficult to understand any problems you have, so try your best to write the function correctly and check that it works before you rely on the `ok` tests to confirm your work.

# In[24]:


# We first create a population table that only includes the 
# 50 countries with the largest 2010 populations. We focus on 
# these 50 countries only so that plotting later will run faster.
big_50 = population.where('time', 2010).sort(2, descending=True).take(np.arange(50)).column('geo')
population_of_big_50 = population.where('time', are.above(1959)).where('geo', are.contained_in(big_50))

def stats_for_year(year):
    """Return a table of the stats for each country that year."""
    p = population_of_big_50.where('time', year).drop('time')
    f = fertility.where('time', year).drop('time')
    c = child_mortality.where('time', year).drop('time')
    p = p.join("geo", f, "geo").join("geo", c, "geo")
    return p


# Try calling your function `stats_for_year` on any year between 1960 and 2010 in the cell below.  Try to understand the output of `stats_for_year`.

# In[25]:


stats_for_year(1980)


# In[26]:


_ = ok.grade('q1_11')


# **Question 12.** Create a table called `pop_by_decade` with two columns called `decade` and `population`. It has a row for each `year` since 1960 that starts a decade. The `population` column contains the total population of all countries included in the result of `stats_for_year(year)` for the first `year` of the decade. For example, 1960 is the first year of the 1960's decade. You should see that these countries contain most of the world's population.
# 
# *Hint:* One approach is to define a function `pop_for_year` that computes this total population, then `apply` it to the `decade` column.  The `stats_for_year` function from the previous question may be useful here.
# 
# **Note:** The `pop_by_decade` cell is directly below the cell containing the helper function `pop_for_year`. This is where you will generate the `pop_by_decade` table!

# In[27]:


def pop_for_year(year):
    return sum((stats_for_year(year))["population_total"])


# This test is just a sanity check for your helper function if you choose to use it. You will not lose points for not implementing the function `pop_for_year`.

# In[28]:


_ = ok.grade('q1_12_0')


# In[29]:


decades = Table().with_column('decade', np.arange(1960, 2011, 10))
holder = np.arange(1960, 2011, 10)
for i in range(len(holder)):
    holder[i] = pop_for_year(holder[i])
pop_by_decade = decades.with_column("population", holder)
pop_by_decade.set_format(1, NumberFormatter)


# In[30]:


_ = ok.grade('q1_12')


# The `countries` table describes various characteristics of countries. The `country` column contains the same codes as the `geo` column in each of the other data tables (`population`, `fertility`, and `child_mortality`). The `world_6region` column classifies each country into a region of the world. Run the cell below to inspect the data.

# In[31]:


countries = Table.read_table('countries.csv').where('country', are.contained_in(population.group('geo').column(0)))
countries.select('country', 'name', 'world_6region')


# **Question 13.** Create a table called `region_counts` that has two columns, `region` and `count`. It should describe the count of how many countries in each region appear in the result of `stats_for_year(1960)`. For example, one row would have `south_asia` as its `world_6region` value and an integer as its `count` value: the number of large South Asian countries for which we have population, fertility, and child mortality numbers from 1960.

# In[32]:


holder = stats_for_year(1960).join("geo", countries, "country")
region_counts = (holder.group("geo")).relabeled("geo", "region")
region_counts


# In[33]:


_ = ok.grade('q1_13')


# The following scatter diagram compares total fertility rate and child mortality rate for each country in 1960. The area of each dot represents the population of the country, and the color represents its region of the world. Run the cell. Do you think you can identify any of the dots?

# In[34]:


from functools import lru_cache as cache

# This cache annotation makes sure that if the same year
# is passed as an argument twice, the work of computing
# the result is only carried out once.
@cache(None)
def stats_relabeled(year):
    """Relabeled and cached version of stats_for_year."""
    return stats_for_year(year).relabel(2, 'Children per woman').relabel(3, 'Child deaths per 1000 born')

def fertility_vs_child_mortality(year):
    """Draw a color scatter diagram comparing child mortality and fertility."""
    with_region = stats_relabeled(year).join('geo', countries.select('country', 'world_6region'), 'country')
    with_region.scatter(2, 3, sizes=1, colors=4, s=500)
    plots.xlim(0,10)
    plots.ylim(-50, 500)
    plots.title(year)

fertility_vs_child_mortality(1960)


# **Question 14.** Assign `scatter_statements` to a list of the numbers of each statement below that can be inferred from this scatter diagram for 1960. 
# 1. The `europe_central_asia` region had the lowest child mortality rate.
# 1. The lowest child mortality rate of any country was from an `east_asia_pacific` country.
# 1. Most countries had a fertility rate above 5.
# 1. There was an association between child mortality and fertility.
# 1. The two largest countries by population also had the two highest child mortality rate.

# In[103]:


scatter_statements = [4]


# In[36]:


_ = ok.grade('q1_14')


# The result of the cell below is interactive. Drag the slider to the right to see how countries have changed over time. You'll find that the great divide between so-called "Western" and "developing" countries that existed in the 1960's has nearly disappeared. This shift in fertility rates is the reason that the global population is expected to grow more slowly in the 21st century than it did in the 19th and 20th centuries.
# 
# **Note:** Don't worry if a red warning pops up when running the cell below. You'll still be able to run the cell!

# In[37]:


import ipywidgets as widgets

# This part takes a few minutes to run because it 
# computes 55 tables in advance: one for each year.
Table().with_column('Year', np.arange(1960, 2016)).apply(stats_relabeled, 'Year')

_ = widgets.interact(fertility_vs_child_mortality, 
                     year=widgets.IntSlider(min=1960, max=2015, value=1960))


# Now is a great time to take a break and watch the same data presented by [Hans Rosling in a 2010 TEDx talk](https://www.gapminder.org/videos/reducing-child-mortality-a-moral-and-environmental-imperative) with smoother animation and witty commentary.

# ## 2. Global Poverty
# 

# In 1800, 85% of the world's 1 billion people lived in *extreme poverty*, defined by the United Nations as "a condition characterized by severe deprivation of basic human needs, including food, safe drinking water, sanitation facilities, health, shelter, education and information." A common measure of extreme poverty is a person living on less than \$1.25 per day.
# 
# In 2018, the proportion of people living in extreme poverty was estimated to be 8%. Although the world rate of extreme poverty has declined consistently for hundreds of years, the number of people living in extreme poverty is still over 600 million. The United Nations recently adopted an [ambitious goal](http://www.un.org/sustainabledevelopment/poverty/): "By 2030, eradicate extreme poverty for all people everywhere."
# In this section, we will examine extreme poverty trends around the world.

# First, load the population and poverty rate by country and year and the country descriptions. While the `population` table has values for every recent year for many countries, the `poverty` table only includes certain years for each country in which a measurement of the rate of extreme poverty was available.

# In[38]:


population = Table.read_table('population.csv')
countries = Table.read_table('countries.csv').where('country', are.contained_in(population.group('geo').column(0)))
poverty = Table.read_table('poverty.csv')
poverty.show(3)


# **Question 1.** Assign `latest_poverty` to a three-column table with one row for each country that appears in the `poverty` table. The first column should contain the 3-letter code for the country. The second column should contain the *most recent_poverty_total year* for which an extreme poverty rate is available for the country. The third column should contain the poverty rate in that year. **Do not change the last line, so that the labels of your table are set correctly.**
# 
# *Hint*: think about how ```group``` works: it does a sequential search of the table (from top to bottom) and collects values in the array in the order in which they appear, and then applies a function to that array. The `first` function may be helpful, but you are not required to use it.

# In[39]:


def first(values):
    return values.item(0)


latest_poverty = poverty.sort("time", descending = True).group("geo", first)

latest_poverty.relabel(0, 'geo').relabel(1, 'time').relabel(2, 'poverty_percent') # You should *not* change this line.


# In[40]:


_ = ok.grade('q2_1')


# **Question 2.** Using both `latest_poverty` and `population`, create a four-column table called `recent_poverty_total` with one row for each country in `latest_poverty`. The four columns should have the following labels and contents:
# 1. `geo` contains the 3-letter country code,
# 1. `poverty_percent` contains the most recent poverty percent,
# 1. `population_total` contains the population of the country in 2010,
# 1. `poverty_total` contains the number of people in poverty **rounded to the nearest integer**, based on the 2010 population and most recent poverty rate.

# In[41]:


pop_2010 = population.where("time", are.equal_to(2010))
pop_2010


# In[42]:


holder = np.arange(len(latest_poverty["geo"]))
for i in range(len(latest_poverty["geo"])):
    holder[i] = pop_2010.where("geo", are.equal_to(latest_poverty["geo"][i]))["population_total"].item(0)
poverty_and_pop = latest_poverty.with_column("population_total", holder).drop("time")
recent_poverty_total = poverty_and_pop.with_column("poverty_total", np.round(poverty_and_pop["poverty_percent"] * 0.01 
                                              * poverty_and_pop["population_total"]))
recent_poverty_total


# In[43]:


_ = ok.grade('q2_2')


# **Question 3.** Assuming that the `poverty_total` numbers in the `recent_poverty_total` table describe *all* people in 2010 living in extreme poverty, assign the name `poverty_percent` to the known percentage of the world's 2010 population that were living in extreme poverty. You should find a number that is above the 2018 global estimate of 8%, since many country-specific poverty rates are older than 2018.
# 
# *Hint*: The sum of the `population_total` column in the `recent_poverty_total` table is not the world population, because only a subset of the world's countries have known poverty rates. Use the `population` table to compute the world's 2010 total population.

# In[44]:


poverty_percent = sum(recent_poverty_total["poverty_total"])/sum(pop_2010["population_total"]) * 100
poverty_percent


# In[45]:


_ = ok.grade('q2_3')


# The `countries` table includes not only the name and region of countries, but also their positions on the globe.

# In[46]:


countries.select('country', 'name', 'world_4region', 'latitude', 'longitude')


# **Question 4.** Using both `countries` and `recent_poverty_total`, create a five-column table called `poverty_map` with one row for every country in `recent_poverty_total`.  The four columns should have the following labels and contents:
# 1. `latitude` contains the country's latitude,
# 1. `longitude` contains the country's longitude,
# 1. `name` contains the country's name,
# 1. `region` contains the country's region from the `world_4region` column of `countries`,
# 1. `poverty_total` contains the country's poverty total.

# In[47]:


poverty_map = recent_poverty_total.join("geo", countries,
                                        "country").select("latitude","longitude",
                                                          "name", "world_4region",
                                                          "poverty_total").relabeled("world_4region", "region")
poverty_map


# In[48]:


_ = ok.grade('q2_4')


# Run the cell below to draw a map of the world in which the areas of circles represent the number of people living in extreme poverty. Double-click on the map to zoom in.

# In[49]:


# It may take a few seconds to generate this map.
colors = {'africa': 'blue', 'europe': 'black', 'asia': 'red', 'americas': 'green'}
scaled = poverty_map.with_column(
    'poverty_total', 2e4 * poverty_map.column('poverty_total'),
    'region', poverty_map.apply(colors.get, 'region')
)
Circle.map_table(scaled)


# Although people live in extreme poverty throughout the world (with more than 5 million in the United States), the largest numbers are in Asia and Africa.

# **Question 5.** Assign `largest` to a two-column table with the `name` (not the 3-letter code) and `poverty_total` of the 10 countries with the largest number of people living in extreme poverty.

# In[50]:


largest = poverty_map.sort("poverty_total", descending = True).take(np.arange(10)).drop("latitude", "longitude", "region")
largest


# In[51]:


_ = ok.grade('q2_5')


# **Question 6.** Write a function called `poverty_timeline` that takes **the name of a country** as its argument. It should draw a line plot of the number of people living in poverty in that country with time on the horizontal axis. The line plot should have a point for each row in the `poverty` table for that country. To compute the population living in poverty from a poverty percentage, multiply by the population of the country **in that year**.
# 
# *Hint*: The names within the `poverty_timeline` function correspond to our staff solution, but you don't need to use them. Any way that you want to draw the plot is fine, as long as it generates the correct graph.
# 
# *Hint*: For the `apply` method, if you don't specify a particular column to apply your function on, the whole row is used as an input to the function. Elements inside a row can be accessed using `.item`.
# 
# *Hint:* This question is long. Feel free to create cells and experiment. 

# In[54]:


population #TEST


# In[53]:


poverty #TEST


# In[58]:


#TESTING CODE
temp = poverty.join("geo", countries, "country")
years = temp.where("name", are.equal_to('India'))["time"]
years


# In[121]:


def population_for_country_in_year(row_of_poverty_table):
    """Optional: Define a function to return the population 
    of a country in a year using a row from the poverty table."""
    holder = population.where("geo", are.equal_to(row_of_poverty_table["geo"].item(0)))
    holder = holder.where("time", are.equal_to(row_of_poverty_table["time"].item(0)))
    return holder["population_total"].item(0)

def poverty_timeline(country):
    country_poverty = (poverty.join("geo", countries.select("country", "name"), "country")).where("name", are.equal_to(country))
    poverty_rates = country_poverty["extreme_poverty_percent_people_below_125_a_day"] * 0.01
    population_rows = population.where("geo", are.equal_to(country_poverty["geo"].item(0)))
    poverty_pop_temp2 = country_poverty.join("time", population_rows, "time")
    poverty_pop_final = poverty_pop_temp2.with_column("poverty pop", 
                                                     poverty_rates * poverty_pop_temp2["population_total"])
    return poverty_pop_final.plot("time", "poverty pop")
    


# Finally, draw the timelines below to see how the world is changing. You can check your work by comparing your graphs to the ones on [gapminder.org](https://goo.gl/lPujuh).

# In[122]:


poverty_timeline('India')


# In[123]:


poverty_timeline('Nigeria')


# In[124]:


poverty_timeline('China')


# In[125]:


poverty_timeline('United States')


# Although the number of people living in extreme poverty has been increasing in Nigeria and the United States, the massive decreases in China and India have shaped the overall trend that extreme poverty is decreasing worldwide, both in percentage and in absolute number. 
# 
# To learn more, watch [Hans Rosling in a 2015 film](https://www.gapminder.org/videos/dont-panic-end-poverty/) about the UN goal of eradicating extreme poverty from the world. 
# 
# Below, we've also added an interactive dropdown menu for you to visualize `poverty_timeline` graphs for other countries. Note that each dropdown menu selection may take a few seconds to run.

# In[126]:


# Just run this cell

all_countries = poverty_map.column('name')
_ = widgets.interact(poverty_timeline, country=list(all_countries))


# **You're finished!** Congratulations on mastering data visualization and table manipulation. Time to submit.

# In[127]:


_ = ok.submit()


# In[ ]:




