import pandas as pd

df = pd.read_csv('dict.csv')

ignore_categories = ['special_characters', 'proper_noun', 'place_name', 'people_names', 'general_product', 'brand_name', '인명']

filtered_df = df[~df['category'].isin(ignore_categories)]
filtered_df = filtered_df[~filtered_df['category'].isnull()]

filtered_df = filtered_df[['term', 'category']]
sorted_df = filtered_df.sort_values(by=['term', 'category'])

sorted_df.to_csv('output.csv', index=False)

