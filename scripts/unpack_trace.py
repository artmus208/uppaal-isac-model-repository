"""Unpack a gzip trace to a new destination; never overwrite an existing file."""
import argparse, gzip, shutil
from pathlib import Path

ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('source',type=Path)
ap.add_argument('destination',type=Path)
args=ap.parse_args()
with gzip.open(args.source,'rb') as src, args.destination.open('xb') as dst:
    shutil.copyfileobj(src,dst)
print(args.destination.resolve())
