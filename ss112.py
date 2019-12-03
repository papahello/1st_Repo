import boto3
import sys
import csv
import configparser


aws_access_key_id = sys.argv[1]
aws_secret_access_key= sys.argv[2]
region_name  = sys.argv[3]

def get_human_readable_file_size(file_size):
    '''
    This function takes file size as input and returns in human readable form
    '''
    if file_size < 1203 :
        return str(file_size) + ' BYTES'
    if file_size >= 1204 and file_size<1048576:
        return str(file_size/1024) + ' KB'

    else:
        return str(file_size/1048576) + ' MB'




s3 = boto3.resource('s3', aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key,region_name=region_name)

file_name = 'test' + '.csv'

with open(file_name, mode='w') as csv_file:
    s3_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    s3_writer.writerow(['Bucket Name', 'Key', 'Size'])


    for bucket in s3.buckets.all():
        count = 0
        for obj in bucket.objects.all():
            size = get_human_readable_file_size(obj.size)
            if count == 0:
                s3_writer.writerow([bucket.name, obj.key, size])
                count = count + 1
            else:
                s3_writer.writerow(['', obj.key, size])
