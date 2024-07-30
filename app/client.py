import requests

query = "What was Nike's revenue in 2023?"

url = "http://127.0.0.1:8000/pdf_rag/invoke"
data = {
    "input": {
        "input": query
    },
    "config": {},
    "kwargs": {}
}

response = requests.post(url, json=data)
print("Response status code:", response.status_code)
print("Query:", query)
print("Response:", response.json()["output"]["answer"])
