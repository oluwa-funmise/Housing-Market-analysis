import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(8,5))
sns.set_style("whitegrid")

df = pd.read_csv("Housing.csv")

df.info()

df.duplicated().sum()

df.describe()

#Cleaning the categorical columns
for col in df.select_dtypes(include="object").columns:
    print(col)
    print(df[col].unique())
    print()

for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].str.strip().str.lower()

yes_no_columns = ['mainroad', 'guestroom', 'basement', 'hotwaterheating',
                  'airconditioning', 'prefarea']

for col in yes_no_columns:
    df[col] = df[col].map({'yes': 1, 'no': 0})

#Encoding furnishing status 
df['furnishingstatus'] = df['furnishingstatus'].map({
    'unfurnished': 0,
    'semi-furnished': 1,
    'furnished': 2
})

df.info()

#Univaraiate Analysis 
plt.figure(figsize=(8,5))
plt.hist(df['price'], bins=30, edgecolor='black')
plt.title("Distribution of House Prices")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.show()


#Boxplot of house prices 
plt.figure(figsize=(8,5))
plt.boxplot(df['price'])
plt.title("Boxplot of House Prices")
plt.ylabel("Price")
plt.show()

#Checking outliers using IQR method 
Q1 = df['price'].quantile(0.25)
Q3 = df['price'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[(df['price'] < lower_bound) | (df['price'] > upper_bound)]
outliers.shape

#Removing them
df_no_outliers = df[(df['price'] >= lower_bound) & (df['price'] <= upper_bound)]


#univariate for other numerical columns 
for col in numerical_columns:
    plt.figure(figsize=(8,5))
    plt.hist(df[col], bins=20, edgecolor='black')
    plt.title(f"Distribution of {col}")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.show()


#BIVARIATE ANALYSIS 
#Price vs area
plt.figure(figsize=(8,5))
plt.scatter(df['area'], df['price'])
plt.title("Price vs Area")
plt.xlabel("Area")
plt.ylabel("Price")
plt.show()

#Price vs bedrooms
plt.figure(figsize=(8,5))
plt.boxplot([df[df['bedrooms'] == b]['price'] for b in sorted(df['bedrooms'].unique())],
            labels=sorted(df['bedrooms'].unique()))
plt.title("Price by Number of Bedrooms")
plt.xlabel("Bedrooms")
plt.ylabel("Price")
plt.show()

#Price vs bathrooms
plt.figure(figsize=(8,5))
plt.boxplot([df[df['bedrooms'] == b]['price'] for b in sorted(df['bedrooms'].unique())],
            labels=sorted(df['bedrooms'].unique()))
plt.title("Price by Number of Bedrooms")
plt.xlabel("Bedrooms")
plt.ylabel("Price")
plt.show()

#Price by furnishing status 
furnishing_labels = ['unfurnished', 'semi-furnished', 'furnished']

plt.figure(figsize=(8,5))
plt.boxplot([df[df['furnishingstatus'] == i]['price'] for i in range(3)],
            labels=furnishing_labels)
plt.title("Price by Furnishing Status")
plt.xlabel("Furnishing Status")
plt.ylabel("Price")
plt.show()


#Correlation Analysis 
df.corr(numeric_only=True)


#Correlation heatmap
plt.figure(figsize=(10,6))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Heatmap")
plt.show()


# GROUPED ANALYSIS FOR INVESTORS AND BUYERS 
# Average price by bedrooms
df.groupby('bedrooms')['price'].mean().sort_values()

# Average price by bathrooms
df.groupby('bathrooms')['price'].mean().sort_values()

# Average price furnishing status 
df.groupby('furnishingstatus')['price'].mean().sort_values()
