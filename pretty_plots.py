import matplotlib.pyplot as plt
from matplotlib import cm
from itertools import cycle, zip_longest, product, chain
from numpy import linspace, ceil, arange


c_palette = cycle(cm.tab20(linspace(0,1,20)))


class txt_eff:
  '''thanks, Boubakr'''
  PURPLE = '\033[95m'
  CYAN = '\033[96m'
  DARKCYAN = '\033[36m'
  BLUE = '\033[94m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  RED = '\033[91m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'
  END = '\033[0m'

  
# EXPLANATORY ANALYSIS  
  
def column_hists(df, ncol=5, square_size=3):
  x, y = int(ceil(len(df.columns)/ncol)), ncol
  fig, axs = plt.subplots(x, y, figsize=(y*square_size, x*square_size))
  for ax, col in zip_longest(iter(axs), df.columns):
    if col:
      ax.hist(df[col], color=next(c_palette))
      ax.set_title(col)
    else: ax.axis('off')
  plt.tight_layout()
  plt.show()

                                          
def plot_corrs(df, method='pearson', plot_size=8,
               labels_off=False):
  table = df.corr(method=method)
  fig, ax = plt.subplots(figsize=(plot_size, plot_size))
  im = ax.imshow(table)
  
  if labels_off:
    ax.set_xticks([]), ax.set_yticks([])
    ax.set_xticklabels([]), ax.set_yticklabels([])
    
  else:
    ax.set_xticks(arange(table.shape[0]))
    ax.set_yticks(arange(table.shape[0]))
    ax.set_xticklabels(table.columns, fontsize=plot_size*1.6)
    ax.set_yticklabels(table.columns, fontsize=plot_size*1.6)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
           rotation_mode="anchor")

    for i in range(table.shape[0]):
      for j in range(table.shape[0]):
        sel_color = 'w' if table.iloc[i, j]<.5 else 'k'
        ax.text(j, i, table.iloc[i, j].round(2), fontsize=plot_size*1.6,
                ha="center", va="center", color=sel_color)
      
  for edge, spine in ax.spines.items():
    spine.set_visible(False)

  ax.set_title("Correlations plot", fontsize=plot_size*2.2)
  plt.tight_layout()
  plt.show()                                    
                                          

# CROSS-VALIDATION

def bulk_cv_jobs(models, xdatas, ydatas, product_jobs=False):
  if product_jobs:
    all_jobs = product(*[models, xdatas, ydatas])
  else:
    all_jobs = zip(models, xdatas, ydatas)
  return all_jobs


def rank_results(scores, item_names, score_names, main_score_id=0, round_by=5, return_only_best=False):
  results = sorted(zip(item_names, scores), key=lambda x: x[1][main_score_id], reverse=True)
  for res in results:
    name = res[0]
    print(txt_eff.BOLD + txt_eff.UNDERLINE + name + txt_eff.END)
    for n, score in enumerate(res[1]):
      effect = txt_eff.BOLD if n==main_score_id else ''
      print(effect + f'{score_names[n]}: {score:.{round_by}f}' + txt_eff.END)
    if return_only_best: return
    print('-'*10)
