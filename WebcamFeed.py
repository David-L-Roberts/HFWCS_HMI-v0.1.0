#!/usr/bin/env python3
import asyncio
import base64
import concurrent.futures
import signal
import time

import cv2
import numpy as np
from fastapi import Response

import nicegui.globals
from nicegui import app, ui
from Utils import SETTINGS


# In case webcam unavailable, this will provide a black placeholder image.
black_1px = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAA1JREFUGFdjYGBg+A8AAQQBAHAgZQsAAAAASUVORK5CYII='
placeholder = Response(content=base64.b64decode(black_1px.encode('ascii')), media_type='image/png')

# Need an executor to schedule CPU-intensive tasks. To be used with `loop.run_in_executor()`.
process_pool_executor = concurrent.futures.ProcessPoolExecutor()

# ===================================================================================================
def convert(frame: np.ndarray) -> bytes:
    """Convert frame to jpg format."""
    _, imencode_image = cv2.imencode('.jpg', frame)
    return imencode_image.tobytes()

@app.get('/video/frame0')
async def grab_video_frame0() -> Response:
    """Create a web route which always provides the latest image from OpenCV.
    Utilises FastAPI's `app.get`."""
    if not video_capture[0].isOpened():
        return placeholder
    loop = asyncio.get_running_loop()
    # `video_capture.read` call is a blocking function.
    # need to run it in a separate thread (default executor) to avoid blocking the event loop.
    _, frame = await loop.run_in_executor(None, video_capture[0].read)
    if frame is None:
        return placeholder
    # `convert` is a CPU-intensive function, so we run it in a separate process to avoid blocking the event loop and GIL.
    jpeg = await loop.run_in_executor(process_pool_executor, convert, frame)
    return Response(content=jpeg, media_type='image/jpeg')

@app.get('/video/frame1')
async def grab_video_frame1() -> Response:
    """Create a web route which always provides the latest image from OpenCV.
    Utilises FastAPI's `app.get`."""
    if not video_capture[1].isOpened():
        return placeholder
    loop = asyncio.get_running_loop()
    # `video_capture.read` call is a blocking function.
    # need to run it in a separate thread (default executor) to avoid blocking the event loop.
    _, frame = await loop.run_in_executor(None, video_capture[1].read)
    if frame is None:
        return placeholder
    # `convert` is a CPU-intensive function, so we run it in a separate process to avoid blocking the event loop and GIL.
    jpeg = await loop.run_in_executor(process_pool_executor, convert, frame)
    return Response(content=jpeg, media_type='image/jpeg')

@app.get('/video/frame2')
async def grab_video_frame2() -> Response:
    """Create a web route which always provides a blank image"""
    return placeholder

async def disconnect() -> None:
    """Disconnect all clients from current running server."""
    for client in nicegui.globals.clients.keys():
        await app.sio.disconnect(client)

def handle_sigint(signum, frame) -> None:
    """Disconnect client upon Ctrl+C (signal interrupt)."""
    # `disconnect` is async, so it must be called from the event loop; we use `ui.timer` to do so.
    ui.timer(0.1, disconnect, once=True)
    # Delay the default handler to allow the disconnect to complete.
    ui.timer(1, lambda: signal.default_int_handler(signum, frame), once=True)

async def cleanup() -> None:
    # This prevents ugly stack traces when auto-reloading on code change,
    # otherwise disconnected clients try to reconnect to the newly started server.
    await disconnect()
    # Release the webcam hardware so it can be used by other applications again.
    for video_obj in video_capture:
        video_obj.release()
    # The process pool executor must be shutdown when the app is closed, otherwise the process will not exit.
    process_pool_executor.shutdown()

# ===================================================================================================
# Use OpenCV to access the webcam.
blankCam = cv2.VideoCapture(SETTINGS["CameraBlank"])
if SETTINGS["DisableCameraFeed"]:
    video_capture = [blankCam, blankCam, blankCam]
else:
    video_capture = [cv2.VideoCapture(SETTINGS["CameraFront"]), cv2.VideoCapture(SETTINGS["CameraBack"]), blankCam]

# release and clean up resources on shutdown
app.on_shutdown(cleanup)
# Need to disconnect clients when the app is stopped with Ctrl+C; 
# otherwise they will keep requesting images which lead to unfinished subprocesses blocking the shutdown.
signal.signal(signal.SIGINT, handle_sigint)

# ===================================================================================================
class VideoSelector:
    """Class for selecting one of the open camera feeds in `video_capture`."""
    video_src = 0   #'/video/frame' endpoint number
    vid_img: ui.interactive_image = None
    process_executor = process_pool_executor

    @classmethod
    def setVideoImageElement(cls, image_element: ui.interactive_image):
        cls.vid_img = image_element

    @classmethod
    def callback(cls):
        cls.vid_img.set_source(f'/video/frame{cls.video_src}?{time.time()}')

    @classmethod
    def setSource(cls, cam_num: int):
        cls.video_src = cam_num