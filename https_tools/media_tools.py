def get_mime_type(images_path: str):
    if images_path.endswith(".jpg") or images_path.endswith(".jpeg"):
        return "image/jpeg"
    if images_path.endswith(".png"):
        return "image/png"
    raise Exception(f"Error support mime_type {images_path}")
