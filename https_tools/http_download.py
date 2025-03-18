import requests


def download_file_stream(url: str) -> requests.Response | None:
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to download file: {e}")


def iter_content_func(response: requests.Response, chunk_size: int = 1024 * 1024 * 10):
    for chunk in response.iter_content(chunk_size=chunk_size):
        yield chunk
    response.close()


def download_file(url: str) -> bytes | None:
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.content
        response.close()
        return content
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to download file: {e}")
