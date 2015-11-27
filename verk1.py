import csv as csv
import numpy as np

csv_file_object = csv.reader(open('train.csv'))

header = next(csv_file_object)
data = []
for row in csv_file_object:
    data.append(row)

data = np.array(data)

number_passengers = np.size(data[0::,1].astype(np.float))
number_survived = np.sum(data[0::,1].astype(np.float))

proportion_survivors = number_survived / number_passengers

women_only_stats = data[0::,4] == "female"
men_only_stats = data[0::,4] != "female"

women_onboard = data[women_only_stats,1].astype(np.float)
men_onboard = data[men_only_stats,1].astype(np.float)

proportion_women_survived = np.sum(women_onboard) / np.size(women_onboard)
proportion_men_survived = np.sum(men_onboard) / np.size(men_onboard)

print('Proportion of women who survived is {}'.format(proportion_women_survived))
print('Proportion of men who survived is {}'.format(proportion_men_survived))

fare_ceiling = 40
data[data[0::,9].astype(np.float) >= fare_ceiling, 9] = fare_ceiling - 1.0
fare_bracket_size = 10
number_of_price_brackets = fare_ceiling / fare_bracket_size

number_of_classes = len(np.unique(data[0::,2]))

survival_table = np.zeros((2,number_of_classes, number_of_price_brackets))

for i in range(int(number_of_classes)):
    for j in range(int(number_of_price_brackets)):
        women_only_stats = data[(data[0::,4] == "female") & \
          (data[0:,2].astype(np.float) == i+1) & \
          (data[0:,9].astype(np.float) >= j*fare_bracket_size) & \
          (data[0:,9].astype(np.float) < (j+1)*fare_bracket_size), 1]

        men_only_stats = data[(data[0::,4] != "female") & \
          (data[0::,2].astype(np.float) == i+1) & \
          (data[0:,9].astype(np.float) >= j*fare_bracket_size) & \
          (data[0:,9].astype(np.float) < (j+1)*fare_bracket_size), 1]

        if len(women_only_stats) > 0:
          survival_table[0,i,j] = np.mean(women_only_stats.astype(np.float))

        if len(men_only_stats) > 0:
          survival_table[1,i,j] = np.mean(men_only_stats.astype(np.float))

#survival_table[ survival_table != survival_table ] = 0.

print (survival_table)