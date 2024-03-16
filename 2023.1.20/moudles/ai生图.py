import http.client
import json
conn = http.client.HTTPSConnection("ston.6pen.art")
payload = json.dumps({
   "prompt": "帅者",
   "model_id": 3,
   "height": 512,
   "fill_prompt": 0,
   "addition": {
      "cfg_scale": 7,
      "negative_prompt": "minim aliqua qui in sed"
   },
   "width": 512
})
headers = {
   'ys-api-key': '52fd6348c04865dd12e2268b838c5f1f',
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'Content-Type': 'application/json'
}
conn.request("POST", "/release/open-task", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))