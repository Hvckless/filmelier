import pandas as pd
from sklearn.cluster import KMeans

df = pd.read_csv('광해.csv')

df_unique = df.drop_duplicates(subset=['Word'])
x = df_unique.drop(columns=['Word', 'sentence_index']).values

num_clusters = 10
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(x)

df_unique['Cluster'] = kmeans.labels_

output_file = 'word_clusters.csv'
df_unique[['Word', 'Cluster']].to_csv(output_file, index=False)

print(f"클러스터링 결과'{output_file}에 저장'")
