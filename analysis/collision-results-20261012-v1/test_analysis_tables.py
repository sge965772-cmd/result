import csv
import tempfile
import unittest
from pathlib import Path
from analysis_tables import convert_table, join_core_tables

class AnalysisTableBehavior(unittest.TestCase):
    def test_full_precision_nan_and_original_rows_survive_conversion(self):
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            src = folder/'source.dat'
            src.write_text('# t i gap pressure\n0.001 17 1.4133806292888758e-05 nan\n0.002 18 -0 inf\n',encoding='utf-8')
            result = convert_table(src,folder/'output','U010','s1','anchor_stats')
            with result['full_csv'].open(encoding='utf-8',newline='') as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(len(rows),2)
            self.assertEqual(rows[0]['gap'],'1.4133806292888758e-05')
            self.assertEqual(rows[0]['pressure'],'nan')
            self.assertEqual(rows[1]['gap'],'-0')
            self.assertEqual(rows[1]['pressure'],'inf')
            self.assertEqual([r['source_line'] for r in rows],['2','3'])

    def test_core_join_refuses_missing_rows_instead_of_inventing_values(self):
        with tempfile.TemporaryDirectory() as folder:
            folder=Path(folder)
            anchor=folder/'anchor.csv'; film=folder/'film.csv'
            anchor.write_text('case_id,segment_id,source_line,t,i,gap\nU010,s1,2,0.1,7,1e-5\n',encoding='utf-8')
            film.write_text('case_id,segment_id,source_line,t,i,pressure\nU010,s1,2,0.2,8,nan\n',encoding='utf-8')
            with self.assertRaises(ValueError):
                join_core_tables(anchor,film,folder/'core.csv')

if __name__=='__main__':
    unittest.main()
