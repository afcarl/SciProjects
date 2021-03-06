from numpy.linalg import norm

import pandas as pd


from SciProjects.fruits import projectroot

category = ["EURODAT", "GYUM", "EV"]
isotope = ["DH1", "DH2", "D13C"]
volatile = ["METOH", "ACALD", "ETAC", "ACETAL", "2BUT",
            "1PROP", "2M1P", "1BUT", "2M1B", "3M1B"]
params_inc = ["D13C", "METOH", "ACALD", "ETAC", "ACETAL",
              "1PROP", "2M1P", "2M1B", "3M1B"]

data = pd.read_excel(projectroot + "Gyümölcs_adatbázis_összesített.xlsx", header=0)
valid = data[category + params_inc].dropna()
X = valid[params_inc]
X = (X - X.mean()) / X.std()
valid[params_inc] = X

ds = []

for categ in ("Alma", "Kajszi", "Málna"):
    x = valid[valid["GYUM"] == categ][params_inc].as_matrix()
    center = x.mean(axis=0)
    print(categ, "center:", center)
    ids = valid[valid["GYUM"] == categ][category].as_matrix()
    for ID, record in zip(ids, x):
        d = norm(center - record)
        ds.append(ID.tolist() + [d])

outchain = "\t".join(category + ["D"]) + "\n"
outchain += "\n".join("\t".join(map(str, line)) for line in ds)

with open(projectroot + "distances.csv", "w") as handle:
    handle.write(outchain.replace(".", ","))
