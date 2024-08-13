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


def check_nginx():
    """Check method count"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    first_result = nginx_collection.count_documents({})

    method = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    print(f"{first_result} logs")
    print("Methods:")

    for one_method in method:
        result = nginx_collection.count_documents({"method": one_method})
        print(f"\t method {one_method}: {result}")
    status_check = nginx_collection.count_documents(
            {"method": "GET", "path": "/status"}
    )
    print(f"{status_check} status check")


if __name__ == "__main__":
    check_nginx()
