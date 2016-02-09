import numpy as np
import pandas as pd
from datetime import date

# Build data
prd = [1, 2, 3, 4, 1, 2]
grp = ['A', 'A', 'A', 'A', 'B', 'B']
yr =  [2010, 2010, 2010, 2010, 2000, 2000]
mth = [7, 7, 7, 7, 8, 8]
day = [1, 13, 13, 21, 20, 15]
dt = [date(y, m, d) for y, m, d in zip(yr, mth, day)]
# Create data frame
df = pd.DataFrame({'Period': prd, 'Group': grp, 'Dates': dt},
                  columns=['Period', 'Group', 'Dates'])


df['median'] = df.groupby('Group')['Period'].transform(np.median)

# d = grouped['Period'].agg({'ref_median' : np.median, 'ref_mean' : np.mean, 'ref_std': np.std})
# df = df.join(d)

print df
