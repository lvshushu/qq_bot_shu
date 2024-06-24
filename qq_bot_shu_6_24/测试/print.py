import time

# 获取当前时间戳
timestamp = time.time()

# 将时间戳转换为本地时间
local_time = time.localtime(timestamp)

# 将本地时间格式化为年月日时
formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)

print(formatted_time)