import requests

query = "What was Nike's revenue in 2023?"

url = "http://127.0.0.1:8000/chain/pdf_rag/invoke"
data = {"input": {"input": query}, "config": {}, "kwargs": {}}

response = requests.post(url, json=data, timeout=60)
print("Response status code:", response.status_code)
print("Query:", query)
print("Response:", response.json()["output"]["answer"])


query = "Is my motorcycle still under warranty?"

url = "http://127.0.0.1:8000/graph/adaptive_rag/invoke"
data = {"input": {"question": query}, "config": {}, "kwargs": {}}

response = requests.post(url, json=data, timeout=60)
print("Response status code:", response.status_code)
print("Query:", query)
print("Response:", response.json()["output"]["generation"])
