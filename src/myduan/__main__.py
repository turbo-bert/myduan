import sys

#                 1       2
print("usager: $0 SQLFILE OUTFILE")

srcfile = sys.argv[1]
outfile = sys.argv[2]

with open(outfile, 'w') as foutfile:

    # step 1 // get tables


    tbl_names = []

    with open(srcfile, 'r') as f:
        for line in f:
            if line.startswith("CREATE TABLE "):
                tbl_name = line.split("`")[1]
                tbl_names.append(tbl_name)
                foutfile.write("tabelle %s\n")
