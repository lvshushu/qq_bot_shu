import pyttsx3
def pyttsx3_debug(text,rate,volume,filename):
    import pyttsx3
    #参数说明: 六个重要参数,阅读的文字,语言(0-英文/1-中文),语速,音量(0-1),保存的文件名(以.mp3收尾),是否发言(0否1是)
    engine = pyttsx3.init()  # 初始化语音引擎
    engine.setProperty('rate', rate)  # 设置语速
    #速度调试结果:50戏剧化的慢,200正常,350用心听小说,500敷衍了事
    engine.setProperty('volume', volume)  # 设置音量
    voices = engine.getProperty('voices')  # 获取当前语音的详细信息
    engine.setProperty('voice', voices[0].id)  # 设置第一个语音合成器 #改变索引，改变声音。0中文,1英文(只有这两个选择)
    engine.save_to_file(text, filename) # 保存音频文件
    print(filename,"保存成功")

    engine.runAndWait() # pyttsx3结束语句(必须加)
    engine.stop() # pyttsx3结束语句(必须加)

    return filename



