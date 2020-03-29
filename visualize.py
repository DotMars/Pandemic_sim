import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
import numpy as np
import csv

with open('data.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)


infected_data = []
susceptible_data = []
remove_data = []
time_data = []
i = 0
for entry in data:
    infected_data.append(entry[0])
    susceptible_data.append(entry[1])
    remove_data.append(entry[2])
    time_data.append(i)
    i += 1
    

# plot the data
fig = plt.figure()
ax1 = fig.add_subplot(111)
# ax2 = fig.add_subplot(132)
# ax3 = fig.add_subplot(133)

ax1.set_title('Infected')
# ax2.set_title('Susceptible')
# ax3.set_title('Removed')

ax1.plot(time_data, infected_data, color='tab:red')
ax1.plot(time_data, susceptible_data, color='tab:blue')
ax1.plot(time_data, remove_data, color='tab:grey')



# display the plot
plt.show()