import time

# 获取当前时间戳
timestamp = time.time()

# 格式化本地时间为字符串
date_str = time.strftime("%Y.%m.%d", time.localtime(timestamp))

print(type(date_str))