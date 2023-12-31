"""
并发上传本地文件到指定S3桶
需要指定的参数
total 总共需要上传的文件个数
bucket_name 桶的名字，不需要包含s3:// 前缀
local_dir 本地文件的路径
max_workers 最大线程数来模拟并发度
"""
import os.path
import threading
import boto3
import time
from concurrent.futures import ThreadPoolExecutor, Future

s3_client = boto3.client('s3')
# 总共需要上传的文件个数
total = 50
# 已经上传的文件个数
current = 0
# s3 桶名字 不需要带s://
bucket_name = "cunxin-bucket"
# 本地文件路径
# 请至少保证该目录下包含1个文件，工作线程会循环读取该目录下文件直到total
local_dir = "/Users/aqiao/Work/WorkDocs/"
# 最大并行度
max_workers = 10

mutex = threading.Lock()
# 创建线程池，初始化max_workers个线程。
pool = ThreadPoolExecutor(max_workers)


def upload_task(full_name, file_name):
    try:
        global current
        with mutex:
            if current < total:
                s3_file = f"{current}_{file_name}"
                s3_client.upload_file(full_name, bucket_name, s3_file)
                current += 1
                threading_name = threading.current_thread().name
                print(f"thread {threading_name} is uploading {s3_file}")
                return s3_file
            else:
                return ""
    except Exception as e:
        return str(e)


def upload_file():
    if os.path.exists(local_dir):
        # In case the quantity of files under local_dir is less than total
        # use the While loop to continue
        while current < total:
            for item in os.listdir(local_dir):
                full_name = os.path.join(local_dir, item)
                if os.path.isfile(full_name):
                    future = pool.submit(upload_task, full_name, item)
                    future.add_done_callback(done)
            time.sleep(1)
    else:
        print(f"{local_dir} is not existed")


def done(response):
    if response.result():
        print(f"File {response.result()} uploaded")


if __name__ == '__main__':
    upload_file()
    pool.shutdown(True)
