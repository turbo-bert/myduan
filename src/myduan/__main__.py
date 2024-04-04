import sys

#                 1       2
print("usager: $0 SQLFILE OUTFILE")

srcfile = sys.argv[1]
outfile = sys.argv[2]

with open(outfile, 'w') as foutfile:

    # step 0 // binary utf8 safe read
    lines = []
    with open(srcfile, 'rb') as f:
        _blob = f.read()
    lines = _blob.decode("utf-8", "replace").split("\n")

    # step 1 // get tables
    tbl_names = []
    for line in lines:
        if line.startswith("CREATE TABLE "):
            tbl_name = line.split("`")[1]
            tbl_names.append(tbl_name)
            foutfile.write("tabelle %s\n" % tbl_name)
