import json

for i in range(100):
    data = {
        "이름": f"000000",
        # 여기에 필요한 다른 필드들을 추가할 수 있습니다.
    }

    filename = f"00000{i}.json"

    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)