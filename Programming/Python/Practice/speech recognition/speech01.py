import speech_recognition as sr
r = sr.Recognizer()
mic = sr.Microphone.list_microphone_names()  # 顯示出所有麥克風的列表

micro = sr.Microphone(device_index=7)
with micro as source:
    print("Say something.")
    r.adjust_for_ambient_noise(source, duration=0.2)
    audio = r.listen(source)

# help(r.recognize_sphinx)

text = r.recognize_sphinx(audio, language='en-US', show_all=False)
print(text)
