import requests
from django.conf import settings


def send_pdf_to_whatsapp(
    phone_number,
    pdf_path,
    filename,
    caption=""
):
    """
    Upload a PDF to WhatsApp and send it
    as an actual PDF document.
    """

    # ==========================================
    # STEP 1: Upload PDF to WhatsApp
    # ==========================================

    upload_url = (
        f"https://graph.facebook.com/"
        f"{settings.WHATSAPP_API_VERSION}/"
        f"{settings.WHATSAPP_PHONE_NUMBER_ID}/media"
    )

    headers = {
        "Authorization": (
            f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}"
        )
    }

    with open(pdf_path, "rb") as pdf_file:

        files = {
            "file": (
                filename,
                pdf_file,
                "application/pdf"
            )
        }

        data = {
            "messaging_product": "whatsapp",
            "type": "application/pdf",
        }

        response = requests.post(
            upload_url,
            headers=headers,
            files=files,
            data=data,
            timeout=60,
        )

    # Check upload result
    if not response.ok:

        print("PDF Upload Failed")
        print(response.text)

        return False

    # WhatsApp gives us a media ID
    media_id = response.json().get("id")

    if not media_id:

        print("Media ID not received")

        return False

    # ==========================================
    # STEP 2: Send PDF to customer
    # ==========================================

    send_url = (
        f"https://graph.facebook.com/"
        f"{settings.WHATSAPP_API_VERSION}/"
        f"{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    )

    send_headers = {
        "Authorization": (
            f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}"
        ),
        "Content-Type": "application/json",
    }

    payload = {

        "messaging_product": "whatsapp",

        "to": phone_number,

        "type": "document",

        "document": {

            "id": media_id,

            "caption": caption,

            "filename": filename,
        }
    }

    response = requests.post(
        send_url,
        headers=send_headers,
        json=payload,
        timeout=60,
    )

    # Check send result
    if not response.ok:

        print("PDF Send Failed")
        print(response.text)

        return False

    return True