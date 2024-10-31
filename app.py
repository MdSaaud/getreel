from flask import Flask, request, send_file, render_template
import platform
from pathlib import Path
import instaloader
import os


def get_downloads_folder():
    system = platform.system()

    if system == "Windows":
        return Path.home() / "Downloads"
    elif system == "Linux":  # Assuming Android is running a Linux-based OS
        # Standard Android Downloads path
        android_download_path = Path("/storage/emulated/0/Download")
        if android_download_path.exists():
            return android_download_path
        else:
            return None  # Handle this case as needed
    else:
        return None


downloads_folder = get_downloads_folder()



app = Flask(__name__)

DOWNLOAD_DIR = f"{downloads_folder}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        link = request.form['link']
        loader = instaloader.Instaloader()
        loader.download_video_thumbnails = False
        loader.save_metadata = False
        loader.download_comments = False
        shortcode = link.split('/')[-2]
        loader.dirname_pattern = DOWNLOAD_DIR
        loader.download_post(instaloader.Post.from_shortcode(loader.context, shortcode), target="")
        print("Download successful!")
        return "Download successful!"
    except Exception as e:
        print("An error occurred:", e)
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)


