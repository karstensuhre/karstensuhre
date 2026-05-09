"""Pre-seed spectrum_utils' UNIMOD cache with the modifications Casanovo emits,
so the mzTab writer doesn't try to fetch unimod.org (which is unreachable here).
"""
import datetime
import os
import pickle

import platformdirs

cache_dir = platformdirs.user_cache_dir("spectrum_utils", False)
os.makedirs(cache_dir, exist_ok=True)

# (mass, accession) by name; (mass, name) by accession.
UNIMOD = [
    ("Carbamidomethyl",   57.021464,  "UNIMOD:4"),
    ("Oxidation",         15.994915,  "UNIMOD:35"),
    ("Deamidated",         0.984016,  "UNIMOD:7"),
    ("Acetyl",            42.010565,  "UNIMOD:1"),
    ("Carbamyl",          43.005814,  "UNIMOD:5"),
    ("Ammonia-loss",     -17.026549,  "UNIMOD:385"),
    ("Phospho",           79.966331,  "UNIMOD:21"),
    ("Methyl",            14.015650,  "UNIMOD:34"),
    ("Dehydrated",       -18.010565,  "UNIMOD:23"),
    ("Dioxidation",       31.989829,  "UNIMOD:425"),
    ("Trioxidation",      47.984744,  "UNIMOD:345"),
    ("Pyro-glu",         -17.026549,  "UNIMOD:28"),
    ("Glu->pyro-Glu",    -18.010565,  "UNIMOD:27"),
    ("Formyl",            27.994915,  "UNIMOD:122"),
    ("Sulfo",             79.956815,  "UNIMOD:40"),
    ("GG",               114.042927,  "UNIMOD:121"),
]
cv_by_name = {name: (mass, accession) for (name, mass, accession) in UNIMOD}
cv_by_accession = {accession: (mass, name) for (name, mass, accession) in UNIMOD}

cv = (cv_by_accession, cv_by_name)
payload = (cv, datetime.datetime.now(datetime.timezone.utc))

path = os.path.join(cache_dir, "UNIMOD.pkl")
with open(path, "wb") as f:
    pickle.dump(payload, f)
print(f"Wrote {path} ({len(UNIMOD)} terms)")
