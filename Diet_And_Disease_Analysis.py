#!/usr/bin/env python
# coding: utf-8

# In[26]:


# Initialize OK
from client.api.notebook import Notebook
ok = Notebook('project2.ok')


# # Project 2: Diet and Disease

# In this project, you will investigate the major causes of death in the world, as well as how one of these causes, heart disease, might be linked to diet!

# ### Logistics
# 
# 
# **Deadline.** This project is due at 11:59pm on Friday, 4/12. It's **much** better to be early than late, so start working now.
# 
# **Checkpoint.** For full credit, you must also complete the questions up until the end of Part 2 and submit them by 11:59pm on Friday, 4/5. You will have some lab time to work on these questions, but we recommend that you start the project before lab and leave time to finish the checkpoint afterward.
# 
# **Partners.** You may work with one other partner. Your partner must be enrolled in the same lab as you are. Only one of you is required to submit the project. On [okpy.org](http://okpy.org), the person who submits should also designate their partner so that both of you receive credit.
# 
# **Rules.** Don't share your code with anybody but your partner. You are welcome to discuss questions with other students, but don't share the answers. The experience of solving the problems in this project will prepare you for exams (and life). If someone asks you for the answer, resist! Instead, you can demonstrate how you would solve a similar problem.
# 
# **Support.** You are not alone! Come to office hours, post on Piazza, and talk to your classmates. If you want to ask about the details of your solution to a problem, make a private Piazza post and the staff will respond. If you're ever feeling overwhelmed or don't know how to make progress, email your TA or tutor for help. You can find contact information for the staff on the [course website](http://data8.org/sp19/staff.html).
# 
# **Tests.** Passing the tests for a question **does not** mean that you answered the question correctly. Tests usually only check that your table has the correct column labels. However, more tests will be applied to verify the correctness of your submission in order to assign your final score, so be careful and check your work!
# 
# **Advice.** Develop your answers incrementally. To perform a complicated table manipulation, break it up into steps, perform each step on a different line, give a new name to each result, and check that each intermediate result is what you expect. You can add any additional names or functions you want to the provided cells. 
# 
# All of the concepts necessary for this project are found in the textbook. If you are stuck on a particular problem, reading through the relevant textbook section often will help clarify the concept.
# 
# To get started, load `datascience`, `numpy`, `plots`, and `ok`.

# In[28]:


from datascience import *
import numpy as np

get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plots
plots.style.use('fivethirtyeight')
np.set_printoptions(legacy='1.13')

from client.api.notebook import Notebook
ok = Notebook('project2.ok')
_ = ok.auth(inline=True)


# # Diet and Cardiovascular Disease

# In the following analysis, we will investigate the world's most dangerous killer: Cardiovascular Disease. Your investigation will take you across decades of medical research, and you'll look at multiple causes and effects across two different studies.

# Here is a roadmap for this project:
# 
# * In Part 1, we'll investigate the major causes of death in the world during the past century (from 1900 to 2015).
# * In Part 2, we'll look at data from the Framingham Heart Study, an observational study into cardiovascular health.
# * In Part 3, we'll examine a claim from the Nurses' Health Study that hormone replacement therapy reduces the risk of coronary heart disease for post-menopausal women.
# * In Part 4, we'll run a hypothesis test on data based on the results of the Heart and Estrogen-Progestin Replacement Study.

# ## Part 1: Causes of Death 

# In order to get a better idea of how we can most effectively prevent deaths, we need to first figure out what the major causes of death are. Run the following cell to read in and view the `causes_of_death` table, which documents the death rate for major causes of deaths over the last century (1900 until 2015).

# In[29]:


causes_of_death = Table.read_table('causes_of_death.csv')
causes_of_death.show(5)


# Each entry in the column **Age Adjusted Death Rate** is a death rate for a specific **Year** and **Cause** of death. 
# 
# The **Age Adjusted** specification in the death rate column tells us that the values shown are the death rates that would have existed if the population under study in a specific year had the same age distribution as the "standard" population, a baseline. This is so we can compare ages across years without worrying about changes in the demographics of our population.

# **Question 1:** What are all the different causes of death in this dataset? Assign an array of all the unique causes of death to `all_unique_causes`.
# 
# 
# <!--
# BEGIN QUESTION
# name: q1_1
# manual: false
# -->

# In[30]:


all_unique_causes = np.unique(causes_of_death.column("Cause"))
sorted(all_unique_causes)


# In[31]:


ok.grade("q1_1");


# In[32]:


# This function may be useful for Question 2.
def elem(x):
    return x.item(0)


# **Question 2:** We would like to plot the death rate for each disease over time. To do so, we must create a table with one column for each cause and one row for each year.
# 
# Create a table called `causes_for_plotting`. It should have one column called `Year`, and then a column with age-adjusted death rates for each of the causes you found in Question 1. There should be as many of these columns in `causes_for_plotting` as there are causes in Question 1.
# 
# *Hint*: Use `pivot`, and think about how the `elem` function might be useful in getting the **Age Adjusted Death Rate** for each cause and year combination.
# 
# <!--
# BEGIN QUESTION
# name: q1_2
# manual: false
# -->

# In[33]:


causes_for_plotting = causes_of_death.pivot("Cause", "Year", "Age Adjusted Death Rate", elem)
causes_for_plotting


# Run the cell below to see what a plot of the data would have looked like had you been living in 1950! CHD was the leading cause of death and had killed millions of people without warning. It had become twice as lethal in just a few decades and people didn't understand why this was happening.
# 
# 

# In[34]:


# Do not change this line
causes_for_plotting.where('Year', are.below_or_equal_to(1950)).plot('Year')


# The view from 2016 looks a lot less scary, however, since we know it eventually went down. The decline in CHD deaths is one of the greatest public health triumphs of the last half century. That decline represents many millions of saved lives, and it was not inevitable. The Framingham Heart Study, in particular, was the first to discover the associations between heart disease and risk factors like smoking, high cholesterol, high blood pressure, obesity, and lack of exercise.

# In[35]:


# Do not change this line
causes_for_plotting.plot('Year')


# Let's examine the graph above. You'll see that in the 1960s, the death rate due to heart disease steadily declines. Up until then, the effects of smoking, blood pressure, and diet on the cardiovascular system were unknown to researchers. Once these factors started to be noticed, doctors were able recommend a lifestyle change for at-risk patients to prevent heart attacks and heart problems.
# 
# Note, however, that the death rate for heart disease is still higher than the death rates of all other causes. Even though the death rate is starkly decreasing, there's still a lot we don't understand about the causes (both direct and indirect) of heart disease.

# ## Part 2: The Framingham Heart Study

# The [Framingham Heart Study](https://en.wikipedia.org/wiki/Framingham_Heart_Study) is an observational study of cardiovascular health. The initial study followed over 5,000 volunteers for several decades, and followup studies even looked at their descendants. In this section, we'll investigate some of its key findings about diet, cholesterol, and heart disease.
# 
# Run the cell below to examine data for almost 4,000 subjects from the first wave of the study, collected in 1956.

# In[36]:


framingham = Table.read_table('framingham.csv')
framingham


# Each row contains data from one subject. The first seven columns describe the subject at the time of their initial medical exam at the start of the study. The last column, `ANYCHD`, tells us whether the subject developed some form of heart disease at any point after the start of the study.
# 
# You may have noticed that the table contains fewer rows than subjects in the original study: this is because we are excluding subjects who already had heart disease as well as subjects with missing data.

# ### Section 1: Diabetes and the population

# Before we begin our investigation into cholesterol, we'll first look at some limitations of this dataset. In particular, we will investigate ways in which this is or isn't a representative sample of the population by examining the number of subjects with diabetes.
# 
# [According to the CDC](https://www.cdc.gov/diabetes/statistics/slides/long_term_trends.pdf), the prevalence of diagnosed diabetes (i.e., the percentage of the population who have it) in the U.S. around this time was 0.93%. We are going to conduct a hypothesis test with the following null and alternative hypotheses:
# 
# **Null Hypothesis**: The probability that a participant within the Framingham Study has diabetes is equivalent to the prevalence of diagnosed diabetes within the population. (i.e., any difference is due to chance).
# 
# **Alternative Hypothesis**: The probability that a participant within the Framingham Study has diabetes is different than the prevalence of diagnosed diabetes within the population.
# 
# We are going to use the absolute distance between the observed prevalence and the true population prevalence as our test statistic. The column `DIABETES` in the `framingham` table contains a 1 for subjects with diabetes and a `0` for those without.

# **Question 1**: What is the observed value of the statistic in the data from the Framingham Study? You should convert prevalences to proportions before calculating the statistic!
# 
# <!--
# BEGIN QUESTION
# name: q2_1_1
# manual: false
# -->

# In[37]:


observed_diabetes_distance = abs(np.average(framingham["DIABETES"] - 0.0093))
observed_diabetes_distance


# In[38]:


ok.grade("q2_1_1");


# **Question 2**: Define the function `diabetes_statistic` which should return exactly one simulated statistic under the null hypothesis of the absolute distance between the observed prevalence and the true population prevalence.
# 
# <!--
# BEGIN QUESTION
# name: q2_1_2
# manual: false
# -->

# In[39]:


diabetes_proportions = make_array(.9907, .0093)

def diabetes_statistic():
    return abs(sample_proportions(3842, diabetes_proportions).item(1) - 0.0093)


# **Question 3**: The array `diabetes_proportions` contains the proportions of the population without and with diabetes. Complete the following code to simulate 5000 values of the statistic under the null hypothesis.
# 
# <!--
# BEGIN QUESTION
# name: q2_1_3
# manual: false
# -->

# In[40]:


diabetes_simulated_stats = make_array()

for i in np.arange(5000): 
    simulated_stat = diabetes_statistic()
    diabetes_simulated_stats = np.append(diabetes_simulated_stats, simulated_stat)
    
diabetes_simulated_stats


# In[41]:


ok.grade("q2_1_3");


# **Question 4**: Run the following cell to generate a histogram of the simulated values of your statistic, along with the observed value.
# 
# *Make sure to run the cell that draws the histogram, since it will be graded.*
# 
# <!--
# BEGIN QUESTION
# name: q2_1_4
# manual: true
# -->
# <!-- EXPORT TO PDF -->

# In[42]:


Table().with_column('Simulated distance to true incidence', diabetes_simulated_stats).hist()
plots.scatter(observed_diabetes_distance, 0, color='red', s=30);


# **Question 5**: Based on the results of the test and the empirical distribution of the test statistic under the null, should you reject the null hypothesis?
# 
# <!--
# BEGIN QUESTION
# name: q2_1_5
# manual: true
# -->
# <!-- EXPORT TO PDF -->

# Yes, I should reject the null hypothesis because the p-value seems like it is 0, which emplies that the observed test statistic is significantly greater than the simulated statistics. 

# **Question 6**: Why might there be a difference between the population and the sample from the Framingham Study? Assign the name `framingham_diabetes_explanations` to a list of the following explanations that **are possible and consistent** with the observed data and hypothesis test results.
# 
# 1. Diabetes was under-diagnosed in the population (i.e., there were a lot of people in the population who had diabetes but weren't diagnosed). By contrast, the Framingham participants were less likely to go undiagnosed because they had regular medical examinations as part of the study.
# 2. The relatively wealthy population in Framingham ate a luxurious diet high in sugar (high-sugar diets are a known cause of diabetes).
# 3. The Framingham Study subjects were older on average than the general population, and therefore more likely to have diabetes.
# 
# <!--
# BEGIN QUESTION
# name: q2_1_6
# manual: false
# -->

# In[48]:


framingham_diabetes_possibilities = [1, 2, 3] 
framingham_diabetes_possibilities


# In[49]:


ok.grade("q2_1_6");


# In real-world studies, getting a truly representative random sample of the population is often incredibly difficult. Even just to accurately represent all Americans, a truly random sample would need to examine people across geographical, socioeconomic, community, and class lines (just to name a few). For a study like this, scientists would also need to make sure the medical exams were standardized and consistent across the different people being examined. In other words, there's a tradeoff between taking a more representative random sample and the cost of collecting all the data from the sample.
# 
# The Framingham study collected high-quality medical data from its subjects, even if the subjects may not be a perfect representation of the population of all Americans. This is a common issue that data scientists face: while the available data aren't perfect, they're the best we have. The Framingham study is generally considered the best in its class, so we'll continue working with it while keeping its limitations in mind.
# 
# (For more on representation in medical study samples, you can read these recent articles from [NPR](https://www.npr.org/sections/health-shots/2015/12/16/459666750/clinical-trials-still-dont-reflect-the-diversity-of-america) and [Scientific American](https://www.scientificamerican.com/article/clinical-trials-have-far-too-little-racial-and-ethnic-diversity/)).

# ### Section 2: Cholesterol and Heart Disease

# In the remainder of this question, we are going to examine one of the main findings of the Framingham study: an association between serum cholesterol (i.e., how much cholesterol is in someone's blood) and whether or not that person develops heart disease.
# 
# We'll use the following null and alternative hypotheses:
# 
# **Null Hypothesis:** In the population, the distribution of cholesterol levels among those who get heart disease is the same as the distribution of cholesterol levels
# among those who do not.
# 
# **Alternative Hypothesis:** The cholesterol levels of people in the population who get
# heart disease are higher, on average, than the cholesterol level of people who do not.

# **Question 1:** From the provided Null and Alternative Hypotheses, does it seem reasonable to use A/B Testing to determine which model is more consistent? Assign the variable `ab_reasonable` to `True` if it seems reasonable and `False` otherwise.
# 
# <!--
# BEGIN QUESTION
# name: q2_2_1
# manual: false
# -->

# In[50]:


ab_reasonable = True
ab_reasonable


# In[51]:


ok.grade("q2_2_1");


# **Question 2:** Now that we have a null hypothesis, we need a test statistic. Explain and justify your choice of test statistic in two sentences or less.
# 
# *Hint*: Remember that larger values of the test statistic should favor the alternative over the null.
# 
# <!--
# BEGIN QUESTION
# name: q2_2_2
# manual: true
# -->
# <!-- EXPORT TO PDF -->

# The test statistic should be the difference between the mean of cholesterol levels of the group of individuals in the sample who get heart disease and the mean of cholesterol levels of the group of individuals who do not get heart disease. The alternative hypothesis compares the distribution of cholesterol levels of the former group to the distribution of cholesterol levels of the latter, so it makes sense to use the averages of the two groups' cholesterol levels to compare the two.

# **Question 3**: Write a function that computes your test statistic. It should take a table with two columns, `TOTCHOL` and `ANYCHD`, and compute the test statistic you described above. 
# 
# <!--
# BEGIN QUESTION
# name: q2_2_3
# manual: false
# -->

# In[52]:


def compute_framingham_test_statistic(tbl):
    avg_without_HD = np.mean(tbl.where("ANYCHD", are.equal_to(0)).column("TOTCHOL"))
    avg_with_HD = np.mean(tbl.where("ANYCHD", are.equal_to(1)).column("TOTCHOL"))
    return avg_with_HD - avg_without_HD


# In[53]:


ok.grade("q2_2_3");


# **Question 4**: Use the function you defined above to compute the observed test statistic, and assign it to the name `framingham_observed_statistic`.
# 
# <!--
# BEGIN QUESTION
# name: q2_2_4
# manual: false
# -->

# In[54]:


framingham_observed_statistic = compute_framingham_test_statistic(framingham)
framingham_observed_statistic


# In[55]:


ok.grade("q2_2_4");


# Now that we have defined hypotheses and a test statistic, we are ready to conduct a hypothesis test. We'll start by defining a function to simulate the test statistic under the null hypothesis, and then use that function 1000 times to understand the distribution under the null hypothesis.
# 
# **Question 5**: Write a function to simulate the test statistic under the null hypothesis. 
# 
# The `simulate_framingham_null` function should simulate the null hypothesis once (not 1000 times) and return the value of the test statistic for that simulated sample.
# 
# <!--
# BEGIN QUESTION
# name: q2_2_5
# manual: false
# -->

# In[57]:


def simulate_framingham_null():
    sample = framingham.sample(with_replacement = False).column("ANYCHD")
    relabeled = framingham.with_column("SHUFFLED", sample).drop("ANYCHD")
    relabeled = relabeled.relabel("SHUFFLED", "ANYCHD")
    return compute_framingham_test_statistic(relabeled)
    


# In[58]:


ok.grade("q2_2_5");


# In[62]:


# Run your function once to make sure that it works.
simulate_framingham_null()


# **Question 6**: Fill in the blanks below to complete the simulation for the hypothesis test. Your simulation should compute 1000 values of the test statistic under the null hypothesis and store the result in the array framingham_simulated_stats.
# 
# *Hint*: You should use the function you wrote above in Question 3.
# 
# *Note*: Warning: running your code might take a few minutes!  We encourage you to check your `simulate_framingham_null()` code to make sure it works correctly before running this cell. 
# 
# <!--
# BEGIN QUESTION
# name: q2_2_6
# manual: false
# -->

# In[60]:


framingham_simulated_stats = make_array()

for i in np.arange(1000):
    statistic = simulate_framingham_null()
    framingham_simulated_stats = np.append(framingham_simulated_stats, statistic)

framingham_simulated_stats


# **Question 7:** The following line will plot the histogram of the simulated test statistics, as well as a point for the observed test statistic. Make sure to run it, as it will be graded. 
# 
# <!--
# BEGIN QUESTION
# name: q2_2_7
# manual: true
# -->
# <!-- EXPORT TO PDF -->

# In[141]:


Table().with_column('Simulated statistics', framingham_simulated_stats).hist()
plots.scatter(framingham_observed_statistic, 0, color='red', s=30)


# **Question 8**: Compute the p-value for this hypothesis test, and assign it to the name `framingham_p_value`.
# 
# *Hint*: One of the key findings of the Framingham study was a strong association between cholesterol levels and heart disease. If your p-value doesn't match up with this finding, you may want to take another look at your test statistic and/or your simulation.
# 
# <!--
# BEGIN QUESTION
# name: q2_2_8
# manual: false
# -->

# In[142]:


framingham_p_value = np.count_nonzero(framingham_simulated_stats >= framingham_observed_statistic) / len(framingham_simulated_stats)
framingham_p_value


# In[143]:


ok.grade("q2_2_8");


# **Question 9**: Despite the Framingham Heart Study's well-deserved reputation as a well-conducted and rigorous study, it has some major limitations. Give one specific reason why it can't be used to say that high cholesterol *causes* heart disease.
# 
# <!--
# BEGIN QUESTION
# name: q2_2_9
# manual: true
# -->
# <!-- EXPORT TO PDF -->

# One reason why this cannot be used to say that high cholesterol causes heart disease is because this data was obtained through a an observational study. This matters because, unlike a randomized controlled exeperiment, observational studies cannot effectively control for confounding variables. Thus, we can only conclude that an association is present rather than establishing causality between high cholesterol and heart disease.

# Similar studies from the 1950s found positive associations between diets high in saturated fat, high cholesterol, and incidence of heart disease. In 1962, the U.S. Surgeon General said:
# 
# *"Although there is evidence that diet and dietary habits may be implicated in the development of coronary heart disease and may be significant in its prevention or control, at present our only research evidence is associative and not conclusive."*

# #### Congratulations, you have reached the checkpoint! Run the submit cell below to generate the checkpoint submission.

# In[63]:


_ = ok.submit()


# ## Part 3: The Nurses' Health Study and Hormone Replacement Therapy

# The Nurses' Health Study (NHS) is another very large observational study which has brought many insights into women's health. It was begun in 1976 by Dr. Frank Speizer, with questionnaires that were mailed to 121,964 female registered nurses in the United States asking about their medical history, cholesterol and blood pressure, current medications, and so on (one of the benefits of studying nurses is their ability to give reliably accurate answers to these questions). The study's initial focus was on investigating the long-term health effects of oral contraceptives, whose use had become much more widespread in the U.S. during the 1960s, but the focus soon expanded to investigating a wide variety of questions on women's health. The NHS continues to this day, tracking its third generation of nurses in the US.
# 
# One of the most consequential early findings from the NHS was about hormone replacement therapy (HRT): supplementary estrogen and progesterone for post-menopausal women to relieve side effects of declining hormone levels due to menopause. The NHS found that HRT in postmenopausal women was negatively associated with heart attack risk. In a landmark 1985 paper in the *New England Journal of Medicine* (NEJM), Speizer and his coauthors wrote that
# > As compared with the risk in women who had never used postmenopausal hormones, the age-adjusted relative risk of coronary disease in those who had ever used them was 0.5 (95 per cent confidence limits, 0.3 and 0.8; P = 0.007)... These data support the hypothesis that the postmenopausal use of estrogen reduces the risk of severe coronary heart disease. [(Stampfer et al., 1985)](https://www.ncbi.nlm.nih.gov/pubmed/4047106)
# 
# In other words, the authors are saying that women on HRT are half as likely to suffer a heart attack over a certain time period. We'll define the term "relative risk" later in this section, and we'll also investigate the interpretation of these claims and their statistical basis.

# **Question 1.** The block quote above is a direct quote from the 1985 article's abstract. Do you find any of the claims to be suspect? If so, why?
# 
# <!--
# BEGIN QUESTION
# name: q3_1
# manual: true
# -->
# <!-- EXPORT TO PDF -->

# I find the claim that "the postmenopausal use of estrogen reduces the risk of severe coronary heart disease" because this statement implies causation rather than association. I think that it is hard to determine causality from an observational study unlike an RCT because of the inability to control for confounding variables. Furthermore, I think that because the study allows people to enter and leave the experiment at different times due to the study's qualifications for valid candidates, it is even harder to determine causality. 

# The scientists running the NHS wanted to compare post-menopausal women who had ever taken HRT with post-menopausal women who had never taken HRT, excluding all women who were not post-menopausal or who had already suffered a heart attack. This study design complicates the analysis because it creates a variety of reasons why women might drop in and out of the relevant comparison groups.

# **Question 2.** Consider the following events which could occur in the middle of the study period (read the above paragraph carefully first): 
# 0. A woman who was pre-menopausal at the beginning of the study period becomes post-menopausal in the middle of the study period.
# 1. A post-menopausal woman survives a heart attack in the middle of the study period (assume the woman is post-menopausal and had never before had a heart attack).
# 2. A woman dies of cancer in the middle of the study period (assume the woman is post-menopausal and has never had a heart attack).
# 3. A woman who was not on HRT at the beginning of the study period, and had never before taken HRT, begins taking HRT in the middle of the period (assume the woman is post-menopausal and has never had a heart attack).
# 4. A woman who was taking HRT at the beginning of the study period stops taking HRT in the middle of the period (assume the woman is post-menopausal and has never had a heart attack).
# 
# For each of the events listed above, answer whether they would result in a woman
# 
# - (`E`) entering the study in the middle, 
# - (`L`) leaving the study in the middle, 
# - (`S`) switching from one comparison group to another in the middle, or 
# - (`N`) none of the above 
# 
# <!--
# BEGIN QUESTION
# name: q3_2
# -->
# 
# Assign `event_result` to a list of strings where the *i*th string is a single *capital* letter corresponding to your answer for the *i*th event.
# 
# For example, an example answer is `event_result = ['N', 'E', 'E', 'L', 'E']` where our answer for event 0 is `N`, our answer for event 1 is `E`, our answer for event 2 is ``, etc.

# In[68]:


event_result = ['E', 'L', 'L', 'S', 'N']


# In[69]:


ok.grade("q3_2");


# Because women could (and did) drop into and out of the comparison groups in the middle of the study, it is difficult to make a table like we usually would, with one row per participant. A more convenient sampling unit is a **person-month at risk**, which is one month spent by a particular woman in one of the comparison groups, during which she might or might not suffer a heart attack. Here, "at risk" just means the woman is being tracked by the survey in either of the two comparison groups, so that if she had a heart attack it would be counted in our data set.
# 
# **Example**: The table below tracks the histories of two hypothetical post-menopausal women in a six-month longitudinal study, who both enter the study in January 1978:
# 1. Alice has never been on HRT. She has a heart attack in March and is excluded for the remainder of the study period. 
# 2. Beatrice begins taking HRT for the first time in April and stays healthy throughout the study period.
# 
# | Name     | Month    | HRT | Heart Attack   |                                             
# |----------|----------|-----|----------------|
# | Alice    | Jan 1978 |  0  | 0              |
# | Alice    | Feb 1978 |  0  | 0              |
# | Alice    | Mar 1978 |  0  | 1              |
# | Beatrice | Jan 1978 |  0  | 0              | 
# | Beatrice | Feb 1978 |  0  | 0              |
# | Beatrice | Mar 1978 |  0  | 0              |
# | Beatrice | Apr 1978 |  1  | 0              |
# | Beatrice | May 1978 |  1  | 0              |
# | Beatrice | Jun 1978 |  1  | 0              |
# 
# 

# The probability that a heart attack will happen to a given at-risk person in a given duration of time is called the **hazard rate**. The NHS calculated its effects in terms of the **relative risk**, which is simply the hazard rate for person-months in the HRT (Group A) group divided by the hazard rate in the no-HRT (Group B) group.

# **Question 3.** Suppose the hazard rate for the no-HRT group is 0.1% per month and the relative risk is 50%. Assign `hrt_no_ha` to the probability that a given woman who is taking HRT will have no heart attacks for the entire four years of the study period.
# 
# Assign `no_hrt_no_ha` to the probability that a woman who is not taking HRT will have no heart attacks for the entire four years of the study period.
# 
# <!--
# BEGIN QUESTION
# name: q3_3
# -->

# In[70]:


hrt_no_ha = pow(0.9995, 48)
no_hrt_no_ha = pow(0.999, 48)


# In[71]:


ok.grade("q3_3");


# Most statistical methods that deal with this type of data assume that we can treat a table like the one above as though it is a sample of independent random draws from a much larger population of person-months at risk in each group. We will take this assumption for granted throughout the rest of this project.

# **Question 4.** The abstract quoted above gives a 95% confidence interval of [0.3, 0.8] for the relative risk. Which of the following statements can be justified based on that confidence interval?
# 1. There is a 95% chance the relative risk is between 0.3 and 0.8.
# 2. If we used a P-value cutoff of 5%, we would reject the hypothesis that the relative risk is equal to 1.
# 3. If we redo the procedure that generated the interval [0.3, 0.8] on a fresh sample of the same size, there is a 95% chance it will include the true relative risk.
# 4. There is between a 30% and 80% chance that any woman will suffer a heart attack during the study period.
# 
# Assign `ci_statements` to a list of number(s) corresponding to the correct answer(s).
# 
# <!--
# BEGIN QUESTION
# name: q3_4
# -->

# In[72]:


ci_statements = [2, 3]


# In[73]:


ok.grade("q3_4");


# Instead of *person-months* at risk, the NHS used *person-years* at risk. It reported 51,478 total person-years at risk in the no-HRT group with 60 heart attacks occurring in total, as well as 54,309 person-years at risk in the HRT group with 30 heart attacks occurring in total. The table NHS below has one row for each person-year at risk. The two columns are 'HRT', recording whether it came from the HRT group (1) or no-HRT group (0), and 'Heart Attack', recording whether the participant had a heart attack that year (1 for yes, 0 for no).

# In[74]:


NHS = Table.read_table('NHS.csv')
NHS.show(3)


# **Question 5.** Fill in the missing code below to write a function called `relative_risk` that takes in a table with the column labels `HRT` and `Heart Attack`, and computes the sample relative risk as an estimate of the population relative risk. Do *not* round your answer.
# 
# <!--
# BEGIN QUESTION
# name: q3_5
# -->

# In[75]:


def relative_risk(tbl):
    """Return the ratio of the hazard rates (events per person-year) for the two groups"""
    tbl = tbl.group("HRT", np.average)
    rates = tbl.column("Heart Attack average")
    return rates.item(1) / rates.item(0)
    
relative_risk(NHS)


# In[76]:


ok.grade("q3_5");


# **Question 6.** Fill in the function `one_bootstrap_rr` so that it generates one bootstrap sample and computes the relative risk. Assign `bootstrap_rrs` to 10 (yes, only 10; the code is slow!) estimates of the population relative risk.
# 
# *Note:* The cell may take a few seconds to run.
# 
# <!--
# BEGIN QUESTION
# name: q3_6
# -->

# In[77]:


def one_bootstrap_rr():
    return relative_risk(NHS.sample())

bootstrap_rrs = make_array()
for i in np.arange(10):
    new_bootstrap_rr = one_bootstrap_rr()
    bootstrap_rrs = np.append(bootstrap_rrs, new_bootstrap_rr)


# In[78]:


ok.grade("q3_6");


# **Question 7.** The file `bootstrap_rrs.csv` contains a table with 2001 saved bootstrapped relative risks. Use these bootstrapped values to compute a 95% confidence interval, storing the left endpoint as `ci_left` and the right endpoint as `ci_right`. 
# 
# Note that our method isn't exactly the same as the method employed by the study authors to get their confidence interval.
# 
# <!--
# BEGIN QUESTION
# name: q3_7
# -->

# In[79]:


bootstrap_rrs_tbl = Table.read_table('bootstrap_rrs.csv')
bootstrap_rrs = bootstrap_rrs_tbl.column(0)
ci_left = percentile(2.5, bootstrap_rrs)
ci_right = percentile(97.5, bootstrap_rrs)

print("Middle 95% of bootstrappped relative risks: [{:f}, {:f}]".format(ci_left, ci_right))


# In[80]:


ok.grade("q3_7");


# The code below plots the confidence interval on top of the bootstrap histogram.

# In[81]:


# Just run this cell
bootstrap_rrs_tbl.hist()
plots.plot([ci_left, ci_right], [.05,.05], color="gold");


# ## Part 4: The Heart and Estrogen-Progestin Replacement Study

# Partly as a result of evidence from the NHS and other observational studies that drew similar conclusions, HRT drugs became a very popular preventive treatment for doctors to prescribe to post-menopausal woman. Even though there were known or suspected risks to the treatment (such as increasing the risk of invasive breast cancer), it was thought that the reduction in heart disease risk was well worth it.

# The Heart and Estrogen-Progestin Replacement Study (HERS) was a large randomized controlled trial carried out by the Women's Health Initiative, which sought to verify whether HRT drugs were as effective as the observational studies seemed to suggest. 2,763 women with a history of heart disease were selected and randomly assigned to receive the treatment (daily estrogen pills) or a placebo pill that looked identical to the treatment. Of the 2763 women participating, 1380 were assigned to the treatment condition and 1383 to the control. They were followed for an average of three years and the number of heart attacks in the two groups was compared.

# The main results table from the HERS study [Hulley et al. (1998)](https://jamanetwork.com/journals/jama/fullarticle/187879) is reproduced here:
# 
# <img src="HERS-table.png" width=500>

# **Question 1**: For this study, we will construct our own table from scratch based on the results given above. Create a table called `HERS` that has one row for each woman in the trial and two columns: `HRT`, which is 1 if she was assigned to treatment and 0 otherwise, and `CHD`, which is 1 if she suffered a Primary CHD (Coronary Heart Disease) event and 0 otherwise.
# 
# *Hint*: Remember what the functions `np.ones` and `np.zeros` do. They may be helpful here!
# 
# <!--
# BEGIN QUESTION
# name: q4_1
# -->

# In[120]:


num_control = 1383
num_treatment = 1380

num_control_chd = 176
num_treatment_chd = 172


hrt = np.append(np.zeros(num_control), np.ones(num_treatment))
chd_control = np.append(np.zeros(num_control - num_control_chd), np.ones(num_control_chd))
chd_treatment = np.append(np.zeros(num_treatment - num_treatment_chd), np.ones(num_treatment_chd))
chd = np.append(chd_control, chd_treatment)
HERS = Table().with_column('HRT', hrt, 'CHD', chd)
HERS.show(3)


# In[104]:


ok.grade("q4_1");


# **Question 2.** Make a pivot table called `HERS_pivot` where each unique `CHD` value has its own row and each unique `HRT` value has its own column. Check that you have the right number of each combination of the two columns. 
# 
# <!--
# BEGIN QUESTION
# name: q4_2
# -->

# In[105]:


HERS_pivot = HERS.pivot("HRT", "CHD")
HERS_pivot


# In[106]:


ok.grade("q4_2");


# **Question 3.** We would like to test the null hypothesis that the treatment (HRT) has no effect on the outcome (CHD), against the alternative hypothesis that the treatment does have an effect. What would be a good test statistic? 
# 
# Assign `good_ts` to a list of number(s) corresponding to the correct answer(s). Keep in mind that this was the first clinical trial to be done on this subject; as a result, it was not clear at the time whether any effect would be positive or negative.
# 
# 
# 1. The absolute difference between 1 and the relative risk.
# 2. The average CHD rate for the treatment group.
# 3. 10 times the absolute difference between the control and treatment groups' average CHD rates.
# 
# <!--
# BEGIN QUESTION
# name: q4_3
# -->

# In[107]:


good_ts = [1, 3]


# In[108]:


ok.grade("q4_3");


# **Question 4.** We'll use distance between average CHD rates as our test statistic. 
# 
# Write a function called `hers_test_statistic` to calculate this test statistic on a table with columns `HRT` and `CHD`. Use this function to calculate the observed test statistic, and assign it to `observed_HERS_test_statistic`.
# 
# Think about what values of the test statistic support the null versus the alternative hypothesis. You'll use this information to compute the p-value later in this section.
# <!--
# BEGIN QUESTION
# name: q4_4
# -->

# In[109]:


def HERS_test_statistic(tbl):
    """Test statistic: Distance between the average responses"""
    averages = tbl.group("HRT", np.average).column("CHD average")
    return abs(averages.item(0) - averages.item(1))


observed_HERS_test_statistic = HERS_test_statistic(HERS)
observed_HERS_test_statistic


# In[110]:


ok.grade("q4_4");


# **Question 5.** Write a function called `simulate_one_HERS_statistic` to simulate one value of the test statistic under the null hypothesis.
# 
# <!--
# BEGIN QUESTION
# name: q4_5
# -->

# In[111]:


def simulate_one_HERS_statistic():
    shuffled = HERS.sample(with_replacement = False).column("HRT")
    tbl = Table().with_column("HRT", shuffled, "CHD", HERS.column("CHD"))
    return HERS_test_statistic(tbl)
simulate_one_HERS_statistic()


# In[112]:


ok.grade("q4_5");


# **Question 6.** Write a `for` loop to repeatedly sample the null hypothesis 1000 times and compute the test statistic each time. The cell may take a few seconds to run.
# 
# 
# <!--
# BEGIN QUESTION
# name: q4_6
# -->

# In[113]:


HERS_test_statistics = make_array()
for i in np.arange(1000):
    new_HERS_statistic = simulate_one_HERS_statistic()
    HERS_test_statistics = np.append(HERS_test_statistics, new_HERS_statistic)


# In[114]:


ok.grade("q4_6");


# The code below generates a histogram of the simulated test statistics along with your test statistic:

# In[115]:


Table().with_column('Simulated test statistics', HERS_test_statistics).hist(bins=np.arange(0,.04,.003))
plots.scatter(HERS_test_statistic(HERS), 0, color='red', s=30);


# **Question 7.** Compute the P-value for your hypothesis test and assign it to `HERS_pval`. 
# 
# <!--
# BEGIN QUESTION
# name: q4_7
# -->

# In[116]:


HERS_pval = np.count_nonzero(HERS_test_statistics >= observed_HERS_test_statistic) / len(HERS_test_statistics)
HERS_pval


# In[117]:


ok.grade("q4_7");


# **Question 8.** Are the data consistent with the null hypothesis being true?
# 
# <!--
# BEGIN QUESTION
# name: q4_7
# manual: true
# -->
# <!-- EXPORT TO PDF -->

# Yes, the data are consistent with the null hypothesis being true because the p-value is 

# In part 3, we gave you 2001 bootstrapped relative risks. In the context of the HERS trial, relative risk is now defined as the ratio of the probability that a given woman in the treatment group will have CHD over the study period divided by the probability that a given woman in the control group will have CHD over the study period.
# 
# We plot the histogram of bootstrapped relative risks, along with a confidence interval representing the middle 95% of that histogram:
# <img src="bootstrap-HERS.png" width=400>
# 
# A relative risk of 1 means that the probability of CHD is the same for both the treatment and control groups, which would correspond to the treatment having no effect. Note that 1 is right in the middle of the interval.

# **Question 9.** Based on the results for this experiment, can we conclude that HRT is not actually protective against heart disease risk? Explain why or why not.
# 
# <!--
# BEGIN QUESTION
# name: q4_9
# manual: true
# -->
# <!-- EXPORT TO PDF -->

# No, we can't conclude that HRT is actually not protective against heart disease risk because the confidence interval has values greater than and less than 1.

# **Question 10:** The HERS study authors put forward a possible answer regarding why the NHS study might be biased:
# > However, the observed association between estrogen therapy and reduced CHD risk might be attributable to selection bias if women who choose to take hormones are healthier and have a more favorable CHD profile than those who do not. Observational studies cannot resolve this uncertainty.
# 
# If women who choose to take hormones are healthier to begin with than women who choose not to, why might that systematically bias the results of observational studies like the NHS? Would we expect observational studies to overestimate or underestimate the protective effect of HRT?
# 
# <!--
# BEGIN QUESTION
# name: q4_10
# manual: true
# -->
# <!-- EXPORT TO PDF -->

# If women who choose to take hormones are healther to begin with than women who choose not to, we would see a systemic bias in observational studies like the NHS because women who are healthier in the HRT group will experience fewer heart attacks. As a result, observational studies would overestimate the protective effect of HRT.

# Congratulations! You have completed your own large scale case study into cause and effect surrounding one of the world's deadliest killers: cardiovascular disease. Your investigation you has taken you through two important data sets and across decades of medical research.
# 
# Run the next two cells to run all the tests at once and submit the project. 

# In[118]:


_ = ok.submit()


# ### Further reading
# 
# If you're interested in learning more, you can check out these articles:
# 
# * [Origin story of the Framingham Heart Study](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1449227/)
# * [NYT article on the Nurses' Health Study and the HERS study](https://www.nytimes.com/2003/04/22/science/hormone-studies-what-went-wrong.html)

# In[119]:


# For your convenience, you can run this cell to run all the tests at once!
import os
print("Running all tests...")
_ = [ok.grade(q[:-3]) for q in os.listdir("tests") if q.startswith('q') and len(q) <= 10]
print("Finished running all tests.")


# In[ ]:




