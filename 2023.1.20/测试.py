if data[0]['messageChain'][1]['type'] == 'Plain':
    text = data[0]['messageChain'][1]['text']
    member_name = data[0]['sender']['memberName']
    group_name = data[0]['sender']['group']['name']
    qq_sender = data[0]['sender']['id']
    qq_group = data[0]['sender']['group']['id']
    if group_name == '壮壮捡漏集团318':
        pass
    elif text == '爱丽丝':
        qq_group = data[0]['sender']['group']['id']
        self.Group_operate.Alice(qq_group, sessionKey)
    elif text == '宁红夜':
        self.Group_operate.bianshengning(qq_group, qq_sender, sessionKey)
    elif text == '胡为':
        self.Group_operate.bianshenghu(qq_group, qq_sender, sessionKey)
    elif text == '康康美女':
        self.Group_operate.random_jpg(qq_group, sessionKey)
    elif text == '康康帅哥':
        self.Group_operate.random_shuaige_jpg(qq_group, sessionKey)
    elif text == '对我发疯':
        self.Group_operate.fa_feng(member_name, qq_group, sessionKey)
    elif '360搜图' in text:
        msg = text.split(' ')[-1]
        self.Group_operate.search_jpg_360(qq_group, sessionKey, msg)
    else:
        if re.search("晚安", text):
            qq_sender = int(qq_sender)
            url = "http://localhost:8080/userProfile"
            sessionKey = self.sessionKey
            send_q = {
                "sessionKey": sessionKey,
                "target": int(qq_sender),
            }
            response = requests.get(url, params=send_q)
            friend_infor = response.json()
            sex = friend_infor['sex']
            for key, value in ato_reponse_group.items():
                self.Group_operate.sendmeassage_group(qq_group, qq_sender, value, sex, key,
                                                      sessionKey)
        for key, value in ato_reponse_group.items():
            self.Group_operate.sendmeassage_group(qq_group, qq_sender, value, text, key,
                                                  sessionKey)