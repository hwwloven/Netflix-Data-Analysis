import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# ---------- 设置现代风格 ----------
sns.set_style("darkgrid")
sns.set_palette("Set2")
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150
plt.rcParams['font.size'] = 11

# ==================== 数据准备 ====================

# 类型占比
type_pd = pd.DataFrame({
    'type': ['Movie', 'TV Show'],
    'count': [5079, 2407]
})

# 国家 Top10
country_pd = pd.DataFrame({
    'country': ['United States','India','Unknown','United Kingdom','Japan',
                'South Korea','Canada','Spain','France','Mexico'],
    'total': [2283, 838, 772, 331, 238, 181, 147, 137, 112, 99]
})

# 各国电影/电视剧占比
country_type_pd = pd.DataFrame({
    'country': ['United States','United States','India','India','Japan','Japan',
                'South Korea','South Korea','United Kingdom','United Kingdom'],
    'type': ['Movie','TV Show','Movie','TV Show','Movie','TV Show','Movie','TV Show','Movie','TV Show'],
    'ratio': [70.48, 29.52, 92.00, 8.00, 31.51, 68.49, 17.68, 82.32, 46.53, 53.47]
})

# 模拟年份趋势数据（替换为你的实际数据）
year_data = pd.DataFrame({
    'year': [2016, 2017, 2018, 2019, 2020, 2021],
    'Movie': [850, 920, 1050, 980, 870, 409],
    'TV Show': [200, 250, 320, 380, 450, 600]
})

# ==================== 图表1：环形图（比饼图更现代） ====================
fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(
    type_pd['count'],
    labels=type_pd['type'],
    autopct='%1.1f%%',
    startangle=90,
    pctdistance=0.75,
    wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2),
    colors=['#FF6B6B', '#4ECDC4']
)
# 中心添加总数值
ax.text(0, 0, f"Total\n{type_pd['count'].sum()}", ha='center', va='center', fontsize=16, fontweight='bold')
for autotext in autotexts:
    autotext.set_fontsize(13)
    autotext.set_fontweight('bold')
ax.set_title('Netflix Content Distribution', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('/home/hadoop/donut_chart.png', dpi=200, bbox_inches='tight')
plt.close()
print("✅ 环形图已保存: donut_chart.png")

# ==================== 图表2：水平柱状图（Top10国家） ====================
fig, ax = plt.subplots(figsize=(10, 7))
colors = sns.color_palette("viridis_r", len(country_pd))
bars = ax.barh(country_pd['country'], country_pd['total'], color=colors, edgecolor='white', linewidth=1.2)
# 在每条柱子右侧标注数值
for bar, val in zip(bars, country_pd['total']):
    ax.text(val + 20, bar.get_y() + bar.get_height()/2, str(val),
            va='center', fontsize=11, fontweight='bold')
ax.set_xlabel('Number of Titles', fontsize=13, fontweight='bold')
ax.set_title('Top 10 Countries by Content Volume', fontsize=16, fontweight='bold')
ax.invert_yaxis()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('/home/hadoop/horizontal_bar.png', dpi=200, bbox_inches='tight')
plt.close()
print("✅ 水平柱状图已保存: horizontal_bar.png")

# ==================== 图表3：堆叠柱状图（各国电影/电视剧对比） ====================
pivot = country_type_pd.pivot(index='country', columns='type', values='ratio')
fig, ax = plt.subplots(figsize=(10, 7))
pivot.plot(kind='barh', stacked=True, ax=ax, color=['#FF6B6B', '#4ECDC4'], edgecolor='white', linewidth=1.2)
ax.set_xlabel('Percentage (%)', fontsize=13, fontweight='bold')
ax.set_title('Movie vs TV Show Ratio by Country (Top 5)', fontsize=16, fontweight='bold')
ax.legend(loc='lower right', fontsize=11)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
for c in ax.containers:
    ax.bar_label(c, fmt='%.1f%%', fontsize=9, fontweight='bold')
plt.tight_layout()
plt.savefig('/home/hadoop/stacked_bar.png', dpi=200, bbox_inches='tight')
plt.close()
print("✅ 堆叠柱状图已保存: stacked_bar.png")

# ==================== 图表4：双轴趋势图（年份趋势） ====================
fig, ax1 = plt.subplots(figsize=(12, 7))
ax2 = ax1.twinx()
# 电影折线
line1 = ax1.plot(year_data['year'], year_data['Movie'], marker='o', linewidth=2.5,
                 color='#FF6B6B', markersize=10, label='Movie')
# 电视剧折线
line2 = ax2.plot(year_data['year'], year_data['TV Show'], marker='s', linewidth=2.5,
                 color='#4ECDC4', markersize=10, label='TV Show')
# 填充区域
ax1.fill_between(year_data['year'], year_data['Movie'], alpha=0.15, color='#FF6B6B')
ax2.fill_between(year_data['year'], year_data['TV Show'], alpha=0.15, color='#4ECDC4')
ax1.set_xlabel('Year', fontsize=13, fontweight='bold')
ax1.set_ylabel('Movie Count', fontsize=13, fontweight='bold', color='#FF6B6B')
ax2.set_ylabel('TV Show Count', fontsize=13, fontweight='bold', color='#4ECDC4')
ax1.set_title('Netflix Content Growth Trend (2016-2021)', fontsize=16, fontweight='bold')
# 图例合并
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left', fontsize=11)
ax1.spines['top'].set_visible(False)
plt.tight_layout()
plt.savefig('/home/hadoop/trend_dual_axis.png', dpi=200, bbox_inches='tight')
plt.close()
print("✅ 双轴趋势图已保存: trend_dual_axis.png")

# ==================== 图表5：热力图（相关矩阵模拟） ====================
fig, ax = plt.subplots(figsize=(8, 6))
heatmap_data = pd.DataFrame({
    'Movie': [1.00, 0.85, 0.72, 0.68],
    'TV Show': [0.85, 1.00, 0.61, 0.55],
    'Content': [0.72, 0.61, 1.00, 0.91],
    'Country': [0.68, 0.55, 0.91, 1.00]
}, index=['Movie', 'TV Show', 'Content', 'Country'])
sns.heatmap(heatmap_data, annot=True, fmt='.2f', cmap='YlOrRd',
            vmin=0, vmax=1, linewidths=1, linecolor='white', ax=ax)
ax.set_title('Feature Correlation Heatmap', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('/home/hadoop/heatmap.png', dpi=200, bbox_inches='tight')
plt.close()
print("✅ 热力图已保存: heatmap.png")

print("\n🎉 全部炫酷图表生成完毕！")
