from nicegui import ui, app
from MovementRegion import MovementRegion
from SVG_Arrow_Icons import Directions
from nicegui.events import KeyEventArguments
from ComPort import ComPort
from Utils import load_settings
from ComReader import ComReader
from Logging import Log
from DataProcessor import DataProcessor


BG_IMG_PATH = "Resources/ExampleIMG.png"

# COLOURS
# stone-900 (header row)
# #818cf8 = indigo-500 (Highlight color)

# REQ
# TODO: Title Bar
#   - Colour change (upon alert raising)
# TODO: generate notifications upon data reception
# TODO: generate movement commands upon long hover
# TODO: 
# TODO:

class MainApp:
    """ Class for running main application """
    def __init__(self) -> None:
        # remove defualt page padding
        ui.query('.nicegui-content').classes('p-0 m-0 gap-0')
        # object for processing received serial data
        self.dataProcessor = DataProcessor()

        # initialise comPort object
        settings = load_settings()
        self.comPort = ComPort(
            portNum=settings["ComPort"],
            baudrate=settings["Baudrate"],
            timeout=settings["ReadTimeoutSec"]
        )
        MovementRegion.comPort = self.comPort
        self.comReader = ComReader(self.comPort)
        # add periodic ...
        ui.timer(1.0, self.serviceRxData)

        # add key bindings
        self.keyboard = ui.keyboard(on_key=self.handle_key)

        
        # page header
        with ui.row().classes("w-full relative"):
            self.add_header()

        # page body
        with ui.element('div').classes("w-full h-[95vh] bg-stone-800 relative"):
            self.add_background_img()
            self.add_grid()

    # ========================================================================================
    #   Header
    # ========================================================================================
    def add_header(self):
        # header spacing allocation
        basis_title = 30
        basis_button = 40
        basis_menu = 30
        # add header elements
        with ui.header().classes('flex flex-row py-1 px-4 no-wrap h-[5vh] bg-stone-900 items-center'):
            # Header title text & icon
            with ui.row().classes(f"basis-[{basis_title}%] items-center"):
                ui.icon("visibility", color="#818cf8"). \
                    classes(f"text-5xl")
                ui.html('Wheelchair <a class="text-bold text-[#818cf8]">HMI</a>'). \
                    classes(f"text-lg text-left")
            # status labels for voice commands - enable/disable
            with ui.row().classes(f"basis-[{basis_button}%] flex-row justify-center text-lg"):
                self.style_indLabel_active = "text-center text-teal-200"
                self.style_indLabel_deactive = "text-center text-stone-500"

                ui.label("Voice Commands: ") \
                    .classes("text-center text-bold text-[#818cf8]")
                ui.label("Keyboard Press -") \
                    .classes("text-center")
                self.indLabelEnable = ui.label("E (Enable)") \
                    .classes(self.style_indLabel_active)
                self.indLabelDisable = ui.label("D (Disable)") \
                    .classes(self.style_indLabel_deactive)
            # drop down menu    
            with ui.row().classes(f"basis-[{basis_menu}%] items-center"):
                ui.label("Menu").classes(f"text-lg text-right pr-[5px] ml-auto")
                self.create_menu()

    def create_menu(self):
        with ui.button(icon='menu', color="indigo-500"):
            with ui.menu() as menu:
                ui.menu_item(
                    'Emergency Stop', 
                    lambda: ui.notify("Emergency Stop Activated", type='negative', position='center'), 
                    auto_close=False
                )
                ui.menu_item(
                    'Auto Break', 
                    lambda: ui.notify("Auto Break Activated", type='warning', position='center'), 
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
            # test image
            cameraFeed = ui.interactive_image(BG_IMG_PATH).classes("absolute-center max-w-[1920px]")

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
            print("! Shutting Down Application !")
            app.shutdown()


    def eyeTrackingEnable(self):
        print("Eye tracking movement command generation has been ENABLED.")
        self.indLabelEnable.classes(replace=self.style_indLabel_active)
        self.indLabelDisable.classes(replace=self.style_indLabel_deactive)
    
    def eyeTrackingDisable(self):
        print("Eye tracking movement command generation has been DISABLED.")
        self.indLabelEnable.classes(replace=self.style_indLabel_deactive)
        self.indLabelDisable.classes(replace=self.style_indLabel_active)

    # ========================================================================================
    #   Manage Data Received
    # ========================================================================================
    def serviceRxData(self):
        while True:
            charCode = self.comReader.popNextMessage()
            if charCode == None:
                return  # no data to process
            
            
            


    # ========================================================================================
    #   Testing Ground
    # ========================================================================================
    def testButton(self):
        print(self.comReader._rxDataQueue)



# =====================================

def main():
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

main()