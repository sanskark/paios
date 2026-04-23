import requests

URL = "http://127.0.0.1:8000/chat"

def test(msg):
    res = requests.post(URL, json={"message": msg})

    print("\n==============================")
    print("INPUT :", msg)
    print("STATUS:", res.status_code)
    try:
        print("JSON  :", res.json())
    except:
        print("❌ Not JSON response")

test("i go to gym at 6")
test("What time do I go to gym?")
