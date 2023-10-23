import xml.etree.ElementTree as ET

# Adjust these variables before running
input_file_path = "./data/2024.xml"
output_file_path = "./output/2024.txt"
output_spacing_str = "\t"
use_threshold_val = True
threshold_val = 2 # don't take anything above this ft value.
remove_high_tides = True
print_header_row = True
line_termination_val = '\n'
# end of variables to adjust

# start of script
output = []

data_xml_node = 'data'

date_column = 'date'
day_column = 'day'
time_column = 'time'
ft_column = 'pred_in_ft'
highlow_column = 'highlow'

high_tide_val = 'H'

columns_to_grab = [
    date_column,
    day_column,
    time_column,
    ft_column,
]

def write_line(unterminated_str, file):
    
    file.write(unterminated_str + line_termination_val)

tree = ET.parse(input_file_path)
root = tree.getroot()
data = root.find(data_xml_node)

for item in data:

    # remove any high tides if control variable is set to true
    if (remove_high_tides and item.find(highlow_column) == high_tide_val):
        continue

    # grab data from row
    output_obj = {}
    
    for column in columns_to_grab:
        output_obj[column] = item.find(column).text

    # omit data if FT threshold is above the provided value
    if (use_threshold_val and threshold_val < float(output_obj[ft_column])):
        continue

    output.append(output_obj)

# send to output file - overwrites file
with open(output_file_path, 'w') as out_file:
    
    # if we want - print header row with column names
    if print_header_row:
        write_line(output_spacing_str.join(columns_to_grab), out_file)

    # write data
    for obj in output:
        
        # build line data
        line_data = []
        for column in columns_to_grab:
            line_data.append(obj[column])

        # write line
        write_line(output_spacing_str.join(line_data), out_file)
