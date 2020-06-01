#!/usr/bin/env python

import preview
from imutils.video import VideoStream
import time

print("[INFO] CAMERA STARTUP")

videoStr = VideoStream(usePiCamera= False).start()
time.sleep(2.0)

app = preview.ImagePreview(videoStr)
app.root.mainloop()
