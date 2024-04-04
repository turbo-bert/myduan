import sys
import os

if len(sys.argv) <= 1:
    #                 1       2       3
    print("usager: $0 SQLFILE OUTFILE DATADIR")
    sys.exit(0)

srcfile = sys.argv[1]
outfile = sys.argv[2]
outdir = sys.argv[3]

os.makedirs(outdir, exist_ok=True)

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

    # step 2 // get table column definitions
    tbl_columns = {}
    for t in tbl_names:
        state = "searching"
        cols = []
        for line in lines:
            if state == "searching":
                if line.startswith("CREATE TABLE `%s`" % t):
                    print("found %s" % t)
                    state = "found"
                    continue
            if state == "found":
                if line.strip().startswith("`"):
                    c_name = line.split("`")[1]
                    cols.append(c_name)
                    print("col %s" % c_name)
                else:
                    break
        tbl_columns[t] = cols

    # step 3 // save/print table column definitions
    for t in tbl_names:
        with open(os.path.join(outdir, t + ".def"), 'w') as tdf:
            tdf.write("\n".join(tbl_columns[t]))

    # step 4 // save INSERT statements for each table
    for t in tbl_names:
        with open(os.path.join(outdir, t + ".inserts"), 'w') as tisf:
            for line in lines:
                if line.strip().startswith("INSERT INTO `%s`" % t):
                    tisf.write("%s\n" % line)
