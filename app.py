from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ✅ Apna Bitrix webhook URL yaha dalna
BITRIX_WEBHOOK_URL = "https://dubaivisa.bitrix24.com/rest/4914/uoux77ofw08qt0sc/crm.lead.add.json"

@app.route("/collectchat", methods=["POST"])
def collectchat():
    data = request.json  # Collect.chat se JSON input

    # Debug ke liye incoming data print karte hain
    print("Received from Collect.chat:", data)

    # ✅ Collect.chat ke fields ko Bitrix ke fields me map karna
    payload = {
        "fields": {
            "TITLE": "Lead from Collect.chat",
            "NAME": data.get("name", ""),
            "LAST_NAME": data.get("last_name", ""),
            "EMAIL": [
                {"VALUE": data.get("email", ""), "VALUE_TYPE": "WORK"}
            ],
            "PHONE": [
                {"VALUE": data.get("phone", ""), "VALUE_TYPE": "WORK"}
            ]
        }
    }

    # ✅ Bitrix24 API ko POST request bhejna
    response = requests.post(BITRIX_WEBHOOK_URL, json=payload)

    return jsonify({
        "status": "ok",
        "collectchat_data": data,
        "bitrix_response": response.json()
    })


if __name__ == "__main__":
    # Local testing ke liye
    app.run(host="0.0.0.0", port=5000, debug=True)
