import numpy as np
import sys
import matplotlib.pyplot as plt
import pandas as pd
import csv

with open('data.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

# data = pd.read_csv("data.csv")

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

x = time_data
y1 = infected_data
y2 = susceptible_data
y3 = remove_data

np.set_printoptions(threshold = sys.maxsize)
y = np.vstack([y1, y2, y3])

# x = np.linspace(0, 10, 500)
# y1 = np.sin(x)
labels = ["Time", "Infected ", "Susceptible", "Remove"]

fig, ax = plt.subplots()
# ax.stackplot(x, y, labels=labels)
# ax.legend(loc='upper left')
# plt.show()

# Plotting
# line1, = ax.plot(x , dashes=[6, 2], label = labels[0])
# line2, = ax.plot(y1 , dashes=[6, 2], label = labels[1])
line3, = ax.plot(y2 , dashes=[6, 2], label = labels[2])
# line4, = ax.plot(y3 , dashes=[6, 2], label = labels[3])

ax.legend()
plt.show()