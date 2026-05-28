import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

type_labels = ['Movie', 'TV Show']
type_counts = [5079, 2407]
countries = ['United States','India','Unknown','United Kingdom','Japan','South Korea','Canada','Spain','France','Mexico']
country_totals = [2283, 838, 772, 331, 238, 181, 147, 137, 112, 99]
years = [2016, 2017, 2018, 2019, 2020, 2021]
movie_year = [850, 920, 1050, 980, 870, 409]
tv_year = [200, 250, 320, 380, 450, 600]

# 环形图
fig, ax = plt.subplots(figsize=(8,8))
wedges, texts, autotexts = ax.pie(type_counts, labels=type_labels, autopct='%1.1f%%',
    startangle=90, pctdistance=0.75, wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2),
    colors=['#FF6B6B','#4ECDC4'])
ax.text(0,0,f'Total\n{sum(type_counts)}',ha='center',va='center',fontsize=16,fontweight='bold')
for t in autotexts: t.set_fontsize(13); t.set_fontweight('bold')
ax.set_title('Netflix Content Distribution', fontsize=16, fontweight='bold')
plt.tight_layout(); plt.savefig('/home/hadoop/donut.png', dpi=200); plt.close()

# 水平柱状图
fig, ax = plt.subplots(figsize=(10,7))
colors = plt.cm.viridis_r([i/(len(countries)-1) for i in range(len(countries))])
bars = ax.barh(countries, country_totals, color=colors, edgecolor='white')
for bar, val in zip(bars, country_totals):
    ax.text(val+20, bar.get_y()+bar.get_height()/2, str(val), va='center', fontsize=11, fontweight='bold')
ax.set_xlabel('Number of Titles'); ax.set_title('Top 10 Countries by Content Volume')
ax.invert_yaxis(); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
plt.tight_layout(); plt.savefig('/home/hadoop/bar.png', dpi=200); plt.close()

# 趋势图
fig, ax1 = plt.subplots(figsize=(12,7))
ax2 = ax1.twinx()
ax1.plot(years, movie_year, 'o-', color='#FF6B6B', linewidth=2.5, markersize=10, label='Movie')
ax2.plot(years, tv_year, 's-', color='#4ECDC4', linewidth=2.5, markersize=10, label='TV Show')
ax1.fill_between(years, movie_year, alpha=0.15, color='#FF6B6B')
ax2.fill_between(years, tv_year, alpha=0.15, color='#4ECDC4')
ax1.set_xlabel('Year'); ax1.set_ylabel('Movie', color='#FF6B6B'); ax2.set_ylabel('TV Show', color='#4ECDC4')
ax1.set_title('Netflix Content Growth Trend')
lines = ax1.get_lines() + ax2.get_lines()
ax1.legend(lines, [l.get_label() for l in lines], loc='upper left')
plt.tight_layout(); plt.savefig('/home/hadoop/trend.png', dpi=200); plt.close()
print('All charts saved!')
