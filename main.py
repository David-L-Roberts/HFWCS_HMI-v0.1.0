from WebcamFeed import VideoSelector
from nicegui import ui, app
from MovementRegion import MovementRegion
from SVG_Arrow_Icons import Directions
from nicegui.events import KeyEventArguments
from ComPort import ComPort
from Utils import SETTINGS
from ComReader import ComReader
from DataProcessor import DataProcessor
from Logging import Log
from MessageLib import txMessageCodes
import time

C_HEADER_DEFAULT = "bg-[#010409]"

# TODO: Distance sensor reading display

class MainApp:
    """ Class for running main application """
    def __init__(self) -> None:
        # remove defualt page padding
        ui.query('.nicegui-content').classes('p-0 m-0 gap-0')

        # initialise comPort object
        self.comPort = ComPort(
            portNum=SETTINGS["ComPort"],
            baudrate=SETTINGS["Baudrate"],
            timeout=SETTINGS["ReadTimeoutSec"]
        )
        MovementRegion.comPort = self.comPort
        # Handle data received from serial 
        self.comReader = ComReader(self.comPort)
        ui.timer(1.0, self.serviceRxData)

        # page header
        with ui.row().classes("w-full relative"):
            self.add_header()
        # page body
        with ui.element('div').classes("w-full h-[95vh] bg-[#0d1117] relative overflow-hidden"):
            self.add_background_img()
            self.add_grid()

        # object for processing received serial data
        self.dataProcessor = DataProcessor(self.headerRow)
        # add key bindings
        self.keyboard = ui.keyboard(on_key=self.handle_key)

        self.startup_transaction()

    def startup_transaction(self):
        self.comPort.writeSerial(txMessageCodes["Hello"])
        Log.log("Attempting to establish connection to Arduino.")
        while True:
            time.sleep(0.5)
            self.serviceRxData()
            if self.dataProcessor.checkACK():
                Log.log("Arduino connected successfully.")
                return 
            


    # ========================================================================================
    #   Header
    # ========================================================================================
    def add_header(self):
        # header spacing allocation
        basis_title = 30
        basis_button = 40
        basis_menu = 30
        # add header elements
        self.headerRow = ui.header().classes(f'flex flex-row py-1 px-4 no-wrap h-[5vh] {C_HEADER_DEFAULT} items-center')
        with self.headerRow:
            # Header title text & icon
            with ui.row().classes(f"basis-[{basis_title}%] items-center"):
                ui.icon("visibility", color="#818cf8"). \
                    classes(f"text-5xl")
                ui.html('Wheelchair <a class="text-bold text-[#818cf8]">HMI</a>'). \
                    classes(f"text-lg text-left")
            # status labels for voice commands - enable/disable
            with ui.row().classes(f"basis-[{basis_button}%] flex-row justify-center text-lg"):
                self.style_indLabel_activeE = "text-center text-teal-200"
                self.style_indLabel_activeD = "text-center text-rose-300"
                self.style_indLabel_deactive = "text-center text-stone-500"

                ui.label("Voice Commands: ") \
                    .classes("text-center text-bold text-[#818cf8]")
                ui.label("Keyboard Press -") \
                    .classes("text-center")
                self.indLabelEnable = ui.label("E (Enabled)") \
                    .classes(self.style_indLabel_activeE)
                self.indLabelDisable = ui.label("D (Disabled)") \
                    .classes(self.style_indLabel_deactive)
            # drop down menu    
            with ui.row().classes(f"basis-[{basis_menu}%] items-center"):
                ui.label("Menu").classes(f"text-lg text-right pr-[5px] ml-auto")
                self.create_menu()

    def create_menu(self):
        with ui.button(icon='menu', color="indigo-500"):
            with ui.menu() as menu:
                ui.menu_item(
                    'Emergency Stop Enable', 
                    lambda: self.dataProcessor.processCharCode('FA'), 
                    auto_close=False
                )
                ui.menu_item(
                    'Emergency Stop Disable', 
                    lambda: self.dataProcessor.processCharCode('FE'), 
                    auto_close=False
                )
                ui.menu_item(
                    'Auto Break Enable', 
                    lambda: self.dataProcessor.processCharCode('FB'), 
                    auto_close=False
                )
                ui.menu_item(
                    'Auto Break Disable', 
                    lambda: self.dataProcessor.processCharCode('FC'), 
                    auto_close=False
                )
                ui.menu_item(
                    'Test', 
                    self.testButton, 
                    auto_close=False
                )
                ui.separator()
                ui.menu_item('Terminate Application (K)', lambda: app.shutdown())
                ui.separator()
                ui.menu_item('Close', on_click=menu.close)

    # ========================================================================================
    #   BACKGROUND IMAGE
    # ========================================================================================
    def add_background_img(self):
        with ui.element('div').classes('w-full h-[95vh] absolute'):
            # Place image for camerafeed in background of UI
            # self.cameraFeed = ui.interactive_image().classes("absolute-center max-w-[1500px]")
            self.cameraFeed = ui.interactive_image().classes("absolute-center max-w-[1920px]")
        # setup for switching between different video feeds
        VideoSelector.setVideoImageElement(self.cameraFeed)
        # A timer constantly updates the source of the image.
        # Because data from same paths are cached by the browser, we must force an update by 
        # adding the current timestamp to the source.
        ui.timer(interval=SETTINGS["CameraRefreshT"], callback=VideoSelector.callback)

    # ========================================================================================
    #   DIRECTION GRID
    # ========================================================================================
    def add_grid(self):
        with ui.element('div').classes('flex flex-row text-lg flex-nowrap w-full h-full absolute'):
            self.create_cols()

    def create_cols(self):
        flex_col_format = 'flex flex-col flex-nowrap basis-%s relative'

        # col 1
        with ui.element('div').classes(flex_col_format %"[20%]"):
            MovementRegion(Directions.LEFT, 100)

        # col 2
        with ui.element('div').classes(flex_col_format %"[60%]"):
            MovementRegion(Directions.UP, 35)
            MovementRegion(Directions.STOP, 30)
            MovementRegion(Directions.DOWN, 35)

        # col 3
        with ui.element('div').classes(flex_col_format %"[20%]"):
            MovementRegion(Directions.RIGHT, 100)

    # ========================================================================================
    #   Key Bindings
    # ========================================================================================
    def handle_key(self, e: KeyEventArguments):
        if (not e.action.keydown) or (e.action.repeat):
            return
        if (e.key == 'e'):
            print("Key Pressed: E")
            self.eyeTrackingEnable()
        elif (e.key == 'd'):
            print("Key Pressed: D")
            self.eyeTrackingDisable()
        elif (e.key == 'k'):
            print("Key Pressed: K")
            Log.log("Shutting Down Application.")
            app.shutdown()
        elif (e.key == 'c'):
            print("Key Pressed: C") # switch to active webcam feed
            VideoSelector.setSource(0)
        elif (e.key == 'b'):
            print("Key Pressed: B") # switch to blancked-out webcam feed
            VideoSelector.setSource(1)


    def eyeTrackingEnable(self):
        Log.log("Movement command generation has been ENABLED.")
        self.indLabelEnable.classes(replace=self.style_indLabel_activeE)
        self.indLabelDisable.classes(replace=self.style_indLabel_deactive)
        MovementRegion.dataTxEnable()
    
    def eyeTrackingDisable(self):
        Log.log("Movement command generation has been DISABLED.")
        self.indLabelEnable.classes(replace=self.style_indLabel_deactive)
        self.indLabelDisable.classes(replace=self.style_indLabel_activeD)
        MovementRegion.dataTxDisable()

    # ========================================================================================
    #   Manage Data Received
    # ========================================================================================
    def serviceRxData(self):
        while True:
            charCode = self.comReader.popNextMessage()
            if charCode == None:
                return  # no data to process
            self.dataProcessor.processCharCode(charCode)

    # ========================================================================================
    #   Testing Ground
    # ========================================================================================
    def testButton(self):
        print(self.comReader._rxDataQueue)


# =====================================

def main():
    print("="*30)
    Log.log("Application Start")
    print("="*30)

    mainApp = MainApp()
    ui.run(
        title="HFWCS HMI-v0.1.0", 
        host='127.0.0.1',
        port=10_000,
        dark=None,
        favicon='♿',
        show=False,
        reload=False
    )

if __name__ == "__main__":
    main()

