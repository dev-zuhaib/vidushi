import os
import os.path
import sys
import wave
from datetime import datetime
import pvporcupine
from pvrecorder import PvRecorder
import speech_recognition as sr
from talk import speak
import subprocess
import time

def main():
    os.system("python3 talk.py")


def Listner():
    keyword_paths=['./विदुषी_hi_raspberry-pi_v3_0_0.ppn']
    output_path = None
    audio_device_index = 1
    porcupine = pvporcupine.create(
        access_key='e3UwujzvAyMkj9bGgzwXlDMy7iKdlXkm434A7x3cKuJPOH+NA2oJLQ==',
        # library_path=args.library_path,
        model_path='./model.pv',
        keyword_paths=['./विदुषी_hi_raspberry-pi_v3_0_0.ppn'],
        sensitivities=([0.7] * len(keyword_paths))
        )
    recorder = PvRecorder(
    frame_length=porcupine.frame_length,
    device_index= audio_device_index)
    keywords = list()
    for x in keyword_paths:
        keyword_phrase_part = os.path.basename(x).replace('.ppn', '').split('_')
        if len(keyword_phrase_part) > 6:
            keywords.append(' '.join(keyword_phrase_part[0:-6]))
        else:
            keywords.append(keyword_phrase_part[0])


    
    recorder.start()

    print('Welcome to LPCPS, Lucknow')
    print('Say Vidushi to talk to me ... ')

    try:
        while True:
            pcm = recorder.read()
            # print("--->",pcm)
            result = porcupine.process(pcm)
            # print(result)

            if result >= 0:
                print('[%s] Detected %s' % (str(datetime.now()), keywords[result]))
                if(os.path.exists('/home/vidushi/Desktop/.Vidushi/ai.mp3')):
                    os.system('rm ~/Desktop/.Vidushi/ai.mp3')
                    os.system('killall ffplay')
                main()

    except KeyboardInterrupt:
        print('Stopping ...')
    finally:
        recorder.delete()
        porcupine.delete()

#
if __name__ == '__main__':
    # os.system('ffplay -v 0 -nodisp -autoexit welcome.mp3')
    os.chdir("/home/vidushi/Desktop/.Vidushi")
    #os.system("touch /home/vidushi/Desktop/test.txt")
    #subprocess.Popen(["python3","ui.py"])
    #time.sleep(10)
    Listner()
