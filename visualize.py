import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# 数据（来自分析结果）
type_pd = pd.DataFrame({
    'type': ['Movie', 'TV Show'],
    'count': [5079, 2407]
})
country_pd = pd.DataFrame({
    'country': ['United States','India','Unknown','United Kingdom','Japan',
                'South Korea','Canada','Spain','France','Mexico'],
    'total': [2283, 838, 772, 331, 238, 181, 147, 137, 112, 99]
})

# 1. 饼图
plt.figure(figsize=(7,7))
plt.pie(type_pd['count'], labels=type_pd['type'], autopct='%1.1f%%',
        startangle=140, colors=sns.color_palette('pastel')[0:2])
plt.title('Movie vs TV Show Share')
plt.savefig('/home/hadoop/type_pie.png', dpi=150)
plt.close()

# 2. 柱状图
plt.figure(figsize=(10,6))
sns.barplot(x='total', y='country', data=country_pd,
            palette=sns.color_palette('viridis_r', len(country_pd)))
plt.title('Top 10 Countries by Number of Titles')
plt.xlabel('Total Titles')
plt.tight_layout()
plt.savefig('/home/hadoop/country_bar.png', dpi=150)
plt.close()

print("Charts saved: type_pie.png, country_bar.png")
