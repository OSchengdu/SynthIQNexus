import requests

def generate_results():
    results = []
    for i in range(100):  # 生成 100 条数据
        result = {
            "summary": f"数据总结： 数据包含 2 行，12 列。数值字段 'Data Value' 的均值为 27.8，最大值为 30.7，最小值为 24.9。",
            "key_info": {
                "fields": ["Name", "Geo Place Name", "Data Value"],
                "values": ["Ozone (O3)", "Upper East Side-Gramercy", 24.9],
                "values_from_another": ["Fordham - Bronx Pk", 30.7]
            },
            "conclusions": [
                "数据中没有异常值。",
                "值高的地点是 Fordham - Bronx Pk（'Data Value' 为 30.7）"
            ],
            "raw_data": [
                {
                    "fields": ["Name", "Geo Place Name", "Data Value"],
                    "values": ["Ozone (O3)", "Upper East Side-Gramercy", 24.9],
                    "values_from_another": ["Fordham - Bronx Pk", 30.7]
                },
                {
                    "fields": ["Name", "Geo Place Name", "Data Value"],
                    "values": ["Ozone (O3)", "Upper East Side-Gramercy", 24.9],
                    "values_from_another": ["Fordham - Bronx Pk", 30.7]
                }
            ],
            "sources": {
                "url": "http://example.com/data",
                "db": "http://example.com/db"
            }

        }
        results.append(result)
    return results

# 发送数据到 results.py
def send_data_to_results(data):
    url = "http://127.0.0.1:8000/receive-data"
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print(f"Data sent successfully: {response.json()}")
        else:
            print(f"Failed to send data: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error sending data: {str(e)}")

# 主函数
if __name__ == "__main__":
    # 生成数据
    generated_data = generate_results()

    # 发送数据到 results.py
    for data in generated_data:
        send_data_to_results(data)
