import requests
import json
import webview
from urllib.parse import quote

# HTML content (same as provided, but as a string)
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>SIM Data Lookup</title>
  <style>
    body {
      margin: 0;
      padding: 0;
      background: #000;
      font-family: Arial, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      animation: fadeIn 1s ease-in-out;
    }
    .box {
      background: #111;
      border: 2px solid green;
      box-shadow: 0 0 25px red;
      padding: 30px 20px;
      border-radius: 15px;
      width: 100%;
      max-width: 400px;
      text-align: center;
      animation: fadeIn 1s ease-in-out;
    }
    .box h2 {
      color: green;
      font-size: 24px;
      margin-bottom: 20px;
    }
    .box input {
      width: 100%;
      padding: 12px;
      border-radius: 8px;
      border: none;
      margin-bottom: 20px;
      font-size: 16px;
      background: #333;
      color: white;
      box-shadow: inset 0 0 5px red;
    }
    .box button {
      width: 100%;
      padding: 12px;
      border: none;
      border-radius: 8px;
      margin: 10px 0;
      font-size: 16px;
      font-weight: bold;
      cursor: pointer;
      color: white;
      background: linear-gradient(90deg, #c00000, #ff0000);
      box-shadow: 0 0 15px red;
      transition: 0.3s;
    }
    .box button:hover {
      transform: scale(1.05);
      background: linear-gradient(90deg, #ff0000, #c00000);
    }
    .whatsapp-btn {
      background: linear-gradient(90deg, #25D366, #128C7E);
      box-shadow: 0 0 15px #25D366;
      color: white;
    }
    .telegram-btn {
      background: linear-gradient(90deg, #0088cc, #005577);
      box-shadow: 0 0 15px #0088cc;
      color: white;
    }
    #responseBox {
      color: white;
      margin-top: 20px;
      font-size: 16px;
      display: none;
      animation: fadeIn 1s ease-in-out;
      background: #222;
      border: 1px solid #444;
      padding: 15px;
      border-radius: 10px;
      text-align: left;
    }
    @keyframes fadeIn {
      0% { opacity: 0; }
      100% { opacity: 1; }
    }
  </style>
</head>
<body>
  <div class="box">
    <h2>🔍 DEEDAR ALI</h2>
    <input type="text" id="number" placeholder="Enter phone number" required />
    <button onclick="fetchData()">🔎 Get Details</button>
    <div id="responseBox"></div>
    <button id="shareButton" class="whatsapp-btn" onclick="shareWhatsApp()" style="display: none;">📲 Share on WhatsApp</button>
    <button class="whatsapp-btn" onclick="window.open('https://wa.link/4ombup', '_blank')">📢 Own WhatsApp</button>
    <button class="telegram-btn" onclick="window.open('https://www.facebook.com/akkasit.pon', '_blank')">✈️ Own Facebook</button>
  </div>
  <script>
    async function fetchData() {
      const number = document.getElementById("number").value.trim();
      const responseBox = document.getElementById("responseBox");
      const shareButton = document.getElementById("shareButton");
      if (!number) {
        alert("Please enter a phone number.");
        return;
      }
      const url = `https://api.allorigins.win/get?url=${encodeURIComponent(`https://fam-official.serv00.net/sim/api.php?num=${number}`)}`;
      try {
        const res = await fetch(url);
        const json = await res.json();
        const apiData = JSON.parse(json.contents);
        if (apiData.status === "success" && Array.isArray(apiData.data) && apiData.data.length > 0) {
          const user = apiData.data[0];
          const content = `
📞 Mobile: ${user.Mobile || "Not found"}
👤 Name: ${user.Name || "Not found"}
🆔 CNIC: ${user.CNIC || "Not found"}
📍 Address: ${user.Address || "Not found"}
📶 Operator: ${user.Operator || "Not found"}
          `;
          responseBox.innerText = content;
          responseBox.style.display = "block";
          shareButton.style.display = "inline-block";
        } else {
          responseBox.innerHTML = `<p style="color: yellow; font-size: 18px; font-weight: bold;">Data Not Found</p>`;
          responseBox.style.display = "block";
          shareButton.style.display = "none";
        }
      } catch (e) {
        responseBox.innerHTML = `<p style="color: green; font-size: 18px; font-weight: bold;">Error fetching data. Please try again later.</p>`;
        responseBox.style.display = "block";
        shareButton.style.display = "none";
      }
    }
    function shareWhatsApp() {
      const responseBox = document.getElementById("responseBox");
      const text = encodeURIComponent(responseBox.innerText);
      const url = `https://wa.me/?text=${text}`;
      window.open(url, '_blank');
    }
  </script>
</body>
</html>
"""

class Api:
    def __init__(self):
        self.number = ""
        self.response_data = ""

    def fetch_data(self, number):
        """Fetches data from the API based on the provided number."""
        self.number = number.strip()
        if not self.number:
            return "Please enter a phone number."

        url = f"https://api.allorigins.win/get?url={quote(f'https://fam-official.serv00.net/sim/api.php?num={self.number}')}"

        try:
            res = requests.get(url)
            res.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            json_data = res.json()
            api_data = json.loads(json_data.get('contents', '{}'))

            if api_data.get('status') == "success" and isinstance(api_data.get('data'), list) and len(api_data['data']) > 0:
                user = api_data['data'][0]
                content = f"""
📞 Mobile: {user.get('Mobile', 'Not found')}
👤 Name: {user.get('Name', 'Not found')}
🆔 CNIC: {user.get('CNIC', 'Not found')}
📍 Address: {user.get('Address', 'Not found')}
📶 Operator: {user.get('Operator', 'Not found')}
                """
                self.response_data = content
                return {"content": content, "show_share": True}
            else:
                self.response_data = "Data Not Found"
                return {"content": '<p style="color: yellow; font-size: 18px; font-weight: bold;">Data Not Found</p>', "show_share": False}

        except requests.exceptions.RequestException as e:
            self.response_data = "Error fetching data. Please try again later."
            return {"content": '<p style="color: green; font-size: 18px; font-weight: bold;">Error fetching data. Please try again later.</p>', "show_share": False}
        except json.JSONDecodeError as e:
            self.response_data = "Error decoding JSON. Please try again later."
            return {"content": '<p style="color: red; font-size: 18px; font-weight: bold;">Error decoding JSON. Please try again later.</p>', "show_share": False}


    def share_whatsapp(self):
        """Generates a WhatsApp share URL based on the response data."""
        text = quote(self.response_data)
        url = f"https://wa.me/?text={text}"
        return url

    def get_html(self):
        return html_content

if __name__ == '__main__':
    api = Api()

    def load_api(window):
        window.expose(api.fetch_data, api.share_whatsapp, api.get_html)

    webview.create_window(
        "SIM Data Lookup",
        html=html_content,
        js_api=api,
        on_top=True
    )
    webview.start()
