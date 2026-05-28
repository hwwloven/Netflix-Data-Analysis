from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when, sum as _sum, desc
from pyspark.sql.types import IntegerType

spark = SparkSession.builder \
    .appName("Netflix Analysis Final") \
    .getOrCreate()

# 读取清洗后的数据
df = spark.read.option("header", True).option("inferSchema", True) \
    .csv("hdfs://localhost:9000/user/hadoop/netflix_project/netflix_cleaned.csv")

# ---------- 数据类型修正 ----------
# 将 added_year 和 release_year 转为整数，并过滤掉无法转换的记录
df = df.withColumn("added_year", col("added_year").cast(IntegerType())) \
       .withColumn("release_year", col("release_year").cast(IntegerType()))
df = df.filter(col("added_year").isNotNull() & col("release_year").isNotNull())

print("=" * 50)
print("5.1 数据读取成功！")
df.printSchema()
print(f"有效记录总数：{df.count()}")

# ---------- 5.2 电影和电视剧占比 ----------
print("\n" + "=" * 50)
print("5.2 电影和电视剧占比")
type_counts = df.groupBy("type").agg(count("*").alias("count"))
total = df.count()
type_ratio = type_counts.withColumn("ratio", col("count") / total * 100)
type_counts.show()
type_ratio.show()

# ---------- 5.3 按年份统计添加节目数量 ----------
print("\n" + "=" * 50)
print("5.3 按年份统计添加的节目数量（added_year）")
added_year_counts = df.groupBy("added_year", "type") \
    .agg(count("*").alias("count")) \
    .orderBy("added_year")
added_year_counts.show(20)

# ---------- 5.4 按年份统计发布节目数量 ----------
print("\n" + "=" * 50)
print("5.4 按年份统计发布的节目数量（release_year）")
release_year_counts = df.groupBy("release_year", "type") \
    .agg(count("*").alias("count")) \
    .orderBy("release_year")
release_year_counts.show(20)

# ---------- 5.5 不同国家影视剧总量 Top10 ----------
print("\n" + "=" * 50)
print("5.5 不同国家影视剧总量（Top 10）")
country_counts = df.groupBy("country") \
    .agg(count("*").alias("total")) \
    .orderBy(desc("total"))
country_counts.show(10)

# ---------- 5.6 不同国家的电影/电视剧占比 ----------
print("\n" + "=" * 50)
print("5.6 不同国家的电影/电视剧占比（Top 10 国家）")
top_countries = [r["country"] for r in country_counts.limit(10).collect()]
country_type = df.filter(col("country").isin(top_countries)) \
    .groupBy("country", "type") \
    .agg(count("*").alias("count"))

from pyspark.sql.window import Window
windowSpec = Window.partitionBy("country")
country_type_ratio = country_type.withColumn(
    "country_total", _sum("count").over(windowSpec)
).withColumn("ratio", col("count") / col("country_total") * 100)
country_type_ratio.orderBy(desc("country_total"), "country", "type").show(20)

spark.stop()
