# LogReader
LogReader is a Python program designed for parsing, converting, and visualizing data from specialized log files. It efficiently processes log entries containing hexadecimal values and categorizes them by identifiers, making it ideal for detailed data analysis and visualization.

## Features
Log File Parsing: Group log entries based on a 3-digit identifier.
Hexadecimal Data Conversion: Tailored conversion logic for different channels, turning raw hex data into meaningful numerical values.
Data Visualization: Generate plots for each channel and drive, offering a clear visual representation of the data.
CSV Output: Export processed data into CSV files, one for each channel.
## Getting Started
### Prerequisites
Ensure you have Python 3.x installed on your system. Additionally, you will need matplotlib for plotting:


1. Using PyCharm, Click Python Packages at the bottom of the window

2. Search for matplotlib and Click install on the right of the window

### Installation
Clone the repository or download the source code:

    git clone https://github.com/yourusername/LogReader.git
### Running LogReader
Place your log file in the same directory as the script, or provide the path to the file.

Run the script in a Python environment:

    python LogReader.py
Enter the log file name at the prompt.

## Usage
LogReader expects log files to follow a specific format:

    (YYYY-MM-DD HH:MM:SS.SSSSSS)  canX  XYZ   [N]  HH HH HH HH HH HH HH HH
    
Where XYZ is a 3-digit identifier, and HH represents hexadecimal values.

## Output
Plots: Visual representation for each channel's data.

CSV Files: channel_X_data.csv containing the processed data for channel X.
