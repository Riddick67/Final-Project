from django.shortcuts import render
import re
import csv
import pandas as pd
import numpy as np
from io import StringIO
from geopy.geocoders import Nominatim
from django.contrib import messages
from django.conf import settings


# from UrlPhising import settings
from .models import *
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from django.http import HttpResponse
from .Utils import *
from django.urls import reverse
import os
from django.core.files.storage import FileSystemStorage
from .models import PickleFile
import os


# from .forms import UploadPickleForm
from .models import PickleFile

import pickle

from sklearn.metrics import precision_recall_fscore_support
from django.http import HttpResponseRedirect

# Model Train Function:
global_list = []


def manual_result(request):
    return render(request, "manualresult.html")


def Home(request):
    if request.method == "POST":
        url = request.POST.get("homepage")
        if url.startswith("http://"):
            url = url[len("http://") :]
        elif url.startswith("https://"):
            url = url[len("https://") :]

        default = "lr"
        if ModelSelected.objects.exists():
            latest_model_selected = ModelSelected.objects.latest("id")
            text_field_value = latest_model_selected.text_field
            if text_field_value == "lr":
                print("lr is selected")
                res = Single_url_check_lr(url)
            else:
                print("mnb is selected")
                res = Single_url_check_Nb(url)
        else:
            res = Single_url_check_lr(url)

        messages.success(request, str(res))
        return redirect("home")
        # return HttpResponseRedirect(redirect_url)

    return render(request, "index.html")


def about_us(request):

    return render(request, "about.html")


def ourteam(request):
    return render(request, "ourteam.html")


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not User.objects.filter(username=username).exists():
            messages.info(request, "Username doesnt exist.")
            return redirect("/login/")
        user = authenticate(username=username, password=password)
        if user is None:
            messages.info(request, "Invalid credentials.")
            return redirect("/login/")
        else:
            messages.info(request, "Successful.")
            login(request, user)
            return redirect("/Userlog/")

    return render(request, "login.html")


def registration(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = User.objects.filter(username=username, password=password)
        if user.exists():
            messages.info(request, "Same username cant exist.")
            return redirect("/registration/")
        else:
            user = User.objects.create(
                first_name=first_name, last_name=last_name, username=username
            )
        user.set_password(password)
        user.save()
        messages.info(request, "Account Created Successfully")
        return redirect("/registration/")
    return render(request, "registration.html")


def manual_dataentry(request):
    if request.method == "POST":
        url = request.POST.get("homepage")
        if url.startswith("http://"):
            url = url[len("http://") :]
        elif url.startswith("https://"):
            url = url[len("https://") :]
        print(url)
        res1 = Single_url_check_Nb(url)
        res2 = Single_url_check_lr(url)
        messages.success(request, f"Result from Multinomial Naive Bayes: {res1}")
        messages.success(request, f"Result From Logistic Regression: {res2}")
        if "checkbox1" in request.POST:
            # Checkbox1 is selected
            print("Checkbox 1 is selected.")
            mnb = "mnb"
            model_selected = ModelSelected.objects.create(text_field=str(mnb))
            print("Naive Bayes is saved")
            model_selected.save()
        else:
            # Checkbox1 is not selected
            print("Checkbox 1 is not selected.")

        # Check if checkbox2 is selected
        if "checkbox2" in request.POST:
            # Checkbox2 is selected
            print("Checkbox 2 is selected.")
            lr = "lr"
            model_selected = ModelSelected.objects.create(text_field=str(lr))
            print("logistic_model is saved")
            model_selected.save()
        else:
            # Checkbox2 is not selected
            print("Checkbox 2 is not selected.")
        return redirect("manual_dataentry")
    return render(request, "manual.html")


def User_log(request):

    return render(request, "Userlogged.html")


def DataTrain(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get("file")
        if uploaded_file and uploaded_file.name.endswith(".pkl"):
            # Define the directory where files will be saved
            uploaded_file.name = "train_data.pkl"

            curr_dir = os.getcwd()
            folder_name = "uploads"
            upload_dir = os.path.join(curr_dir, folder_name)

            fs = FileSystemStorage(location=upload_dir)
            # Save the uploaded file to the specified directory
            if fs.exists(uploaded_file.name):

                fs.delete(uploaded_file.name)

            fs.save(uploaded_file.name, uploaded_file)
            # Get the file path
            file_path = os.path.join(upload_dir, uploaded_file.name)
            # Process the file as needed
            # ...
            print("Pickle file uploaded successfully:", file_path)
            return render(request, "DataTrain.html", {"file_path": file_path})
        else:
            print("No valid pickle file uploaded.")
    return render(request, "DataTrain.html")


def Trainmodel(request):
    Lr = LogisticRegression_Model()
    Nb = NaiveBayes_model()
    print("hello world")
    train_check = False

    if Lr and Nb:
        train_check = True
    while train_check:
        return render(request, "TrainedModel.html", {"train_check": train_check})

    return render(request, "TrainedModel.html", {"train_check": train_check})


def Testdata(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get("testFile")
        if uploaded_file and uploaded_file.name.endswith(".pkl"):
            # Define the directory where files will be saved
            uploaded_file.name = "test_data.pkl"

            curr_dir = os.getcwd()
            folder_name = "testfiles"
            upload_dir = os.path.join(curr_dir, folder_name)
            print(upload_dir)

            fs = FileSystemStorage(location=upload_dir)
            # Save the uploaded file to the specified directory
            if fs.exists(uploaded_file.name):

                fs.delete(uploaded_file.name)

            fs.save(uploaded_file.name, uploaded_file)
            # Get the file path
            file_path = os.path.join(upload_dir, uploaded_file.name)
            # Process the file as needed
            # ...
            print("Pickle file uploaded successfully:", file_path)
            print("testing")
            # Logistic_testing()
            # NaiveBayes_testing()
            return render(request, "testdata.html", {"file_path": file_path})
        else:
            print("No valid pickle file uploaded.")

    return render(request, "testdata.html")


def single_user(request):
    # error_message = None  # Initialize error_message
    # if request.method == "POST":
    #     uploaded_file = request.FILES.get("file")
    #     if uploaded_file:
    #         obj = SingleTrainFile.objects.create(file=uploaded_file)
    #         try:
    #             df = pd.read_csv(obj.file)
    #             print(df.head(5))
    #             return render(request, "singleusertrain.html", {"dataframe": df})
    #         except Exception as e:
    #             error_message = f"Error reading the file: {str(e)}"
    #             return render(
    #                 request, "singleusertrain.html", {"error_message": error_message}
    #             )

    return render(request, "singleusertrain.html")


def analytic(request):
    try:
        metrics = evaluationMetrics.objects.latest("id")
        Nb_accuracy = metrics.accuracy
        Nb_precision_class_0 = metrics.precision_class_0
        Nb_recall_class_0 = metrics.recall_class_0
        Nb_precision_class_1 = metrics.precision_class_1
        Nb_recall_class_1 = metrics.recall_class_1
        Nb_f1_class_0 = metrics.f1_class_0
        Nb_f1_class_1 = metrics.f1_class_1
        print(
            Nb_accuracy,
            Nb_precision_class_0,
            Nb_precision_class_1,
            Nb_recall_class_0,
            Nb_recall_class_1,
            Nb_f1_class_0,
            Nb_f1_class_1,
        )
        report = LogisticEvaluationReport.objects.latest("id")

        # Extract the values from the report object
        lr_accuracy = report.accuracy
        lr_precision_class_0 = report.precision_class_0
        lr_recall_class_0 = report.recall_class_0
        lr_precision_class_1 = report.precision_class_1
        lr_recall_class_1 = report.recall_class_1
        lr_f1_class_0 = report.f1_class_0
        lr_f1_class_1 = report.f1_class_1

        # Now you can use these values as needed
        print(
            lr_accuracy,
            lr_precision_class_0,
            lr_precision_class_1,
            lr_recall_class_0,
            lr_recall_class_1,
            lr_f1_class_0,
            lr_f1_class_1,
        )
        # Extract the values from the confusion matrix object
        confusion_matrix = ConfusionMatrix.objects.latest("id")
        true_positive = confusion_matrix.true_positive
        true_negative = confusion_matrix.true_negative
        false_positive = confusion_matrix.false_positive
        false_negative = confusion_matrix.false_negative

        lr_confusion_matrix = LogisticRegressionConfusionMatrix.objects.latest("id")
        lr_true_positive = lr_confusion_matrix.true_positive
        lr_true_negative = lr_confusion_matrix.true_negative
        lr_false_positive = lr_confusion_matrix.false_positive
        lr_false_negative = lr_confusion_matrix.false_negative

        evaluation_metrics = {
            "true_positive": 66,
            "true_negative": 33,
            "false_positive": 0,
            "false_negative": 1,
        }

        context = {
            "evaluation_metrics": evaluation_metrics,
            "saved_conf_matrix": confusion_matrix,
            "lr_saved_conf_matrix": lr_confusion_matrix,
            "Nb_accuracy": Nb_accuracy,
            "Nb_f1_class_0": Nb_f1_class_0,
            "Nb_precision_class_0": Nb_precision_class_0,
            "Nb_recall_class_0": Nb_recall_class_0,
            "Nb_precision_class_1": Nb_precision_class_1,
            "Nb_recall_class_1": Nb_recall_class_1,
            "Nb_f1_class_1": Nb_f1_class_1,
            # "saved_conf_matrix": confusion_matrix,
            "lr_accuracy": lr_accuracy,
            "lr_f1_class_0": lr_f1_class_0,
            "lr_precision_class_0": lr_precision_class_0,
            "lr_recall_class_0": lr_recall_class_0,
            "lr_precision_class_1": lr_precision_class_1,
            "lr_recall_class_1": lr_recall_class_1,
            "lr_f1_class_1": lr_f1_class_1,
        }

    except evaluationMetrics.DoesNotExist:
        return HttpResponse("no metrics to load")

    return render(request, "analysis.html", context)


def Testing(request):
    lr_test = Logistic_testing()
    Nb_test = NaiveBayes_testing()
    if Nb_test and lr_test:
        test_check = True
    while test_check:
        return render(request, "testing.html", {"test_check": test_check})
    return render(request, "testing.html")


def simultaionResult(request):
    return render(request, "simulationresult.html")


def logout(request):
    # clear_data = StoredModel.objects.all().delete()
    # # clear_analysis = analysisreport.objects.all().delete()
    # clear_file = File.objects.all().delete()
    # clear_testfile = TestFile.objects.all().delete()
    # clear_singlefile = SingleTrainFile.objects.all().delete()
    # clear_scratchmodel = StoredModel_scratch.objects.all().delete()
    # print(
    #     clear_data,
    #     # clear_analysis,
    #     clear_file,
    #     clear_testfile,
    #     clear_singlefile,
    #     clear_scratchmodel,
    # )
    return redirect("home")
