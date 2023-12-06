import re
import csv
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime

# Define the regular expression to match the 3-digit identifier
log_line_regex = r"\s+(\d{3})\s+"

# Define the identifiers for each channel
channel_identifiers = {
    "1": ['181', '182', '183', '184'],
    "2": ['281', '282', '283', '284'],
    "3": ['381', '382', '383', '384'],
    "4": ['481', '482', '483', '484']
}

def parse_and_group_log_lines(log_file_path):
    grouped_logs = defaultdict(list)
    with open(log_file_path, 'r') as file:
        for line in file:
            match = re.search(log_line_regex, line)
            if match:
                identifier = match.group(1)
                grouped_logs[identifier].append(line.strip())
    return grouped_logs

def convert_hex_values(data, conversion_identifier):
    log_channel = conversion_identifier[0]
    hex_values = data.split()
    actualTorqueScale = 0.001

    if log_channel == "1":
        #statusWord = int.from_bytes(bytes.fromhex(''.join(hex_values[:2])), byteorder='little', signed=False)
        controlEffort = int.from_bytes(bytes.fromhex(''.join(hex_values[2:4])), byteorder='little', signed=True)
        actualTorque = actualTorqueScale * int.from_bytes(bytes.fromhex(''.join(hex_values[4:])), byteorder='little', signed=True)
        return controlEffort, actualTorque

    elif log_channel == "2":
        desiredPosition = int.from_bytes(bytes.fromhex(''.join(hex_values[:4])), byteorder='little', signed=True)
        actualPosition = int.from_bytes(bytes.fromhex(''.join(hex_values[4:])), byteorder='little', signed=True)
        return desiredPosition, actualPosition

    elif log_channel == "3":
        desiredSpeed = int.from_bytes(bytes.fromhex(''.join(hex_values[:4])), byteorder='little', signed=True)
        actualSpeed = int.from_bytes(bytes.fromhex(''.join(hex_values[4:])), byteorder='little', signed=True)
        return desiredSpeed, actualSpeed

    elif log_channel == "4":
        sensor = int(hex_values[5], 16)
        return sensor, sensor

def prepare_data_for_plotting(grouped_logs):
    data_for_plotting = defaultdict(lambda: defaultdict(lambda: {'times': [], 'values1': [], 'values2': []}))
    for channel, ids in channel_identifiers.items():
        for id_ in ids:
            if id_ in grouped_logs:
                for entry in grouped_logs[id_]:
                    # Extract date-time and data
                    datetime_str = re.search(r"\((.*?)\)", entry).group(1)
                    datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f')
                    data_part = entry.split()[-8:]
                    data_str = ' '.join(data_part)
                    converted_data1, converted_data2 = convert_hex_values(data_str, id_)
                    # Parse converted data and add to data_for_plotting
                    data_for_plotting[channel][id_]['times'].append(datetime_obj)
                    data_for_plotting[channel][id_]['values1'].append(converted_data1)
                    data_for_plotting[channel][id_]['values2'].append(converted_data2)

    return data_for_plotting

def write_to_csv(data_for_plotting):
    for channel, drives_data in data_for_plotting.items():
        if channel == "1":
            title_value1 = "Control Effort"
            title_value2 = "Actual Torque"
        elif channel == "2":
            title_value1 = "Desired Position"
            title_value2 = "Actual Position"
        elif channel == "3":
            title_value1 = "Desired Speed"
            title_value2 = "Actual Speed"
        elif channel == "4":
            title_value1 = "0 = Home, 1 = End"
            title_value2 = "0 = Home, 1 = End"
        with open(f'channel_{channel}_data.csv', 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['PDO_ID', 'DateTime', f'{title_value1}', f'{title_value2}'])
            for PDO_ID, data in drives_data.items():
                for datetime_obj, val1, val2 in zip(data['times'], data['values1'], data['values2']):
                    csv_writer.writerow([PDO_ID, datetime_obj, val1, val2])

def plot_data_by_channel_and_drive(data_for_plotting):
    for channel, drives_data in data_for_plotting.items():

        y_axis_limits = [float('-4'), float('4')]

        if channel == "1":
            title_value1 = "Control Effort"
            title_value2 = "Actual Torque"
            color1 = 'darkred'
            color2 = 'orange'
        elif channel == "2":
            title_value1 = "Desired Position"
            title_value2 = "Actual Position"
            color1 = 'blue'
            color2 = 'green'
        elif channel == "3":
            title_value1 = "Desired Speed"
            title_value2 = "Actual Speed"
            color1 = 'purple'
            color2 = 'brown'
        elif channel == "4":
            title_value1 = "0 = Home, 1 = End"
            title_value2 = "0 = Home, 1 = End"
            color1 = 'black'
            color2 = 'black'

        if channel != "4":
            for drive, data in drives_data.items():
                for val1, val2 in zip(data['values1'], data['values2']):
                    y_axis_limits[0] = min(y_axis_limits[0], val1, val2)
                    y_axis_limits[1] = max(y_axis_limits[1], val1, val2)

        fig, axs = plt.subplots(len(drives_data), 1, figsize=(10, 6 * len(drives_data)), sharex=True)
        fig.suptitle(f'Channel {channel} Data by Drive')

        for i, (drive, data) in enumerate(drives_data.items()):
            if channel != "4":
                axs[i].plot(data['times'], data['values1'], label=f'{title_value1}', color=color1, alpha=0.7)
                axs[i].plot(data['times'], data['values2'], label=f'{title_value2}', color=color2, alpha=0.7)
            else:
                axs[i].plot(data['times'], data['values1'], 'o', label=f'{title_value1}', color=color1, alpha=0.7)
            axs[i].set_ylim(y_axis_limits[0], y_axis_limits[1])
            axs[i].set_ylabel(f'Drive {drive[2]}')
            axs[i].legend()
            axs[i].grid(True)

        plt.xlabel('Time (Portion A)')
        plt.tight_layout()
        plt.show()

# Main execution
log_file_path = input('Please input the filename (Ex: filename.log):')

grouped_logs = parse_and_group_log_lines(log_file_path)

data_for_plotting = prepare_data_for_plotting(grouped_logs)

write_to_csv(data_for_plotting)

plot_data_by_channel_and_drive(data_for_plotting)
