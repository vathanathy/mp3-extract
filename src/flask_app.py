
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, send_file
from processing import dl
from pytube import YouTube
import os
import glob
from flask_httpauth import HTTPBasicAuth
from dotenv import load_dotenv


#Load env variables
load_dotenv()

app = Flask(__name__)
app.config["DEBUG"] = True

auth = HTTPBasicAuth()

@auth.verify_password
def verify(username, password):
    print(os.environ.get("usr"))
    print(os.environ.get("pw"))
    if username == os.environ.get("usr") and password == os.environ.get("pw"):
        return True
    else:
        return False

@app.route("/", methods=["GET", "POST"])
@auth.login_required
def dl_page():
    if request.method == "POST":
        files = glob.glob("./mysite/files/*")
        for f in files:
            os.remove(f)
        link = str(request.form["link"])
        if link is not None :
            yt = YouTube(link)

            video = yt.streams.filter(only_audio=True).first()

            out_file = video.download(output_path="./mysite/files")
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)

            return send_file(new_file, as_attachment=True)
    return '''
        <html>
                <body>
                    <form method="post" action=".">
                        <p><input name="link" /></p>
                        <p><input type="submit" value="inject" /></p>
                    </form>
                </body>
        </html>
    '''

