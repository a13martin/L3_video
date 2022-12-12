import os
import subprocess


def resize(path):
    """
    :param path: the path of the video file
    :return:
    calls ffmpeg to re-sclae the video to 3 different formats
    """
    if os.path.exists("v1.mp4") and os.path.exists("v2.mp4") and os.path.exists("v3.mp4"):
        os.remove("v1.mp4")
        os.remove("v2.mp4")
        os.remove("v3.mp4")

    subprocess.call("ffmpeg -i bbb.mp4 -filter:v scale=1280:720 -c:a copy v1.mp4")
    subprocess.call("ffmpeg -i bbb.mp4 -filter:v scale=768:480 -c:a copy v2.mp4")
    subprocess.call("ffmpeg -i bbb.mp4 -filter:v scale=320:240 -c:a copy v3.mp4")


class Streaming:

    def __init__(self, vid):
        self.vid = vid

    def hls_transport(self):
        #resize(self.vid)
        out = self.vid.replace(".mp4", "")
        subprocess.call(f"ffmpeg -i {self.vid} -c:v h264 -flags +cgop -g 30 -hls_time 6 {out}.m3u8")



if __name__ == '__main__':
    video = 'bbb.mp4'
    stream = Streaming(video)
    stream.hls_transport()
