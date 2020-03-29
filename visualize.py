import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# with open('data.csv', newline='') as f:
#     reader = csv.reader(f)
#     data = list(reader)

# infected_data = []
# susceptible_data = []
# remove_data = []
# time_data = []
# i = 0
# for entry in data:
#     infected_data.append(entry[0])
#     susceptible_data.append(entry[1])
#     remove_data.append(entry[2])
#     time_data.append(i)
#     i += 1

data = pd.read_csv("data.csv")

x = data[0]
y1 = data[1]
y2 = data[2]
y3 = data[3]

y = np.vstack([y1, y2, y3])

labels = ["Infected ", "Susceptible", "Remove"]

fig, ax = plt.subplots()
ax.stackplot(x, y1, y2, y3, labels=labels)
ax.legend(loc='upper left')
plt.show()



