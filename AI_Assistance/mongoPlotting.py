import matplotlib.pyplot as plt
import pandas as pd
import pymongo



client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')

mydb=client['mydb']
tradeinfo = mydb.TradeDetails


lst_power_production = list(tradeinfo.find(filter={}, projection={"_id": 0, "ccy": 1, "ctr": 1}))

df_mongo = pd.DataFrame(lst_power_production)


# Create DataFrame
#df = pd.DataFrame(data)

# Count the occurrences of each trade status
status_counts = df_mongo['ctr'].value_counts()

print(status_counts)

# Create bar chart
plt.bar(status_counts.index, status_counts.values)

# Add labels and title
plt.xlabel('CTR')
plt.ylabel('Count')
plt.title('Distribution of CTR')

# Display the chart
plt.show()