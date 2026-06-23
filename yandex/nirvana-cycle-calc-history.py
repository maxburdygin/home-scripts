from nirvana_api import *
from nirvana_api.blocks import *
from nirvana_api.highlevel_api import *
import time
from datetime import timedelta, date
import datetime

nirvana_token = "y1__xDmpb2RpdT-ARiPBSDPq58DrUFQ2QIWoxpVZ3q8HS2SjQVO5Nc"

workflow_id = 'c60b79de-1818-4bb9-adfe-cf8eee2b8d24'
original_instance = "473b0e96-4bc4-445d-a3c0-309c859fe724" #473b0e96-4bc4-445d-a3c0-309c859fe724        #"03155abc-8bf1-4ba6-b7f6-c862e105e866"
api = NirvanaApi(oauth_token=nirvana_token, ssl_verify=False)


def calc_week(device_id, rows, dayrange=7):
    timestamps = []

    for row in rows:
        timestamps.append(datetime.datetime.strptime(row.fielddate, "%Y-%m-%d"))

    timestamps.sort()

    dates_return = {date.strftime("%Y-%m-%d") for date in timestamps}
    for date in timestamps:
        for daynum in range(1, dayrange + 1):
            dates_return.add((date + datetime.timedelta(days=daynum)).strftime("%Y-%m-%d"))

    for day in dates_return:
        yield {"device_id": device_id, "week_fielddate": day}

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def run():

    # start_date = date(2022, 12, 14)
    # end_date = date(2023, 1, 1)
    #time.sleep(14400)
    # for single_date in daterange(start_date, end_date):
        #prev_date = (single_date - timedelta(1)).strftime("%Y-%m-%d")
    single_date  = date(2026, 1, 11)
    str_date = single_date.strftime("%Y-%m-%d")
    print("Helloworld!")
    print(str_date)
    print(single_date)
    new_instance_id = api.clone_workflow_instance(
        workflow_id=workflow_id,
        workflow_instance_id=original_instance
    )

    api.set_global_parameters(
        workflow_id=workflow_id,
        workflow_instance_id=new_instance_id,
        param_values=[
            {'parameter':'date', 'value': str_date}
        ]
    )

    api.start_workflow(
        workflow_id=workflow_id,
        workflow_instance_id=new_instance_id
    )

    time.sleep(2000)
    print("Done!")

run()