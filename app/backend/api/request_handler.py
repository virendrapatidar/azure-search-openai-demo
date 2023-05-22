import requests


# The API endpoint
base_url = "https://api.cassavaecocash.co.za/v3/"
uk_base_url = "https://api-gb.sasairemit.com/api/v3/"
headers = {'Content-Type': 'application/vnd.api+json', 'Accept': 'application/vnd.api+json'}

class RequestHandler():
    def post_request(self, endpoint, req_data, isUk):
        # A POST request to the API
        url = base_url + endpoint
        if(isUk):
            url = uk_base_url + endpoint
        post_response = requests.post(url, json=req_data, headers=headers)
        post_response_json = post_response.json()        
        return post_response_json

