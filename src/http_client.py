import requests


def get_json(url: str, params=None, headers=None):
    """
    Send a GET request and return JSON data.
    """

    try:
        print('making request.....')
        response = requests.get(url, params=params, headers=headers,timeout=10)

        response.raise_for_status()

        print("Status Code:", response.status_code)
        print("Request successful.")
        print(f"Response Time: {response.elapsed.total_seconds()} seconds")

        return response.json()
    

    except requests.exceptions.Timeout:
        print("Request timed out.")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None