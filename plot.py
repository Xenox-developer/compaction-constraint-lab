"""Render only saved audited counts; no inferred uncertainty or decorative claims."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
a=json.loads((ROOT/'results/audit.json').read_text());assert a['passed'] and a['calls']==64
with plt.rc_context({'font.family':'DejaVu Sans','font.size':15,'svg.fonttype':'none'}):
 fig,axes=plt.subplots(1,2,figsize=(12,6.4),layout='constrained',sharex=True)
 for ax,model,title in zip(axes,['qwen2.5:7b','qwen3:8b'],['Qwen2.5 7B','Qwen3 8B']):
  kinds=['full','summary_only','pinned'];labels=['Full history','Summary only','Summary + pinned rule'];values=[a['summary'][model][k]['exact'] for k in kinds]
  bars=ax.barh(range(3),values,color=['#575E66','#B35E00','#00769B'],height=.5)
  for y,v in enumerate(values):ax.text(v+.12,y,f'{v}/8',va='center',fontsize=18)
  ax.set_yticks(range(3),labels);ax.invert_yaxis();ax.set_xlim(0,9.3);ax.set_xticks([0,2,4,6,8]);ax.set_xlabel('Correct candidate sets');ax.set_title(title,fontweight='bold');ax.spines[['top','right']].set_visible(False);ax.grid(axis='x',alpha=.18);ax.set_axisbelow(True)
 for suffix in ['png','svg']:fig.savefig(ROOT/f'results/compaction-constraints.{suffix}',dpi=170,facecolor='white')
 plt.close(fig)
(ROOT/'evidence/chart-environment.json').write_text(json.dumps({'matplotlib':matplotlib.__version__,'input':'results/audit.json','script':'plot.py','metric':'Exact candidate-set matches out of8 per condition; zero axis; no inferential intervals.'},indent=2)+'\n')
