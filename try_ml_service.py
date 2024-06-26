# This small script is only to replace bash and cURL which doesn't work well on Windows ;-(
import requests

post_data = {
    "instances": [
        [0.0, 0.0, 7.0, 14.0, 15.0, 4.0, 0.0, 0.0, 0.0, 7.0, 15.0, 4.0, 9.0, 12.0, 0.0, 0.0, 0.0, 6.0, 15.0, 1.0, 4.0, 14.0, 0.0, 0.0, 0.0, 0.0, 9.0, 13.0, 14.0, 7.0, 0.0, 0.0, 0.0, 0.0, 2.0, 16.0, 16.0, 4.0, 0.0, 0.0, 0.0, 0.0, 14.0, 7.0, 3.0, 15.0, 4.0, 0.0, 0.0, 0.0, 16.0, 3.0, 0.0, 13.0, 8.0, 0.0, 0.0, 0.0, 7.0, 16.0, 16.0, 10.0, 1.0, 0.0],
        [0.0, 0.0, 7.0, 13.0, 10.0, 1.0, 0.0, 0.0, 0.0, 1.0, 15.0, 3.0, 9.0, 10.0, 0.0, 0.0, 0.0, 3.0, 16.0, 4.0, 13.0, 11.0, 0.0, 0.0, 0.0, 0.0, 6.0, 12.0, 12.0, 16.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 12.0, 5.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 5.0, 11.0, 0.0, 0.0, 1.0, 11.0, 2.0, 0.0, 7.0, 11.0, 0.0, 0.0, 0.0, 7.0, 13.0, 16.0, 15.0, 4.0, 0.0],
        [0.0, 0.0, 1.0, 11.0, 15.0, 6.0, 0.0, 0.0, 0.0, 2.0, 15.0, 10.0, 16.0, 15.0, 0.0, 0.0, 0.0, 1.0, 14.0, 5.0, 6.0, 11.0, 0.0, 0.0, 0.0, 0.0, 5.0, 14.0, 14.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, 14.0, 16.0, 6.0, 0.0, 0.0, 0.0, 0.0, 10.0, 8.0, 6.0, 15.0, 1.0, 0.0, 0.0, 0.0, 9.0, 9.0, 4.0, 16.0, 3.0, 0.0, 0.0, 0.0, 1.0, 15.0, 15.0, 6.0, 0.0, 0.0],
    ]
}

if __name__ == '__main__':
    res = requests.post('http://localhost:8080/v1/models/model:predict', json=post_data)
    print(res)
    
    assert res.ok
    assert res.status_code == 200
    res.raise_for_status()
    
    print(res.text)
    assert res.text == '{"predictions":[8,9,8]}'
