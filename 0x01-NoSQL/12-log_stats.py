#!/usr/bin/env python3
"""
   Write a Python script that
   provides some stats about Nginx
   logs stored in MongoDB:

   Database: logs
   Collection: nginx
   Display (same as the example):
   first line: x logs where x is
   the number of documents
   in this collection

   second line: Methods:
   5 lines with the number of
   documents with the method =
   ["GET", "POST", "PUT", "PATCH", "DELETE"]
   in this order (see example below
   - warning: it’s a tabulation before each line)

   one line with the number of documents with:
   method=GET path=/status
"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    first_result = nginx_collection.count_documents({})

    second_result = nginx_collection.count_documents({"method": "GET"})
    post_result = nginx_collection.count_documents({"method": "POST"})
    put_result = nginx_collection.count_documents({"method": "PUT"})
    patch_result = nginx_collection.count_documents({"method": "PATCH"})
    delete_result = nginx_collection.count_documents({"method": "DELETE"})

    print(f"{first_result} logs")
    print("Methods:")
    print(f"\tmethod GET: {second_result}")
    print(f"\tmethod POST: {post_result}")
    print(f"\tmethod PUT: {put_result}")
    print(f"\tmethod PATCH: {patch_result}")
    print(f"\tmethod DELETE: {delete_result}")
    status_check = nginx_collection.count_documents(
            {"method": "GET", "path": "/status"}
    )
    print(f"{status_check} status check")
