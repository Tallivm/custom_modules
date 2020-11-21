import matplotlib.pyplot as plt
from matplotlib import cm
from itertools import cycle, zip_longest
from numpy import linspace, ceil

c_palette = cycle(cm.tab20(linspace(0,1,20)))

def column_hists(df, ncol=5, square_size=3):
  x, y = int(ceil(len(df.columns)/ncol)), ncol
  fig, axs = plt.subplots(x, y, figsize=(y*square_size, x*square_size))
  for n, col in zip_longest(x*y, df.columns):
    x0, x1 = 0+n//ncol, 0+n%ncol
    if col:
      axs[x0, x1].hist(df[col], color=next(c_palette))
      axs[x0, x1].set_title(col)
    else: axs[x0, x1].axis('off')
  plt.tight_layout()
  plt.show()
