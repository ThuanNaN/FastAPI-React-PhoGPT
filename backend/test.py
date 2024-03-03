import requests

def test_health():
    response = requests.get('http://localhost:5000')
    assert response.status_code == 200

def test_instruction(data):
    response = requests.post('http://localhost:5000/instruction', json=data)
    assert response.status_code == 200

def test_chat(data):
    response = requests.post('http://localhost:5000/chat', json=data)
    assert response.status_code == 200


test_health()
test_instruction(
    data = {
        "input_prompt": "Xin chào"
    }
)

test_chat(
    data = {
        "input_prompt": [
            {"role": "user", "content": "Con gà có mấy chân"},
        ]
    }
)