

import uuid


def get_purchase_invoice_image_upload_folder(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{str(uuid.uuid4())}.{ext}"
    return "/".join(["images", instance.branch.name, "purchase-invoice", filename])