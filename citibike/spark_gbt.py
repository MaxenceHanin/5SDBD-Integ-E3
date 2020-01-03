from pyspark.ml import Pipeline
from pyspark.ml.classification import GBTClassifier
from pyspark.ml.feature import StringIndexer, VectorIndexer, VectorAssembler
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

from pyspark.sql import SparkSession
from pyspark.sql.types import ArrayType, DoubleType
from pyspark.sql.functions import monotonically_increasing_id
from pyspark.sql.functions import to_timestamp, month, hour, dayofweek
from pyspark.sql.functions import array, udf

# Inspired from Spark example
# https://spark.apache.org/docs/latest/ml-classification-regression.html#gradient-boosted-tree-classifier
# https://towardsdatascience.com/machine-learning-with-pyspark-and-mllib-solving-a-binary-classification-problem-96396065d2aa

# PySpark Dataframe tutorials
# https://www.analyticsvidhya.com/blog/2016/10/spark-dataframe-and-operations/
# https://sparkbyexamples.com/spark/different-ways-to-create-a-spark-dataframe/

spark = SparkSession\
        .builder\
        .appName("Citibike Spark Test")\
        .getOrCreate()

# Load and parse the data file, converting it to a DataFrame.
data = spark.read.format("csv").option("header", "true").load("../datasets/JC-201909-citibike-tripdata.csv")
data = data.withColumn("rowId", monotonically_increasing_id())


#### PREPROCESSING

# features = month, hour, weekday, start station id (, age, gender)
# prediction = end station id

data = data.withColumn("month", month("starttime"))\
            .withColumn("hour", hour("starttime"))\
            .withColumn("weekday", dayofweek("starttime"))

labelCol = "labels"
featuresCol = "features"

featuresCols = ["month", "hour", "weekday", "start station id"]

# featuresAssembler = VectorAssembler(inputCols=featuresCols, outputCol=featuresCol)
# featuresAssembler.transform(data)
features = array([data[feature].cast("double") for feature in featuresCols]).alias(featuresCol)
new_schema = ArrayType(DoubleType(), containsNull=False)
udf_foo = udf(lambda x:x, new_schema)
features = features.withColumn(featuresCol, udf_foo(featuresCol))

gbt_dataset = data.select(data["end station id"].cast("double").alias(labelCol), features)

gbt_dataset.show()

# Split the data into training and test sets (30% held out for testing)
(trainingData, testData) = gbt_dataset.randomSplit([0.7, 0.3])


#### TRAINING

featuresIndexer = VectorIndexer(inputCol= featuresCol, outputCol = "indexedFeatures").fit(gbt_dataset)

# Train a GBT model.
gbt = GBTClassifier(labelCol=labelCol, featuresCol="indexedFeatures", maxIter=10)
pipeline = Pipeline(stages=[featuresIndexer, gbt])

# Train model.
model = pipeline.fit(trainingData)

# Make predictions.
predictions = model.transform(testData)

# Select example rows to display.
predictions.select("prediction", featuresCol, labelCol).show(5)


#### EVALUATION

# Select (prediction, true label) and compute test error
evaluator = MulticlassClassificationEvaluator(
    labelCol=labelCol[0], predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print("Test Error = %g" % (1.0 - accuracy))

gbtModel = model.stages[0]
print(gbtModel)  # summary only

spark.stop()
