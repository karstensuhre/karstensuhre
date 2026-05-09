"""
Convert a Bruker timsTOF .d directory to MGF for Casanovo.

Uses timsrust_pyo3.SpectrumReader, which yields one MS2 Spectrum per
identified precursor (DDA only). Each Spectrum already has aggregated
mz_values / intensities and an attached Precursor.

Usage:
    python tims_to_mgf.py <path/to/file.d> <out.mgf> [--max-spectra N]
"""

import sys
import argparse

import timsrust_pyo3 as tims


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("d_path")
    ap.add_argument("out_mgf")
    ap.add_argument("--max-spectra", type=int, default=0)
    ap.add_argument("--min-peaks", type=int, default=10)
    args = ap.parse_args()

    reader = tims.SpectrumReader(args.d_path)
    n_total = len(reader)
    print(f"Reader has {n_total} spectra", file=sys.stderr)

    written = 0
    skipped_no_charge = 0
    skipped_few_peaks = 0
    skipped_errors = 0

    with open(args.out_mgf, "w") as out:
        for i in range(n_total):
            if args.max_spectra and written >= args.max_spectra:
                break
            try:
                sp = reader.get(i)
            except Exception:
                skipped_errors += 1
                continue
            prec = sp.precursor
            if prec is None or prec.charge is None or prec.charge == 0:
                skipped_no_charge += 1
                continue
            mzs = sp.mz_values
            ints = sp.intensities
            if mzs is None or len(mzs) < args.min_peaks:
                skipped_few_peaks += 1
                continue

            title = f"index={sp.index};frame={prec.frame_index};im={prec.im:.4f}"
            out.write("BEGIN IONS\n")
            out.write(f"TITLE={title}\n")
            out.write(f"PEPMASS={prec.mz:.6f}\n")
            out.write(f"CHARGE={prec.charge}+\n")
            out.write(f"RTINSECONDS={prec.rt:.4f}\n")
            for mz, intensity in zip(mzs, ints):
                out.write(f"{mz:.6f} {intensity:.4f}\n")
            out.write("END IONS\n")
            written += 1
            if written % 1000 == 0:
                print(f"  wrote {written}", file=sys.stderr)

    print(
        f"Done. wrote={written} skipped_no_charge={skipped_no_charge} "
        f"skipped_few_peaks={skipped_few_peaks} skipped_errors={skipped_errors}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
