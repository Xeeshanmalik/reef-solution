import unittest
from main import convert_to_html
import pandas as pd
import numpy as np

class MyTest(unittest.TestCase):
    def test(self):
        name=['ABC','DEF','GHI']
        project=['1','2','3']
        time=['11', '22','33']
        src_df = pd.DataFrame(columns=name, index=project)
        src_df = src_df.fillna('')
        np.fill_diagonal(src_df.values, time)
        for column in src_df:
            src_df[column] = src_df[column].str.encode('utf-8')
        df = convert_to_html(name, project, time, "output/test.html")
        self.assertItemsEqual(df, src_df)

