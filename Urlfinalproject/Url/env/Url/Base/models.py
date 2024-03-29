from django.db import models
from django.contrib.auth.models import User
from django.db import models
from joblib import dump, load
from io import BytesIO


class LogisticEvaluationReport(models.Model):
    accuracy = models.FloatField(null=True, blank=True)
    precision_class_0 = models.FloatField(null=True, blank=True)
    recall_class_0 = models.FloatField(null=True, blank=True)
    f1_class_0 = models.FloatField(null=True, blank=True)
    precision_class_1 = models.FloatField(null=True, blank=True)
    recall_class_1 = models.FloatField(null=True, blank=True)
    f1_class_1 = models.FloatField(null=True, blank=True)


class evaluationMetrics(models.Model):
    accuracy = models.FloatField(null=True, blank=True)
    precision_class_0 = models.FloatField(null=True, blank=True)
    recall_class_0 = models.FloatField(null=True, blank=True)
    f1_class_0 = models.FloatField(null=True, blank=True)
    precision_class_1 = models.FloatField(null=True, blank=True)
    recall_class_1 = models.FloatField(null=True, blank=True)
    f1_class_1 = models.FloatField(null=True, blank=True)


class StoredModel(models.Model):
    serialized_model = models.BinaryField()

    @property
    def model(self):
        return load(BytesIO(self.serialized_model))

    @model.setter
    def model(self, value):
        bio = BytesIO()
        dump(value, bio)
        self.serialized_model = bio.getvalue()


class StoredModel_scratch(models.Model):
    serialized_model = models.BinaryField()

    @property
    def model(self):
        return load(BytesIO(self.serialized_model))

    @model.setter
    def model(self, value):
        bio = BytesIO()
        dump(value, bio)
        self.serialized_model = bio.getvalue()


class PickleFile(models.Model):
    file = models.FileField(upload_to="pickle_files/", null=True, blank=True)


class ModelSelected(models.Model):
    text_field = models.CharField(max_length=100)


# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


# class File(models.Model):
#     Train_file = models.FileField(upload_to="files", null=True, blank=True)


class TestFile(models.Model):
    testFile = models.FileField(upload_to="testfiles")


# class SingleTrainFile(models.Model):
#     file = models.FileField(upload_to="Singlefiles")


class ConfusionMatrix(models.Model):
    true_positive = models.IntegerField()
    true_negative = models.IntegerField()
    false_positive = models.IntegerField()
    false_negative = models.IntegerField()


class LogisticRegressionConfusionMatrix(models.Model):
    true_positive = models.IntegerField()
    true_negative = models.IntegerField()
    false_positive = models.IntegerField()
    false_negative = models.IntegerField()
