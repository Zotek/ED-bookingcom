# -*- coding: utf-8 -*-

import codecs
import csv


def to_csv(query_result, filename = "output.out"):

	output_file = codecs.open(filename, "w")

	with output_file as csvfile:
		writer = csv.writer(csvfile)
		for row in query_result:
			row = map(lambda x: unicode(x).encode('utf-8'), row)
			writer.writerow(row)