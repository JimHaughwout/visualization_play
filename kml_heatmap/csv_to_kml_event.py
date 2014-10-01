from sys import argv
import sys
import csv

if len(argv) != 3: # Usage guidance
	usage = "Usage: %s input_file.csv output_file" % argv[0]
	error = "You passed %d arguments." % len(argv)
	sys.exit("%s -- %s" % (usage, error))

script, source, destination = argv

if '.csv' not in source:
	usage = "Usage: %s input_file.csv num_slices output_file.json" % argv[0]
	error = "You passed %r for input_file.csv" % source
	sys.exit("%s -- %s" % (usage, error))


target = open(destination + '.kml', 'w')
data = open(source)
reader = csv.reader(data)
data_row_count = len(list(reader)) - 1
data_write_count = 0
invalid_count = 0
data.seek(0)

row_num = 0
for row in reader:
	if row_num == 0: #HEADER
		label = row # Labels only used for array
		num_cols = len(label) 
		if num_cols != 3:
			sys.exit("Expecting 3 columns, seeing %d." % num_cols)
	else:
		# Skip column 0 (date) 
		# Format and write column 1 and 2
		data_valid = True
		try:
			lat = float(row[1])
		except:
			print "Could not convert %r to lat for row %d... skipping this row." % (row[1], row_num)
			data_valid = False

		try:
			lng = float(row[2])
		except:
			print "Could not convert %r to lng for row %d... skipping this row." % (row[2], row_num)
			data_valid = False	 

		if data_valid:
			target.write("  new google.maps.LatLng(%f, %f),\n" % (lat, lng))
			data_write_count += 1
		else:
			invalid_count += 1
	row_num += 1

target.closed
print "SUCCESS: Wrote %d KML records from %d data records to %s. Skipped %d invalid records." % (data_write_count, data_row_count, destination, invalid_count)