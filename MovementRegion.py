from nicegui import ui
from SVG_Arrow_Icons import SvgElement, Directions

class MovementRegion():
    # class attributes
    bg_hover        = "violet-400"
    opacity_hover   = 30
    bg_hover2_to    = "green-400"
    bg_hover2_from  = "blue-500"

    def __init__(self, arrowDirection: Directions, basis: int) -> None:
        # formatting config
        html_format     = "absolute-center"
        margin          = 0.5
        bg_normal       = "zinc-600"
        opacity         = 25

        self.name = arrowDirection
        self.timerStart = False
        self.cursorExit = True

        # format background based on arrow direction
        directionGradients = {
            Directions.DOWN: "bg-gradient-to-b",
            Directions.UP:  "bg-gradient-to-t",
            Directions.LEFT: "bg-gradient-to-l",
            Directions.RIGHT: "bg-gradient-to-r",
            Directions.STOP: f"bg-gradient-to-t to-{bg_normal}/[.{opacity}] hover:to-{self.bg_hover}/[.{self.opacity_hover}]"
        }
        
        # background element
        self.bgRow = ui.row() \
            .classes(f"basis-[{basis}%] {directionGradients[arrowDirection]} \
                     from-{bg_normal}/[.{opacity}] m-{margin} relative \
                     hover:from-{self.bg_hover}/[.{self.opacity_hover}]")
        self.bgRow.on("mouseenter", self.startHoverTimer)
        self.bgRow.on("mouseleave", self.setExitFlag)

        # arrow element
        with self.bgRow:
            self.htmlElement = ui.html(SvgElement.get_svgElement(arrowDirection)) \
                .classes(html_format)
    
    def startHoverTimer(self):
        print(f"Mouse entered: {self.name}")    # DEBUG 
        self.cursorExit = False
        if self.timerStart:
            return
        
        ui.timer(1, self.timerEvent, once=True)
        self.timerStart = True

    def timerEvent(self):
        print("Timer activated")    # DEBUG 
        self.timerStart = False


    def setExitFlag(self):
        self.cursorExit = True
        print(f"Mouse left: {self.name}")   # DEBUG 