from nicegui import ui, app
from MovementRegion import MovementRegion
from SVG_Arrow_Icons import Directions

BG_IMG_PATH = "Resources/ExampleIMG.png"

# REQ
# TODO: Title Bar
#   - status info text (alerts or lack of alerts (healthy)) 
#       - Speech: E = enable, D = Disable (green / red coloured text depending on state)
#   - Colour change (upon alert raising)
# TODO: generate notifications upon data reception
# TODO: generate movement commands upon long hover
# TODO: 
# TODO:


class MainApp:
    """ Class for running main application """
    def __init__(self) -> None:
        ui.query('.nicegui-content').classes('p-0 m-0 gap-0') # remove defualt page padding
        
        # page header
        with ui.row().classes("w-full relative"):
            self.add_header()

        # page body
        with ui.element('div').classes("w-full h-[95vh] bg-slate-900 relative"):
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
            # temp buttons for testing
            with ui.row().classes(f"basis-[{basis_button}%] flex"):
                ui.button("Emergency Stop", color="blue-grey-9") \
                    .on('click', lambda: ui.notify("Emergency Stop Activated", type='negative', position='center')) \
                    .classes(f"text-center flex-auto")
                    # .classes(f"basis-[{basis_button}%] text-center")
                ui.button("Auto Break", color="blue-grey-9") \
                    .on('click', lambda: ui.notify("Auto Break Activated", type='warning', position='center')) \
                    .classes(f"text-center flex-auto")
                    # .classes(f"basis-[{basis_button}%] text-center")
                ui.button("Test", color="blue-grey-9") \
                    .on('click', self.testButton) \
                    .classes(f"text-center flex-auto")
            # place holder text
            with ui.row().classes(f"basis-[{basis_menu}%] items-center"):
                textLabel = ui.label("Menu").classes(f"text-lg text-right pr-[5px] ml-auto")
                self.create_menu(textLabel)

    def create_menu(self, menu_text: ui.label):
        with ui.button(icon='menu', color="indigo-500"):
            with ui.menu() as menu:
                ui.menu_item('Terminate Application', lambda: app.shutdown())
                ui.menu_item('Menu item 2 (keep open)', lambda: menu_text.set_text('Selected item 3'), auto_close=False)
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
    #   Testing Ground
    # ========================================================================================
    def testButton(self):
        print("Test button")


# =====================================

def main():
    mainApp = MainApp()
    ui.run(
        title="HFWCS HMI-v0.0.2", 
        host='127.0.0.1',
        port=10_000,
        dark=None,
        favicon='♿',
        show=False,
        reload=False
    )

main()