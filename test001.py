import nicegui as ng
from nicegui import ui

IMG_PATH = "D:/1. My Folders/Programming/Python/100_Uni_Projects/01_HFWCS_HMI/HFWCS_HMI-v0.0.1/Resources/Example_IMG.png"

class MainApp:
    """
    """
    def __init__(self) -> None:
        # labelFoward = ui.label("Forward")
        # labelLeft = ui.label("Turn Left")
        # labelRight = ui.label("Turn Right")
        # with ui.column().classes('h-screen p-8 no-wrap'):
            # exampleImage = ui.interactive_image(IMG_PATH, cross=True).style("max-width: 1500px")
            # exampleImage = ui.interactive_image(IMG_PATH, cross=True)
        #     exampleImage = ui.image(IMG_PATH)
        # with ui.column():
        #     ui.label("hello")
            # exampleImage.classes("absolute inset-0")

            # # TODO: place grid object inside image, then place text in grid positions
            # with exampleImage:
            #     with ui.column():
            #         labelLeft = ui.label("Turn Left").classes("bg-transparent absolute-left text-h3 vertical-middle")
            #     with ui.column():
            #         labelFoward = ui.label("Forward").classes('bg-transparent absolute-top text-h3 text-center')
            #         labelCenter = ui.html('<strong>Center</strong>.').classes('bg-transparent absolute-center text-h1 text-center')
            #         labelBack = ui.label("Backward").classes("bg-transparent absolute-bottom text-h3 text-center")
            #     labelRight = ui.label("Turn Right").classes("bg-transparent absolute-right text-h3 vertical-middle")

            # with exampleImage:
            #     with ui.row().classes("inline-block"):
            #         with ui.column():
            #             labelLeft = ui.label("Turn Left")
            #         with ui.column():
            #             labelFoward = ui.label("Forward")
            #             labelCenter = ui.html('<strong>Center</strong>.')
            #             labelBack = ui.label("Backward")
            #         with ui.column():
            #             labelRight = ui.label("Turn Right")

        height = 200
        tailwind = f'h-[{height}px] bg-emerald-500 break-inside-avoid'

        

        with ui.element('div').classes('columns-2 w-full gap-2'):
            card_bg = ui.card().classes(tailwind)
            with card_bg:
                with ui.grid(columns=3).classes("text-slate-950 w-full h-full text-center absolute inset-0"):
                    ui.label("")
                    ui.label("1,2")
                    ui.label("")

                    ui.label("2, 1")
                    ui.label("2, 2")
                    ui.label("2, 3")

                    ui.label("")
                    ui.label("3, 2")
                    ui.label("")

            exampleImage = ui.interactive_image(IMG_PATH).classes("w-full aspect-video")
            with exampleImage:
                with ui.column():
                    ui.label("Text In Image")
                    ui.label("Text In Image")
        
        with ui.element("div").classes("bg-violet-800 w-full h-48"):
            ui.label("hello")
# =====================================

def main():
    mainApp = MainApp()
    ui.run(
        title="HFWCS HMI", 
        host='127.0.0.1',
        port=10_000,
        dark=None,
        favicon='♿'
    )

main()