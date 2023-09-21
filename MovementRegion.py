from nicegui import ui
from SVG_Arrow_Icons import SvgElement, Directions

DELAY_TIME = 0.75   # seconds

class MovementRegion():
    # class attributes
    bg_hover        = "violet-400"
    opacity_hover   = 30
    bg_hover2_to    = "green-400"
    bg_hover2_from  = "blue-500"
    hoverStyle_default  = f"hover:from-{bg_hover}/[.{opacity_hover}]"
    hoverStyle_active   = f"hover:to-{bg_hover2_to}/[.{opacity_hover}] hover:from-{bg_hover2_from}/[.{opacity_hover}]"

    def __init__(self, arrowDirection: Directions, basis: int) -> None:
        # formatting config
        html_format     = "absolute-center"
        margin          = 0.5
        bg_normal       = "zinc-600"
        opacity         = 25

        self.name = arrowDirection
        self.timerStart: bool = False # activation timer has begun counting down
        self.cursorExit: bool = True  # The cursor has exited the screen region
        self.regionActive: bool = False  # The region is considered active

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
        self.cursorExit = False

        if self.timerStart:
            return
        
        ui.timer(DELAY_TIME, self.timerEvent, once=True)
        self.timerStart = True

    def timerEvent(self):
        self.timerStart = False     # reset timer flag
        # check if cursor is still within region
        if self.cursorExit:
            return
        # activate the region
        self.regionActive = True
        self.reStyleRegion()        # restyle the region as active

    def setExitFlag(self):
        self.cursorExit = True
        if self.regionActive:
            self.regionActive = False
            self.reStyleRegion()

    def reStyleRegion(self):
        # change styling of movement region 
        if self.regionActive:   # active region styling
            self.bgRow.classes(
                remove=self.hoverStyle_default,
                add=self.hoverStyle_active
            )
        else:                   # defautl region styling
            self.bgRow.classes(
                remove=self.hoverStyle_active,
                add=self.hoverStyle_default
            )