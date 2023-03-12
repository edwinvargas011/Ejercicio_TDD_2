import json
from urllib.request import urlopen
from datetime import datetime
import boto3
import os
import time


def lambda_handler(event, context):

    data1 = boto3.client('s3')
    
    ##Debido a que la pagina del banco esta en mantenimiento (https://totoro.banrep.gov.co/) se copia el archivo json y se accede a traves de este url  https://api.npoint.io/2ef60fcd7540294647cc
    with urlopen("https://api.npoint.io/2ef60fcd7540294647cc") as response:
        body=response.read()
        date_time = datetime.now()
        id_text=date_time.strftime("%Y%m%d  %H:%M:%S")
        client = boto3.client('s3')
        client.put_object(Body=body,Bucket='bucketdollar1',Key='data_value_dollar/'+"dolar_"+str(id_text[2:])+".txt")
        print('data_value_dollar/'+"dolar_"+str(id_text[2:])+".txt")
        
    name_object=data1.list_objects_v2(Bucket="bucketdollar1")['Contents'][1]['Key']
    time_new=datetime.now().strftime("%d %B, %Y %H:%M")
    response = data1.head_object(Bucket='bucketdollar1', Key=name_object)
    if(response['ResponseMetadata']['HTTPStatusCode']==200):
          data1.copy_object(Bucket='bucketdollar1', CopySource={'Bucket':'bucketdollar1','Key':name_object}, Key='data_value_dollar_new/dolar_'+time_new)
    time.sleep(2)
    data1.delete_object(Bucket="bucketdollar1",Key="data_value_dollar/"+name_object+".txt")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
