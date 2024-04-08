import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
from scipy import stats
import seaborn as sns
# from sklearn import preprocessing
# from scipy.stats import pearsonr

matplotlib.use('TkAgg')

path = 'passes.csv'

columns = ['game_id','passing_quote','winner']

# Reading the specified columns
data = pd.read_csv(path, sep=';', usecols=columns)

# drop Na
data.dropna(subset=['game_id','passing_quote','winner'], inplace=True)


fig, axs = plt.subplots(1, 1, figsize=(8, 9))

# Extract passing rates data
total_passes = data['passing_quote']

# Create DataFrame for passing rates
total_passes = pd.DataFrame({'Passing_rates': total_passes})

# Plot the histogram
sns.histplot(data=total_passes, x='Passing_rates', kde=True, ax=axs, color='lightgreen')

# Set title
axs.set_title('Distribution of Passing Quotes')

# Set labels
axs.set_ylabel('Frequency')
axs.set_xlabel('Passing Rate')

# Show the plot
plt.show()


winner_data = {}
loser_data = {}
for index, row in data.iterrows():
    # Check if the value in the 'passing_quote' column matches the specific value
    game_id = row['game_id']

    # Update the 'winner' status to 'winner' for this row
    if row['winner'] == "Yes":
        winner_data[game_id] = []
        winner_data[game_id].append(row['passing_quote'])

    if row['winner'] == "No":
        if game_id not in loser_data:
            loser_data[game_id] = []
        loser_data[game_id].append(row['passing_quote'])

winners = [i for i in winner_data.values()]
losers = [i for i in loser_data.values() if len(i) < 2]

total_winners = [i[0] for i in winners]
total_losers = [i[0] for i in losers]

pass_draw = []
for i in loser_data.values():
    if len(i) == 2:
        pass_draw.append(i[0])
        pass_draw.append(i[1])

winner_frame = pd.DataFrame({'Winner': total_winners})
loser_frame = pd.DataFrame({'Loser': total_losers})
draw_frame = pd.DataFrame({'Draw': pass_draw})

winners = winner_frame['Winner']
losers = loser_frame['Loser']


mean_data = np.mean(winners)
median_data = np.median(winners)
mode_data = winners.mode()[0]
range_data = np.ptp(winners)
quartile1, quartile2, quartile3 = np.percentile(winners, [25, 50, 75])
variance_data = np.var(winners)
standart_deviation = np.std(winners)

print("Mean: {}".format(mean_data))
print("Median: {}".format(median_data))
print("Mode: {}".format(mode_data))
print("Range: {}".format(range_data))
print("Q1: {}".format(quartile1))
print("Q2: {}".format(quartile2))
print("Q3: {}".format(quartile3))
print("Variance: {}".format(variance_data))
print("Standard Deviation: {}".format(standart_deviation))


mean_data = np.mean(losers)
median_data = np.median(losers)
mode_data = losers.mode()[0]
range_data = np.ptp(losers)
quartile1, quartile2, quartile3 = np.percentile(losers, [25, 50, 75])
variance_data = np.var(losers)
standart_deviation = np.std(losers)

print("Mean: {}".format(mean_data))
print("Median: {}".format(median_data))
print("Mode: {}".format(mode_data))
print("Range: {}".format(range_data))
print("Q1: {}".format(quartile1))
print("Q2: {}".format(quartile2))
print("Q3: {}".format(quartile3))
print("Variance: {}".format(variance_data))
print("Standard Deviation: {}".format(standart_deviation))


# Creating subplots
fig, axs = plt.subplots(3, 1, figsize=(8, 9))

# Plot histograms
sns.histplot(data=winner_frame, x='Winner', kde=True, ax=axs[0],color='skyblue')
sns.histplot(data=loser_frame, x='Loser', kde=True, ax=axs[1],color='salmon')
sns.histplot(data=draw_frame, x='Draw', kde=True, ax=axs[2], color='lightgreen')

# Set titles
axs[0].set_title('Distribution of Passing Quote for Winners')
axs[1].set_title('Distribution of Passing Quote for Losers')
axs[2].set_title('Distribution of Passing Quote for Draws')

for ax in axs.flat:
    ax.set_ylabel('Frequency')
    ax.set_xlabel('Passing Rate')

# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()


# Combine the data into a list of arrays
data = [total_winners, total_losers]

# Create a boxplot
plt.boxplot(data)

# Set labels for x-axis
plt.xticks([1, 2], ['Winners', 'Losers'])

# Add a title
plt.title('Comparison of Passing Quote between Winners and Losers')

# Add labels for y-axis
plt.ylabel('Passing Quote')

# Show the plot
plt.show()



values = stats.ttest_ind(a=total_winners, b=total_losers)
t_statistic = values.statistic
p_value = values.pvalue
print(values)

plt.figure(figsize=(8, 6))

# Plot histograms of the two groups
plt.hist(total_winners, bins=20, alpha=0.5, label='Winners')
plt.hist(total_losers, bins=20, alpha=0.5, label='Losers')

# Mark the t-test statistic on the plot
plt.axvline(x=np.mean(total_winners), color='blue', linestyle='--', label='Mean of Winners')
plt.axvline(x=np.mean(total_losers), color='orange', linestyle='--', label='Mean of Losers')
plt.axvline(x=t_statistic, color='red', linestyle='--', label=f'T-Statistic: {t_statistic:.2f}')
plt.axvline(x=p_value, color='green', linestyle='--', label=f'P-Value: {p_value:.2f}')

plt.title(f'Distribution of Passing Quotes\np-value: {p_value:.4f}')  # Include p-value in the title

plt.title('Distribution of Passing Quotes')
plt.xlabel('Passing Quotes')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)
plt.show()

print("T-Statistic:", t_statistic)
print("P-Value:", p_value)


pass_difference_win_lose = np.abs(np.subtract(total_winners, total_losers))
for i in pass_difference_win_lose:
    print(i)

pass_difference_draw= [abs(i[0] - i[1]) for i in loser_data.values() if len(i) == 2]
print(pass_difference_draw)

values = stats.ttest_ind(a=pass_difference_win_lose, b=pass_difference_draw)
t_statistic = values.statistic
p_value = values.pvalue


print("pass difference - Win - Draw")

win_lose_frame = pd.DataFrame({'pass_diff1': pass_difference_win_lose})
pass_diff_frame = pd.DataFrame({'pass_diff2': pass_difference_draw})


pass_diffwin_lose = win_lose_frame['pass_diff1']
pass_dif = pass_diff_frame['pass_diff2']

mean_data = np.mean(pass_diffwin_lose)
median_data = np.median(pass_diffwin_lose)
mode_data = pass_diffwin_lose.mode()[0]
range_data = np.ptp(pass_diffwin_lose)
quartile1, quartile2, quartile3 = np.percentile(pass_diffwin_lose, [25, 50, 75])
variance_data = np.var(pass_diffwin_lose)
standart_deviation = np.std(pass_diffwin_lose)

print("Mean: {}".format(mean_data))
print("Median: {}".format(median_data))
print("Mode: {}".format(mode_data))
print("Range: {}".format(range_data))
print("Q1: {}".format(quartile1))
print("Q2: {}".format(quartile2))
print("Q3: {}".format(quartile3))
print("Variance: {}".format(variance_data))
print("Standard Deviation: {}".format(standart_deviation))


mean_data = np.mean(pass_dif)
median_data = np.median(pass_dif)
mode_data = pass_dif.mode()[0]
range_data = np.ptp(pass_dif)
quartile1, quartile2, quartile3 = np.percentile(pass_dif, [25, 50, 75])
variance_data = np.var(pass_dif)
standart_deviation = np.std(pass_dif)

print("Mean: {}".format(mean_data))
print("Median: {}".format(median_data))
print("Mode: {}".format(mode_data))
print("Range: {}".format(range_data))
print("Q1: {}".format(quartile1))
print("Q2: {}".format(quartile2))
print("Q3: {}".format(quartile3))
print("Variance: {}".format(variance_data))
print("Standard Deviation: {}".format(standart_deviation))

print(values)


# draw difference pass difference
data = [pass_difference_win_lose, pass_difference_draw]

# Create a boxplot
plt.boxplot(data)

# Set labels for x-axis
plt.xticks([1, 2], ['Win matches', 'Draw matches'])

# Add a title
plt.title('Comparison of Passing Difference in a match between Win and Draw')

# Add labels for y-axis
plt.ylabel('Passing Quote')

# Show the plot
plt.show()


plt.figure(figsize=(8, 6))

# Plot histograms of the two groups
plt.hist(pass_difference_win_lose, bins=20, alpha=0.5, label='Pass difference in Win matches')
plt.hist(pass_difference_draw, bins=20, alpha=0.5, label='Pass difference in Draw matches')

# Mark the t-test statistic on the plot
plt.axvline(x=np.mean(pass_difference_win_lose), color='blue', linestyle='--', label='Mean of pass difference in Win matches')
plt.axvline(x=np.mean(pass_difference_draw), color='orange', linestyle='--', label='Mean of pass difference in Draw matches')
plt.axvline(x=t_statistic, color='red', linestyle='--', label=f'T-Statistic: {t_statistic:.2f}')
plt.axvline(x=p_value, color='green', linestyle='--', label=f'P-Value: {p_value:.2f}')

plt.title('Distribution of Passing Quotes')
plt.xlabel('Passing Quotes')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)
plt.show()


