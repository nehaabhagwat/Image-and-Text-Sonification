from collections import OrderedDict, defaultdict
import calendar
try:
    import matplotlib.pyplot as plt
except ImportError as e:
    print "Matplotlib could not be imported. Graphs will not be plotted"

filename = "1116082.csv"

dataset = open(filename, "r")

header_line = dataset.readline()

header_line = header_line.split(",")

temp_ind_num = header_line.index('"TAVG"') + 1
date_ind_num = header_line.index('"DATE"') + 1
data = dataset.readlines()

monthly_temp = {}
temperatures = []
for record in data:
    record = record.replace(",,,",",noise,noise,")
    record = record.replace(",,",",noise,")
    record = record.split(',')
    # print(record[11][1:len(record[11])-1])
    if record[date_ind_num].find("noise") == -1 and record[temp_ind_num].find("noise") == -1:
        monthly_temp.update({record[date_ind_num][1:len(record[date_ind_num])-1]:float(record[temp_ind_num][1:len(record[temp_ind_num])-1])})
        temperatures.append(record[temp_ind_num][1:len(record[temp_ind_num])-1])
minTemperature = min(temperatures)
maxTemperature = max(temperatures)

ordered_dict = OrderedDict(sorted(monthly_temp.items(), key=lambda t: t[0]))
# print ordered_dict
new_dict = defaultdict(list)
for date in ordered_dict.iterkeys():
    new_date = date[0:4]
    # print new_date
    if new_date in new_dict.iterkeys():
        new_dict[new_date] = [round((ordered_dict[date] + new_dict[new_date][0]),2), new_dict[new_date][1] + 1]
    else:
        new_dict[new_date] = ordered_dict[date], 1
    new_date = date[5:7]


# print new_dict
date_list = []
temp_list = []
for record in sorted(new_dict.iterkeys()):
    temp_list.append(new_dict[record][0] / new_dict[record][1])
    # temp_list.append(ordered_dict[record])
    # date_list.append(record)
    date_list.append(record)

# *********************CUMULATIVE GRAPH**************************************
try:
    fig, ax = plt.subplots()
    plt.title("Average temperature over the years")
    plt.xlabel("Year")
    plt.ylabel("Temperature")
    plt.bar(date_list, temp_list, color="black")
    for label in ax.xaxis.get_ticklabels():
        label.set_visible(False)
    for label in ax.xaxis.get_ticklabels()[::10]:
        label.set_visible(True)
    for tick in ax.get_xticklabels():
        tick.set_rotation(45)
    legend_text = "X axis:1 unit=1 year\nY axis:1 unit=10 F"
    plt.annotate(legend_text, (0.85, 1), xycoords = 'axes fraction')
    plt.savefig("cumulative_temperature_plot.jpg")
except Exception as e:
    print "Graph could not be generated due to the following error:"
    print e

# **********************MONTHLY GRAPH**************************************
print "Enter the number of the month for which you want to generate a graph"
correct_input = 0
monthly_data = {}
selected_month = 0
while correct_input != 1:
    selected_month = input()
    if selected_month <13 and selected_month>0:
        correct_input = 1
    else:
        print "Incorrect number entered. Please enter a number between 1 and 12."
for date in ordered_dict.iterkeys():
    new_date = date[5:7]
    if int(new_date) == selected_month:
        monthly_data.update({date[0:4]:ordered_dict[date]})

date_list = []
temp_list = []
for record in sorted(monthly_data.iterkeys()):
    date_list.append(record)
    temp_list.append(monthly_data[record])

try:
    fig, ax = plt.subplots()
    plt.title("Monthly temperature for the month of " + str(calendar.month_name[selected_month]))
    plt.xlabel("Year")
    plt.ylabel("Temperature")
    plt.bar(date_list, temp_list, color="black")
    for label in ax.xaxis.get_ticklabels():
        label.set_visible(False)
    for label in ax.xaxis.get_ticklabels()[::10]:
        label.set_visible(True)
    for tick in ax.get_xticklabels():
        tick.set_rotation(45)
    legend_text = "X axis:1 unit=1 year\nY axis:1 unit=10F"
    plt.annotate(legend_text, (0.85, 1), xycoords = 'axes fraction')
    plt.savefig("monthly_temperature_graph.jpg")
except Exception as e:
    print "Graph could not be generated due to the following error:"
    print e
