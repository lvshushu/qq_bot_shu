import base64
from urllib.parse import quote

def run():
    names = "王五\n\n张三"
    base64_str = base64.b64encode(quote(names).encode('utf-8')).decode('utf-8').replace('+', '-').replace('/', '_')
    print("http://namerena.github.io/#n=" + base64_str)

def main(event):
    winners = event.data.winners
    print("胜利者（输出）：")
    print("".join(winners))

if __name__ == "__main__":
    run()
