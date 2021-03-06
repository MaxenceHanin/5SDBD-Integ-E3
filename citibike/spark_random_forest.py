from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import StringIndexer, VectorIndexer, VectorAssembler
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

from pyspark.sql import SparkSession
from pyspark.sql.types import ArrayType, DoubleType
from pyspark.sql.functions import monotonically_increasing_id
from pyspark.sql.functions import to_timestamp, month, hour, dayofweek
from pyspark.sql.functions import array, udf

# Inspired from Spark example
# https://spark.apache.org/docs/latest/ml-classification-regression.html#random-forest-classifier
# https://towardsdatascience.com/machine-learning-with-pyspark-and-mllib-solving-a-binary-classification-problem-96396065d2aa

# PySpark Dataframe tutorials
# https://www.analyticsvidhya.com/blog/2016/10/spark-dataframe-and-operations/
# https://sparkbyexamples.com/spark/different-ways-to-create-a-spark-dataframe/

# How to do grid testing
# https://stackoverflow.com/questions/38767786/spark-mllib-2-0-categorical-features-in-pipeline

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

# Split the data into training and test sets (30% held out for testing)
(trainingData, testData) = data.randomSplit([0.8, 0.2])
print("Training on %d trips, Testing on %d trips" % (trainingData.count(), testData.count()))


#### TRAINING

stages = []

# Setup the pipeline
strIndexer = StringIndexer(inputCol="start station id", outputCol = "start station index")
stages += [strIndexer]

endIndexer = StringIndexer(inputCol="end station id", outputCol = "end station index", handleInvalid="keep")
stages += [endIndexer]

featuresCols = ["month", "hour", "weekday", "start station index"]
assembler = VectorAssembler(inputCols = featuresCols, outputCol="features")
stages += [assembler]

# Train a random forest model.
rfc = RandomForestClassifier(labelCol="end station index", featuresCol="features", numTrees=100, maxBins=64, maxDepth=7)
paramGrid = ParamGridBuilder().addGrid(rfc.numTrees, [50, 100, 200]).addGrid(rfc.maxDepth, [6, 7, 9, 11]).build()
stages += [rfc]

pipeline = Pipeline(stages=stages)

crossval = CrossValidator(estimator=pipeline,
                          estimatorParamMaps=paramGrid,
                          evaluator=MulticlassClassificationEvaluator(labelCol="end station index", predictionCol="prediction", metricName="accuracy"),
                          numFolds=3)

# Train model.
# <!> currently we do not use the CrossValidator.
# To use CrossValidator change the line to:
# model = crossval.fit(trainingData)
model = pipeline.fit(trainingData)

# Make predictions.
predictions = model.transform(testData)

# Select example rows to display.
predictions = predictions.select("prediction", "features", "end station index")
predictions.show(5)


#### EVALUATION

# Select (prediction, true label) and compute test error
evaluator = MulticlassClassificationEvaluator(labelCol="end station index", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print("Test Accuracy = %g" % (accuracy))

rfcModel = model.stages[-1]
print(rfcModel)  # summary only

spark.stop()
