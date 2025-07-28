import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats

# read csv files
men_df = pd.read_csv('men_results.csv')
women_df = pd.read_csv('women_results.csv')

# convert to data
men_df['date'] = pd.to_datetime(men_df['date'])
women_df['date'] = pd.to_datetime(women_df['date'])

# filter matches before 2002
men_df = men_df[men_df['date'] >= '2002']
women_df = women_df[women_df['date'] >= '2002']

# only FIFA World Cup
men_df = men_df[men_df['tournament'] == 'FIFA World Cup']
women_df = women_df[women_df['tournament'] == 'FIFA World Cup']

# independent of place
men_df['total_score'] = men_df['home_score'] + men_df['away_score']
women_df['total_score'] = women_df['home_score'] + women_df['away_score']

# normality test
men_norm = stats.shapiro(men_df['total_score']).pvalue
women_norm = stats.shapiro(women_df['total_score']).pvalue
print(f'Men normality p-value: {men_norm}')
print(f'Women normality p-value: {women_norm}')

plt.hist(men_df['total_score'])
plt.hist(women_df['total_score'])
plt.legend(['men', 'women'])
plt.ylabel('goals count')
plt.show()

# variances difference test
v_stat, p_var = stats.levene(men_df['total_score'], women_df['total_score'], center='median')
print(f"Levene’s test for variance difference p-value: {p_var}")


# data is not normal, variances are significantly same, using non-parametrical mann-whitney test
alpha = 0.1

stat, p = stats.mannwhitneyu(women_df['total_score'], men_df['total_score'], alternative='greater')
print(f'Mann–Whitney U test p-value: {p}')

result_answer = 'reject' if p < alpha else 'fail to reject'
result_dict = {"p_val": p, "result": result_answer}
print(result_dict)
