from datetime import datetime

def read_data(path):
    data = {}
    with open(path, 'r') as file:
        for line in file:
            if data == {}:  # Fill the dictionary with header values
                headers = line.split(",")
                for i in range(len(headers)):
                    headers[i] = headers[i].strip("\n")  # if /n is present in the string remove it
                    data[headers[i]] = []  # Create place holders for data
                continue
            values = line.split(",")
            for i in range(len(headers)):
                values[i] = values[i].strip("\n")  # if /n is present in the string remove it
                if ":" not in values[i]:
                    values[i] = int(values[i])  # if value string doesn't contain ":" it must be an integer
                data[headers[i]].append(values[i])
    return data



def find_occurences(data):
    occurence_dict = {"Red": 0, "Yellow": 0, "Green": 0}
    for key in data.keys():  # iterate through keys
        if key in occurence_dict.keys():  # if the key is a color
            occurence_dict[key] = sum(data[key])
    return occurence_dict

def find_on_time(data):
    time_ON = {"Red": 0, "Yellow": 0, "Green": 0}
    for i in range(len(data["TimeActive"])):
        if data["TimeActive"][i] != 0 and any(data[color][i] == 1 for color in time_ON.keys()):  # if time isn't 0 and atleast one of the colors is 1
            time = data["TimeActive"][i]
            for key in time_ON.keys():
                time_ON[key] += time * data[key][i]  # adds time if color is 1
    return time_ON

def find_occurances_by_time(data, color, type):
    """
    type = False -> Returns str
    type = True -> Returns datetime class
    """
    captured_time = []
    for i in range(len(data[color])):
        if data[color][i] == 1:
            time = data["Time"][i]
            if type:
                time = datetime.strptime(time, '%H:%M:%S').time()
            captured_time.append(time)
    return captured_time
def find_cycles(data):
    cycle_count = 0
    order_id = 0
    order = [(1, 0, 0),
            (0, 1, 0),
            (0, 0, 1),
            (0, 1, 0),
            (1, 0, 0)]

    for i in range(len(data["Time"])):
        color_tuple = (data["Red"][i], data["Yellow"][i], data["Green"][i])
        if color_tuple == order[order_id]:
            order_id += 1
            if order_id == len(order) - 1:
                cycle_count += 1
                order_id = 0
        else:
            order_id = 0

    return cycle_count

def find_errors(data):
    error_count = 0
    for i in range(len(data["Time"])):
        color_tuple = (data["Red"][i], data["Yellow"][i], data["Green"][i])
        if sum(color_tuple) != 1:
            error_count += 1
    return error_count

if __name__ == "__main__":
    data = read_data('data.txt')
    occurances = find_occurences(data)
    print(f"Red light was turned on {occurances['Red']} times")
    print(f"Yellow light was turned on {occurances['Yellow']} times")
    print(f"Green light was turned on {occurances['Green']} times")
    time_ON = find_on_time(data)
    print(f"Total time Red light was on: {time_ON['Red']} seconds")
    print(f"Total time Yellow light was on: {time_ON['Yellow']} seconds")
    print(f"Total time Green light was on: {time_ON['Green']} seconds")
    green_occurances_by_time_str = find_occurances_by_time(data, "Green", False)
    green_occurances_by_time_class = find_occurances_by_time(data, "Green", True)
    print(f"All times when Green light was active: {green_occurances_by_time_str}")
    number_of_cycles = find_cycles(data)
    print(f"Amount of full cycles: {number_of_cycles}")
    error_count = find_errors(data)
    print(f"Error count: {error_count}")