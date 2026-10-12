"""Lossless token-to-CSV conversion of saved simulation tables."""
import csv
import io
import hashlib
from pathlib import Path

class NotTabular(ValueError):
    pass

def join_core_tables(anchor_csv, film_csv, destination):
    def read(path):
        with Path(path).open(encoding='utf-8',newline='') as f:
            reader=csv.DictReader(f);columns=reader.fieldnames;rows=list(reader)
        by_key={}
        for row in rows:
            key=(row['case_id'],row['segment_id'],row['t'],row['i'])
            if key in by_key:
                raise ValueError('duplicate original (case, segment, t, i) key')
            by_key[key]=row
        return columns,by_key
    ac,ar=read(anchor_csv);fc,fr=read(film_csv)
    if ar.keys()!=fr.keys():
        raise ValueError('anchor and film tables do not have exactly the same original keys')
    columns=['case_id','segment_id','time_s','iteration','anchor_source_line','film_source_line']
    ax=[x for x in ac if x not in ('case_id','segment_id','source_line')]
    fx=[x for x in fc if x not in ('case_id','segment_id','source_line')]
    columns+=['anchor__'+x for x in ax]+['film__'+x for x in fx]
    destination=Path(destination);destination.parent.mkdir(parents=True,exist_ok=True)
    with destination.open('w',encoding='utf-8',newline='') as f:
        writer=csv.writer(f,lineterminator='\n');writer.writerow(columns)
        for key,a in ar.items():
            r=fr[key]
            writer.writerow([key[0],key[1],key[2],key[3],a['source_line'],r['source_line']]+[a[x] for x in ax]+[r[x] for x in fx])
    return dict(path=destination,rows=len(ar),columns=columns)

def convert_table(source, destination, case, segment, table, max_part_bytes=512_000):
    source=Path(source); destination=Path(destination)
    lines=source.read_text(encoding='utf-8').splitlines()
    if not lines or not lines[0].startswith('# '):
        raise NotTabular('no original named table header')
    columns=lines[0][2:].split()
    if not columns or len(set(columns))!=len(columns):
        raise NotTabular('empty or duplicate original column names')
    records=[]
    for lineno,line in enumerate(lines[1:],2):
        if not line.strip() or line.startswith('#'):
            continue
        values=line.split()
        if len(values)!=len(columns):
            raise ValueError(f'{source.name}:{lineno}: {len(values)} fields != {len(columns)} original columns')
        records.append([case,segment,str(lineno)]+values)
    destination.mkdir(parents=True,exist_ok=True)
    header=['case_id','segment_id','source_line']+columns
    full=destination/f'{table}.csv'
    with full.open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(header);w.writerows(records)
    parts=[]; chunk=[]; part_size=0
    def encode(row):
        buffer=io.StringIO();csv.writer(buffer,lineterminator='\n').writerow(row)
        return buffer.getvalue().encode('utf-8')
    header_bytes=encode(header)
    for row in records:
        raw=encode(row)
        if len(header_bytes)+len(raw)>max_part_bytes:
            raise ValueError('one complete row exceeds chunk capacity')
        if chunk and part_size+len(raw)+len(header_bytes)>max_part_bytes:
            parts.append(chunk);chunk=[];part_size=0
        chunk.append(raw);part_size+=len(raw)
    if chunk or not parts:
        parts.append(chunk)
    paths=[]
    for i,chunk in enumerate(parts,1):
        path=destination/'parts'/f'{table}.part-{i:04d}.csv'
        path.parent.mkdir(exist_ok=True)
        path.write_bytes(header_bytes+b''.join(chunk));paths.append(path)
    return dict(full_csv=full,parts=paths,columns=columns,rows=len(records),
                source_bytes=source.stat().st_size,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
