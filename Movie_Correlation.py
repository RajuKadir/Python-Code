import pandas as pd,  numpy as np,  seaborn as sns

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib
plt.style.use('ggplot')
from matplotlib.pyplot import figure

plt.show()
matplotlib.rcParams['figure.figsize'] = (12,8)

pd.options.mode.chained_assignment = None

# Load data into dataframe

df = pd.read_csv(r'C:\Users\Raju\Documents\Portfolio\Movie Data\movies.csv')
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)

# Check for missing data.

for col in df.columns:
    pct_missing = np.mean(df[col].isnull())
    print('{} - {}%'.format(col, round(pct_missing*100)))

# Drop missing data from budget and gross columns

df= df.dropna(subset=['budget'])
df= df.dropna(subset=['gross'])

# Looking at the data types in columns

print(df.dtypes)

# Change the data type of budget and gross into integers

df['budget'] = df['budget'].astype('int64')
df['gross'] = df['gross'].astype('int64')
print(df.dtypes)

# Create correct year column

df['yearcorrect'] = df['released'].str.split(',').str[1].str.extract('(\d+)').astype('Int64')
print(df)

df = df.sort_values(by=['gross'], inplace=False, ascending=False)
print(df)

# Drop any duplicates

df.drop_duplicates()

# Scatter plot with budget vs gross

plt.scatter(x=df['budget'], y=df['gross'])
plt.title('Budget vs Gross Earnings')
plt.xlabel('Gross Earnings (Millions)')
plt.ylabel('Budget (Billions)')
plt.show()

# Plot budget vs gross using seaborn

scatter = sns.regplot(x='budget', y='gross' , data=df, scatter_kws={"color": "red"}, line_kws={"color": "blue"})
scatter.set_title('Budget vs Gross Earnings')
scatter.set_xlabel('Gross Earnings (Millions)')
scatter.set_ylabel('Budget (Billions)')

# Looking at the correlation

df.corr(method='pearson') # pearson, kendall, spearman

# There is a high correlation between budget and gross

# Display correlation matrix for numeric fields

correlation_matrix = df.corr(method='pearson')
sns.heatmap(correlation_matrix, annot=True)
plt.title('Correlation Matrix for Numeric Fields')
plt.xlabel('Movie Features')
plt.ylabel('Movie Features')
plt.show()

# Changing all fields to numeric and looking at the correlation

df_numerized = df
for col_name in df_numerized.columns:
    if(df_numerized[col_name].dtype == 'object'):
        df_numerized[col_name] = df_numerized[col_name].astype('category')
        df_numerized[col_name] = df_numerized[col_name].cat.codes

correlation_matrix = df_numerized.corr(method='pearson')
sns.heatmap(correlation_matrix, annot=True)
plt.title('Correlation Matrix for Numeric Fields')
plt.xlabel('Movie Features')
plt.ylabel('Movie Features')
plt.show()

correlation_mat = df_numerized.corr()
corr_pairs = correlation_mat.unstack()
sorted_pairs = corr_pairs.sort_values()
print(sorted_pairs)

high_corr = sorted_pairs[(sorted_pairs) > 0.5]
print(high_corr)

#Plot a ratings by gross graph

sns.stripplot(x="rating", y="gross", data=df)