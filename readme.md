## 功能
1.upload_to_s3_in_parallel.py

该工具用来把本地文件并发上传到S3桶。当你需要模拟并发上传场景来测试AWS服务的相关指标时可以考虑使用此工具
## 参数说明
修改文件中的参数来适配你的需求
- total 总共需要上传的文件个数，到达此个数后线程池退出
- bucket_name S3桶名，不要包含s3:// 前缀
- local_dir 本地文件的路径
- max_workers 最大线程数来模拟并发度

## 运行
1. 安装boto3，<code>pip3 install boto3</code>
2. 下载upload_to_s3_in_parallel.py文件，并根据需要修改上述参数
3. 命令行运行：<code>python3 upload_to_s3_in_parallel.py</code>
