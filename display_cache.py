#!/usr/bin/env python3

import pandas as pd
import pyarrow.parquet as pq
from IPython.display import display

df = pq.read_table(source='cache.parquet').to_pandas()
#df = pq.read_table(source='export (4)').to_pandas()
print()
display(df)
print()


