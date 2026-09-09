# The Chinese Hub — Django Shop

A Django website for a Chinese-food shop:
- Menu with categories, **Half / Full pricing**, and food photos
- **Add to Cart** (session-based, no login required)
- **₹40 service charge** automatically added to every bill
- Checkout → creates an **Order** and generates a real **PDF bill**
- **Owner contact card** on the homepage + floating **Call** button
- Order-success page has a **"Send Bill (PDF) via WhatsApp"** button that
  uses the phone's native share sheet to send the actual PDF file
- Full **Django admin** to manage menu items and orders

## Setup

```bash
cd chinese_hub_shop
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py seed_menu           # optional: loads a sample menu
python manage.py runserver
```

Visit http://127.0.0.1:8000/ for the shop, and http://127.0.0.1:8000/admin/
for the admin panel.

## Configure your shop's details

Edit `chinese_hub_shop/settings.py`:

```python
SHOP_NAME = "The Chinese Hub"
OWNER_NAME = "Owner Name"
OWNER_PHONE_DISPLAY = "+91 99999 99999"
OWNER_PHONE_TEL = "+919999999999"
OWNER_WHATSAPP_NUMBER = "919999999999"
SERVICE_CHARGE = Decimal("40.00")
```

## Sending the PDF bill via WhatsApp

The success page has one button: **"Send Bill (PDF) via WhatsApp."** It
fetches the generated PDF and hands it to the phone's native share sheet
(Web Share API) with the actual file attached — the customer picks
WhatsApp, then picks the shop's contact, and the real PDF lands in the
chat. This works on most modern phone browsers, no backend service or API
key needed.

If a browser doesn't support file sharing (older phones, most desktop
browsers), the button hides itself and a plain "Download the PDF" link
appears instead, with a note to attach it manually.

**Want zero-tap fully automatic sending instead?** That requires the real
WhatsApp Business API (e.g. Twilio), since only a server-side integration
can push a message (and attach a file) to the owner without anyone in the
loop tapping "send." That's a bigger, separate setup — ask if you want it
wired back in.
