import gzip
import shutil
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

def get_result_file(uid):
    return os.path.join("/tmp", uid+"_biclusters.tsv")

def get_matrix_path(uid):
    return os.path.join(get_wd(uid), uid + ".matrix")

def save_file(uid, request: Request):
    os.mkdir(get_wd(uid))
    og_filename, path = write_file(uid, request.FILES.get('file'))
    Data.objects.create(uid=uid, filename=og_filename, location=path)

def uncompress_file(path, filename, file_ending):
    if file_ending == "gz" or file_ending == "gzip":
        with gzip.open(os.path.join(path, filename), 'rb') as f_in:
            with open(os.path.join(path, filename+"_uncompressed"), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
                os.remove(os.path.join(path, filename))
    return filename+"_uncompressed"


def write_file(uid, file):
    fs = FileSystemStorage(location=get_wd(uid))
    filename = fs.save(uid, file)
    splits = file.name.split(".")
    file_ending = splits[-1]
    if file_ending == "gzip" or file_ending=="gz":
        filename = uncompress_file(get_wd(uid), filename, file_ending)
    filepath = os.path.join(get_wd(uid), filename)
    matrixpath = get_matrix_path(uid)
    os.system(f"mv '{filepath}' {matrixpath}")
    return file.name, matrixpath


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
    df.index = df.index.astype('string')
    result_genes = set(itertools.chain(*[bicluster['genes'] for bicluster in result.values()]))
    result_samples = set(itertools.chain(*[bicluster['samples'] for bicluster in result.values()]))
    df = df.filter(result_samples)
    df = df.filter(result_genes, axis=0)
    columns, rows, values = format_input(df)
    return {'columns': columns, 'rows': rows, 'values': values}


