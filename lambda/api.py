from __future__ import print_function
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime, timedelta, timezone
import json
import traceback
import os

#-----Dynamo Info change here------
TABLE_NAME = os.environ.get('TABLE_NAME', "default")
DDB_PRIMARY_KEY = "device_id"
DDB_SORT_KEY = "time"
#-----Dynamo Info change here------

dynamodb = boto3.resource('dynamodb')
table  = dynamodb.Table(TABLE_NAME)

#------------------------------------------------------------------------
def dynamo_query(device_id, search_time_since, search_time_until, limit):
    print("dynamo_query start")
    
    JST = timezone(timedelta(hours =+ 9), 'JST')
    now = datetime.now(JST).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
    
    time_condition = Key(DDB_SORT_KEY).lt(now)
    if search_time_since != None and search_time_until == None:
        time_condition = Key(DDB_SORT_KEY).lt(search_time_since)
    if search_time_since == None and search_time_until != None:
        time_condition = Key(DDB_SORT_KEY).gt(search_time_until)
    if search_time_since != None and search_time_until != None:
        time_condition = Key(DDB_SORT_KEY).between(search_time_since, search_time_until)

    
    val_list = []
    res = None
    
    if limit == None: 
        res = table.query(
            KeyConditionExpression = Key(DDB_PRIMARY_KEY).eq(device_id) & time_condition, 
            ScanIndexForward = False
        )
    else: 
        res = table.query(
            KeyConditionExpression = Key(DDB_PRIMARY_KEY).eq(device_id) & time_condition, 
            ScanIndexForward = False,
            Limit = limit
        )
        
    print(res)

    for row in res['Items']:
        item_dict = {
            "time":row['time'],
            "temperature": float(row['temperature']),
            "humidity": float(row['humidity']),
            "co2": int(row['co2'])
        }
        val_list.append(item_dict)
    print(val_list)
        
    result = {
        "device_id": device_id,
        "data": val_list
    }

    return result

#------------------------------------------------------------------------
# call by Lambda here.
#  Event structure : API-Gateway Lambda proxy post
#------------------------------------------------------------------------
def lambda_handler(event, context):
    #Lambda Proxy response back template
    http_res = {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin" : "*"},
        "body": "",
        "isBase64Encoded": False
    }

    try:
        print("lambda_handler start")
        print(json.dumps(event))

        # get Parameters
        path_parameters = event.get('pathParameters')
        request_parameters = event.get('queryStringParameters')
        
        print(path_parameters)
        print(request_parameters)
        
        device_id = int(path_parameters["device_id"])
        
        print(device_id)
        
        search_time_since = None
        search_time_until = None
        limit = None

        if request_parameters != None:
            search_time_since = request_parameters.get('since')
            search_time_until = request_parameters.get('until')
            if request_parameters.get('limit') != None:
                limit = int(request_parameters.get('limit'))
        
        print(search_time_since)
        print(search_time_until)
        print(limit)

        res_item_dict = dynamo_query(device_id, search_time_since, search_time_until, limit)
        http_res['body'] = json.dumps(res_item_dict)

    except Exception as e:
        print(traceback.format_exc())
        http_res["statusCode"] = 500
        http_res["body"] = "Lambda error. check lambda log"

    print("response:{}".format(json.dumps(http_res)))
    return http_res
