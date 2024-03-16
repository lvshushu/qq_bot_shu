import http.client
import json
class Info_informession:
    def __init__(self, host="localhost", port=8080, verifyKey="Wuhao118744"):
        """
        :param host: 监听地址
        :param port: 监听端口
        :param verifyKey: key
        """
        self.VisitHttpPath = http.client.HTTPConnection(host, port)
        self.verifyKey = verifyKey
        self.sessionKey = self.bind()
        self.bot_qq = 2320864323 # 这里输入bot的qq号

    def bind(self):
        print('该程序由wh制作')
        auto = json.dumps({"verifyKey": self.verifyKey})
        VisitHttpPath = self.VisitHttpPath
        VisitHttpPath.request("POST", "/verify", auto)
        response = VisitHttpPath.getresponse()
        session = response.read().decode("utf-8")
        print("主人，恭喜您认证成功啦:" + str(session))

        sessionKey = json.loads(session)['session']
        bind = json.dumps({"sessionKey": sessionKey, "qq":2320864323 })  # 此处输入bot的qq号
        VisitHttpPath.request("POST", '/bind', bind)
        response = VisitHttpPath.getresponse().read().decode("utf-8")
        print("主人，恭喜你绑定成功啦:" + str(response))

        return sessionKey
