from nicegui import app, ui
from WebcamFeed import VideoSelector
from nicegui.events import KeyEventArguments

# refresh period of webcam feed, in seconds
FRAME_REFRESH_T = 0.2




class MainApp:
    def __init__(self) -> None:
        with ui.element('div').classes("w-full h-[95vh] bg-slate-900 relative"):
            with ui.element('div').classes('w-full h-[95vh] absolute'):
                video_image = ui.interactive_image().classes('w-full h-full absolute-center')
                video_image.style("max-width: 1500px")

        # A timer constantly updates the source of the image.
        # Because data from same paths are cached by the browser,
        # we must force an update by adding the current timestamp to the source.
        VideoSelector.setVideoImageElement(video_image)
        ui.timer(interval=FRAME_REFRESH_T, callback=VideoSelector.callback)

        keyboard = ui.keyboard(on_key=self.handle_key)


    def handle_key(self, e: KeyEventArguments):
        if (not e.action.keydown) or (e.action.repeat):
            return
        if (e.key == 'e'):
            print("Key Pressed: E")
            VideoSelector.setSource(0)
        if (e.key == 'r'):
            print("Key Pressed: R")
            VideoSelector.setSource(1)

def main():
    MainApp()
    # ui.run(port=10_000, dark=True, native=False, reload=False, window_size=(1920, 1080))
    ui.run(port=10_000, host='localhost', dark=True, reload=False)

main()

