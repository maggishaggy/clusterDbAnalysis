#!/usr/bin/python

# This is NOT a pipe command.
#
# Given one (or multiple to string with ORs) annotation,
# returns all genes in the database matching that annotation.

import optparse, sqlite3

usage = "%prog \"Annotation 1\" \"Annotation 2\" ..."
description = "Given list of run IDs, returns a list of genes and clusters containing given word(s) in the annotation"
parser = optparse.OptionParser(usage=usage, description=description)
(options, args) = parser.parse_args()

# Change the annotations so that they are all LIKE %name%                                                                                                                                                      
teststr = tuple('%' + s + '%' for s in args)

con = sqlite3.connect("db/methanosarcina")
cur = con.cursor()

query = """SELECT processed.geneid, processed.annotation
           FROM processed
           WHERE ("""

for i in range(len(teststr)):
    query = query + "processed.annotation LIKE ? "
    if not i == len(teststr) - 1:
        query = query + "OR "
query = query + ");"

cur.execute(query, teststr)

for l in cur:
    s = list(l)
    stri = "\t".join(str(t) for t in s)
    print stri