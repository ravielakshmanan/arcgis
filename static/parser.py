import csv, operator, json

filename = "data/transposed.csv"
total_dict = {}

with open(filename, newline='') as csvfile:
    data = list(csv.reader(csvfile))

sorted_data = sorted(data, key=operator.itemgetter(0, 1))

lat = sorted_data[0][0]
lng = sorted_data[0][1]
map_x = []
map_y = []
for row in sorted_data:
        # print(row['Latitude'], row['Longitude'])
        # break
        if row[0] == lat and row[1] == lng:
            time = row[3].split(' 16 ')
            map_x.append(time[-1])
            map_y.append(row[2])
        else:
            key = '(' + row[1] + ', ' + row[0] + ')'
            total_dict[key] = {'dates': map_x, 'data': map_y}
            map_x = []
            map_y = []
            lat = row[0]
            lng = row[1]
            time = row[3].split(' 16 ')
            map_x.append(time[-1])
            map_y.append(row[2])

with open('data_dictionary.json', 'w') as fp:
    json.dump(total_dict, fp)
