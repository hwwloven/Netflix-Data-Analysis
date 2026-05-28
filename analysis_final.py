from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum as _sum, desc, split, regexp_replace
from pyspark.sql.types import IntegerType
from pyspark.sql.window import Window

spark = SparkSession.builder \
    .appName("Netflix Analysis Final Fix") \
    .getOrCreate()

# ---------- 读取文本并解析列名（去掉双引号） ----------
raw_df = spark.read.text("hdfs://localhost:9000/user/hadoop/netflix_project/netflix_cleaned.csv")
header_row = raw_df.first()[0]
# 按制表符拆分列名，并去除每个列名两侧的引号
column_names = [c.strip('"') for c in header_row.split("\t")]
print("检测到的列名：", column_names)

# ---------- 将数据行按制表符拆分为独立列 ----------
data_df = raw_df.filter(col("value") != header_row) \
    .select([split(col("value"), "\t")[i].alias(column_names[i]) for i in range(len(column_names))])

# 列值中也可能有额外引号，去除掉（可选，为了后续类型转换）
for c in column_names:
    data_df = data_df.withColumn(c, regexp_replace(col(c), '"', ''))

# ---------- 类型转换与清洗 ----------
df = data_df.withColumn("added_year", col("added_year").cast(IntegerType())) \
            .withColumn("release_year", col("release_year").cast(IntegerType()))
df = df.filter(col("added_year").isNotNull() & col("release_year").isNotNull())

print("=" * 50)
print("5.1 数据读取成功！")
df.printSchema()
print(f"有效记录数：{df.count()}")

# ---------- 5.2 电影与电视剧占比 ----------
print("\n" + "=" * 50)
print("5.2 电影和电视剧占比")
type_counts = df.groupBy("type").agg(count("*").alias("count"))
total = df.count()
type_ratio = type_counts.withColumn("ratio", col("count") / total * 100)
type_counts.show()
type_ratio.show()

# ---------- 5.3 按添加年份统计 ----------
print("\n" + "=" * 50)
print("5.3 按年份统计添加的节目数量 (added_year)")
df.groupBy("added_year", "type").agg(count("*").alias("count")) \
    .orderBy("added_year").show(20)

# ---------- 5.4 按发布年份统计 ----------
print("\n" + "=" * 50)
print("5.4 按年份统计发布的节目数量 (release_year)")
df.groupBy("release_year", "type").agg(count("*").alias("count")) \
    .orderBy("release_year").show(20)

# ---------- 5.5 不同国家影视剧总量 Top10 ----------
print("\n" + "=" * 50)
print("5.5 不同国家影视剧总量 Top10")
country_counts = df.groupBy("country").agg(count("*").alias("total")).orderBy(desc("total"))
country_counts.show(10)

# ---------- 5.6 不同国家电影/电视剧占比 ----------
print("\n" + "=" * 50)
print("5.6 不同国家电影/电视剧占比 (Top 10)")
top_list = [r["country"] for r in country_counts.limit(10).collect()]
country_type = df.filter(col("country").isin(top_list)) \
    .groupBy("country", "type").agg(count("*").alias("count"))
windowSpec = Window.partitionBy("country")
country_type.withColumn("country_total", _sum("count").over(windowSpec)) \
    .withColumn("ratio", col("count") / col("country_total") * 100) \
    .orderBy(desc("country_total"), "country", "type").show(20)

spark.stop()
