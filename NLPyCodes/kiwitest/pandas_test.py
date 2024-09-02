import pandas as pd
import numpy as np

dates = pd.date_range('20130101', periods=6)
df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))

print(dates)
print("-------------------")
print(df)

print("~~~~~~~~~~~~~~~~~~~")
print(np.random.randn(6,4))

df.to_csv('./hello.csv')