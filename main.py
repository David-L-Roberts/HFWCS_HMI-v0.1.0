from nicegui import ui, app
from MovementRegion import MovementRegion
from SVG_Arrow_Icons import Directions

BG_IMG_PATH = "Resources/ExampleIMG.png"

# REQ
# TODO: on long hover > change colour
# TODO: replace text with SVG or icons (arrows)
# TODO: Title Bar
#   - status info text (alerts or lack of alerts (healthy)) 
#   - Colour change (upon alert raising)
# TODO: generate notifications
# TODO: generate movement commands upon long hover

# OPT
# TODO: Time in header


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
        basis_button = 20   # x2
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
            ui.button("Emergency Stop", color="blue-grey-9") \
                .on('click', lambda: ui.notify("Emergency Stop Activated", type='negative', position='center')) \
                .classes(f"basis-[{basis_button}%] text-center")
            ui.button(f"Auto Break", color="blue-grey-9") \
                .on('click', lambda: ui.notify("Auto Break Activated", type='warning', position='center')) \
                .classes(f"basis-[{basis_button}%] text-center")
            # place holder text
            with ui.row().classes(f"basis-[{basis_menu}%] items-center"):
                textLabel = ui.label("Menu").classes(f"text-lg text-right pr-[5px] ml-auto")
                self.create_menu(textLabel)

    def create_menu(self, menu_text: ui.label):
        #  with ui.row().classes('w-full '):
        with ui.button(icon='menu'):
            with ui.menu() as menu:
                ui.menu_item('Terminate Application', lambda: app.shutdown())
                ui.menu_item('Menu item 2', lambda: menu_text.set_text('Selected item 2'))
                ui.menu_item('Menu item 3 (keep open)', lambda: menu_text.set_text('Selected item 3'), auto_close=False)
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