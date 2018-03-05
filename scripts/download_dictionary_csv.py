import requests

def download_file_from_google_drive(id):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = False)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = False)

    import pdb;pdb.set_trace()
    csv_text = list(save_response_content(response))
    csv_text = ''.join(csv_text)
    return csv_text

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response):
    for chunk in response.iter_content(decode_unicode=True):
        if chunk: # filter out keep-alive new chunks
            yield chunk

if __name__ == "__main__":
    file_id = '101dprpGjFCSoSLa3bhrMsZwx_bfPrXxW'
    download_file_from_google_drive(file_id)
