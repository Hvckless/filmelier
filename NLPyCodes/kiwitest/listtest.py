import pandas as pd

somelist = []

indexTitles = ["legend", "minecraft"]

kinglist = [1,2,3]
poplist = [4,5,6]

columnList = ["king", "god", "emperor"]

somelist.append(kinglist)
somelist.append(poplist)

df = pd.DataFrame(somelist, index=indexTitles, columns=columnList)

print(df)

print(somelist)




print('-----------------------')
print(list('안녕','하세','요'))