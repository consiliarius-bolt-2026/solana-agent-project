#!/usr/bin/env python3
import os
import sys
import subprocess
import re
import yt_dlp

def extract_audio(video_input, output_audio_path):
    # 確保輸出路徑有 .wav 副檔名
    if not output_audio_path.lower().endswith('.wav'):
        output_audio_path += '.wav'
        
    output_dir = os.path.dirname(output_audio_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    is_url = re.match(r"https?://", video_input)
    video_to_process = ""

    try:
        if is_url:
            temp_video_path = "/workspace/temp_video_for_audio_extraction"
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f"{temp_video_path}.%(ext)s",
                'quiet': True,
                'no_warnings': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_input, download=True)
                video_to_process = ydl.prepare_filename(info_dict)
        else:
            video_to_process = video_input
            if not os.path.exists(video_to_process):
                print(f"❌ 錯誤：本地影片檔案不存在：{video_to_process}", file=sys.stderr)
                return False

        ffmpeg_command = [
            "/usr/bin/ffmpeg",
            "-i", video_to_process,
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            output_audio_path,
            "-y"
        ]
        
        result = subprocess.run(ffmpeg_command, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ ffmpeg 錯誤 (code {result.returncode}):\n{result.stderr}", file=sys.stderr)
            return False

        if is_url and os.path.exists(video_to_process):
            os.remove(video_to_process)

        return True
    except Exception as e:
        print(f"❌ 提取失敗：{e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: video_audio_extractor <影片路徑或URL> <輸出檔名>", file=sys.stderr)
        sys.exit(1)
    
    video_in = sys.argv[1]
    audio_out = sys.argv[2]
    
    if extract_audio(video_in, audio_out):
        print(f"✅ 音軌成功提取至：{audio_out}.wav" if not audio_out.endswith('.wav') else f"✅ 音軌成功提取至：{audio_out}")
    else:
        sys.exit(1)