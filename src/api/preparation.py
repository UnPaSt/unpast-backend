from fileinput import filename
import json
import os
import uuid
import itertools

from django.core.files.storage import FileSystemStorage
from rest_framework.request import Request

from database.models import Task, Mail, Data

import numpy as np
import pandas as pd


def get_uid(model):
    uid = str(uuid.uuid4())
    while model.objects.filter(uid=uid).exists():
        uid = str(uuid.uuid4())
    return uid


def get_wd(uid):
    return os.path.join("/tmp", uid) + "/"


def get_matrix_path(uid):
    return os.path.join(get_wd(uid), uid + ".matrix")


def save_file(uid, request: Request):
    os.mkdir(get_wd(uid))
    og_filename, path = write_file(uid, request.FILES.get('file'))
    Data.objects.create(uid=uid, filename=og_filename, location=path)


def write_file(uid, file):
    fs = FileSystemStorage(location=get_wd(uid))
    filename = fs.save(uid, file)
    path = get_matrix_path(uid)
    os.system("mv " + os.path.join(get_wd(uid), filename) + " " + get_matrix_path(uid))
    return filename, path


def store_mail(uid, email):
    if email is not None and len(email) > 0:
        Mail.objects.create(uid=uid, mail=email)


def update_task(uid, req) -> Task:
    task = Task.objects.get(uid=uid)
    del req["mail"]
    task.request = json.dumps(req)
    task.status = "Ready"
    task.save()
    return task


def format_input(df):
    columns = df.columns.tolist()
    rows = df.index.tolist()
    data = df.stack().reset_index().to_numpy().tolist()
    return columns, rows, data


def read_input(data: Data):
    return pd.read_csv(data.location, sep='\t', index_col=0)


def get_formatted_input(data: Data, result):
    df = read_input(data)
    result_genes = set(itertools.chain(*[bicluster['genes'] for bicluster in result.values()]))
    result_samples = set(itertools.chain(*[bicluster['samples'] for bicluster in result.values()]))
    df = df.filter(result_samples)
    df = df.filter(result_genes, axis=0)
    columns, rows, values = format_input(df)
    return {'columns': columns, 'rows': rows, 'values': values}


