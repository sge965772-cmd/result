"""Download and verify full core CSVs; requires an internet-enabled Python runtime."""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request

REPO='sge965772-cmd/result'
PREFIX='analysis/collision-results-20261012-v1'

def fetch(url):
    request=urllib.request.Request(url,headers={'User-Agent':'collision-analysis-reader'})
    with urllib.request.urlopen(request,timeout=60) as response:
        return response.read()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output-dir',type=Path,required=True)
    parser.add_argument('--case',choices=['all','U010','U0183','U0200','U0212'],default='all')
    parser.add_argument('--ref',default='main',help='Use a published full Git commit SHA for a pinned analysis')
    args=parser.parse_args()
    base=f'https://raw.githubusercontent.com/{REPO}/{args.ref}/'
    catalog=json.loads(fetch(base+PREFIX+'/catalog.json'))
    args.output_dir.mkdir(parents=True,exist_ok=True)
    for case in catalog['cases']:
        if args.case!='all' and case['case']!=args.case:
            continue
        destination=args.output_dir/case['direct_upload_csv']
        if destination.exists():
            if hashlib.sha256(destination.read_bytes()).hexdigest()==case['direct_upload_sha256']:
                print(case['case'],'already verified; not downloaded again');continue
            raise SystemExit('refuse overwrite of a different existing CSV: '+str(destination))
        blocks=[];header=None
        for part in case['parts']:
            raw=fetch(base+part['path'])
            if len(raw)!=part['bytes'] or hashlib.sha256(raw).hexdigest()!=part['sha256']:
                raise ValueError('CSV chunk integrity check failed: '+part['path'])
            first,body=raw.split(b'\n',1)
            if header is None:header=first
            elif first!=header:raise ValueError('inconsistent core CSV headers')
            blocks.append(body)
        data=header+b'\n'+b''.join(blocks)
        if len(data)!=case['direct_upload_bytes'] or hashlib.sha256(data).hexdigest()!=case['direct_upload_sha256']:
            raise ValueError('full reconstructed CSV hash mismatch')
        destination.write_bytes(data)
        print(case['case'],case['rows_including_retained_tails'],'rows',len(data),'bytes; verified')
    for name in ['README.md','DATA_DICTIONARY.md','catalog.csv']:
        destination=args.output_dir/name
        if not destination.exists():destination.write_bytes(fetch(base+PREFIX+'/'+name))

if __name__=='__main__':main()
