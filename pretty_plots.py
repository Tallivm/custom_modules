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
  for n, col in zip_longest(range(x*y), df.columns):
    x0, x1 = 0+n//ncol, 0+n%ncol
    if col and (len(df.columns) <= ncol):
      axs[x1].hist(df[col], color=next(c_palette))
      axs[x1].set_title(col)
    elif col:
      axs[x0, x1].hist(df[col], color=next(c_palette))
      axs[x0, x1].set_title(col)
    else: axs[x0, x1].axis('off')
  plt.tight_layout()
  plt.show()

                                          
def plot_corrs(df, method='pearson', plot_size=8):
  table = df.corr(method=method)
  fig, ax = plt.subplots(figsize=(plot_size, plot_size))
  im = ax.imshow(table)
  ax.set_xticks(arange(len(df.columns)))
  ax.set_yticks(arange(len(df.columns)))
  ax.set_xticklabels(df.columns, fontsize=plot_size*1.6)
  ax.set_yticklabels(df.columns, fontsize=plot_size*1.6)
  plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")
  for edge, spine in ax.spines.items():
    spine.set_visible(False)

  for i in range(len(df.columns)):
    for j in range(len(df.columns)):
      sel_color = 'w' if table.iloc[i, j]<.5 else 'k'
      ax.text(j, i, table.iloc[i, j].round(2), fontsize=plot_size*1.6,
              ha="center", va="center", color=sel_color)

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


def score_cross_validation(model, x, y, scoring_dict,
                           cv=10, n_jobs=-1, return_estimator=False):
  results = cross_validate(model, x, y, cv=cv, n_jobs=n_jobs,
                            scoring=list(scoring_dict.values()),
                            return_estimator=return_estimator)
  chosen_results = []
  for score_name, scores in scoring_dict.items():
    biggest = max(results['test_'+scores])
    average = np.mean(results['test_'+scores])
    std = np.std(results['test_'+scores])
    chosen_results.extend([biggest, average, std])

  score_names = [[f'Max {name}', f'Mean {name}', f'Std {name}'] for name in scoring_dict.keys()]
  score_names = list(chain(*score_names))

  return chosen_results, score_names


def rank_results(scores, item_names, score_names, main_score_id=0, round_by=5):
  results = sorted(zip(item_names, scores), key=lambda x: x[1][main_score_id], reverse=True)
  for res in results:
    name = res[0]
    print(txt_eff.BOLD + txt_eff.UNDERLINE + name + txt_eff.END)
    for n, score in enumerate(res[1]):
      effect = txt_eff.BOLD if n==main_score_id else ''
      print(effect + f'{score_names[n]}: {score:.{round_by}f}' + txt_eff.END)
    print('-'*10)
