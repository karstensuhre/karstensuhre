"""Quick summary of a Casanovo mzTab output."""
import sys
import statistics
from collections import Counter

path = sys.argv[1]
psms = []
with open(path) as f:
    header = None
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if parts[0] == "PSH":
            header = parts
        elif parts[0] == "PSM":
            psms.append(parts)

if not psms:
    print("No PSM rows found.")
    sys.exit(0)

# Casanovo's PSM column order: PSM | sequence | PSM_ID | accession | unique
# | database | database_version | search_engine | search_engine_score[1]
# | modifications | retention_time | charge | exp_mass_to_charge
# | calc_mass_to_charge | spectra_ref | pre | post | start | end
# | opt_ms_run[1]_aa_scores | opt_ms_run[1]_canonical_seq

scores = []
seqs = []
charges = []
seq_lens = []
for row in psms:
    seq = row[1]
    score = float(row[8])
    charge = int(row[11])
    scores.append(score)
    seqs.append(seq)
    charges.append(charge)
    seq_lens.append(len(seq))

print(f"PSM count: {len(psms)}")
print(f"Score: median={statistics.median(scores):.3f}, "
      f"mean={statistics.mean(scores):.3f}, "
      f"min={min(scores):.3f}, max={max(scores):.3f}")
hi = sum(1 for s in scores if s >= 0.9)
mid = sum(1 for s in scores if 0.5 <= s < 0.9)
lo = sum(1 for s in scores if s < 0.5)
print(f"  score >= 0.9: {hi} ({100*hi/len(scores):.1f}%)")
print(f"  0.5 <= score < 0.9: {mid} ({100*mid/len(scores):.1f}%)")
print(f"  score < 0.5: {lo} ({100*lo/len(scores):.1f}%)")
print(f"Length: median={statistics.median(seq_lens)}, "
      f"min={min(seq_lens)}, max={max(seq_lens)}")
print(f"Charge: {dict(Counter(charges))}")
print(f"Unique sequences: {len(set(seqs))}")
print()
print("Top 10 highest-confidence predictions:")
ranked = sorted(zip(scores, seqs, charges, seq_lens), reverse=True)[:10]
for s, seq, c, n in ranked:
    print(f"  {s:.3f}  z={c}  n={n}  {seq}")
print()
print("10 lowest-confidence predictions:")
ranked = sorted(zip(scores, seqs, charges, seq_lens))[:10]
for s, seq, c, n in ranked:
    print(f"  {s:.3f}  z={c}  n={n}  {seq}")
