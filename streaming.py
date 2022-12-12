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


def fragment(path):
    out = path.replace(".mp4", "")
    if os.path.exists(f"{out}-fragmented.mp4"):
        os.remove(f"{out}-fragmented.mp4")
    subprocess.call(f"mp4fragment {path} {out}-fragmented.mp4")
    # Creates a new video file with the fragmented mp4


class Streaming:

    def __init__(self, vid):
        self.vid = vid

    def hls_transport(self):
        # resize(self.vid)
        out = self.vid.replace(".mp4", "")
        #subprocess.call(f"ffmpeg -i {self.vid} -c:v h264 -flags +cgop -g 30 -hls_time 6 {out}.m3u8")
        subprocess.call(f'ffmpeg -i {self.vid} -filter_complex "[0:v]split=3[v1][v2][v3]; [v1]copy[v1out]; '
                        f'[v2]scale=w=1280:h=720[v2out]; [v3]scale=w=640:h=360[v3out]" -map [v1out] -c:v:0 '
                        f'libx264 -x264-params "nal-hrd=cbr:force-cfr=1" -b:v:0 5M -maxrate:v:0 5M -minrate:v:0 5M '
                        f'-bufsize:v:0 10M -preset slow -g 48 -sc_threshold 0 -keyint_min 48  -map [v2out] -c:v:1 '
                        f'libx264 -x264-params "nal-hrd=cbr:force-cfr=1" -b:v:1 3M -maxrate:v:1 3M -minrate:v:1 3M '
                        f'-bufsize:v:1 3M -preset slow -g 48 -sc_threshold 0 -keyint_min 48  -map [v3out] -c:v:2 '
                        f'libx264 -x264-params "nal-hrd=cbr:force-cfr=1" -b:v:2 1M -maxrate:v:2 1M -minrate:v:2 1M '
                        f'-bufsize:v:2 1M -preset slow -g 48 -sc_threshold 0 -keyint_min 48  -map a:0 -c:a:0 aac '
                        f'-b:a:0 96k -ac 2  -map a:0 -c:a:1 aac -b:a:1 96k -ac 2  -map a:0 -c:a:2 aac -b:a:2 48k '
                        f'-ac 2  -f hls  -hls_time 6  -hls_playlist_type vod  -hls_flags independent_segments  '
                        f'-hls_segment_type mpegts  -hls_segment_filename stream_%v/data%02d.ts  -master_pl_name '
                        f'master_{out}.m3u8  -var_stream_map "v:0,a:0 v:1,a:1 v:2,a:2" stream_{out}_%v.m3u8')

        """
        Code copied from the internet:
        Above we are converting using variables the bbb video to 1080 (copy), 720 and 360, then we trasncode them into
        different bitrates, and finnally we create a hls playlist, containing the master file, and other 3 for the different
        scales, and its corresponding segments of 6 seconds
        """

    def mpd(self):
        # First we need to fragment the video
        fragment(self.vid)
        ipt = self.vid.replace(".mp4", "")
        ipt += "-fragmented.mp4"
        print(ipt)
        subprocess.call(f"mp4dash --marlin --encryption-key=121a0fca0f1b475b8910297fa8e0a07e:a0a1a2a3a4a5a6a7a8a9aaabacadaeaf {ipt}", shell=True)


if __name__ == '__main__':
    video = 'bbb.mp4'
    stream = Streaming(video)
    stream.hls_transport()
    #stream.mpd()
