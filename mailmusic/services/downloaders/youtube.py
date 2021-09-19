# Calls Music 1 - Telegram bot for streaming audio in group calls
# Copyright (C) 2021  Roj Serbest

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Modified by Inukaasith

from os import path
from youtube_dl import YoutubeDL

from mailmusic.config import DURATION_LIMIT
from mailmusic.helpers.errors import DurationLimitError


ydl_opts = {
    "format": "bestaudio/best[ext=m4a]",
    "geo-bypass": True,
    "geo-bypass-counyry ID": True,
    "--external-downloader aria2c": True,
    "--external-downloader-args '-x 16 -s 16 -k 1M -q'": True,
    "--no-check-certificate": True,
    "--no-playlist": True,
    "--no-mtime": True,
    "--no-cache-dir": True,
    "--force-ipv4": True,
    "--no-warnings": True,
    "--abort-on-error": True,
    "--no-progress": True,
    "verbose": True,
    "addmetadata": True,
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}

ydl = YoutubeDL(ydl_opts)

def download(url: str) -> str:
    global ydl
    info = ydl.extract_info(url, False)
    duration = round(info["duration"] / 60)

    if duration > DURATION_LIMIT:
        raise DurationLimitError(
            f"Videos longer than {DURATION_LIMIT} minute(s) aren't allowed, the provided video is {duration} minute(s)"
        )
    try:
        ydl.download([url])
    except:
        raise DurationLimitError(
            f"Videos longer than {DURATION_LIMIT} minute(s) aren't allowed, the provided video is {duration} minute(s)"
        )
    return path.join("downloads", f"{info['id']}.{info['ext']}")
