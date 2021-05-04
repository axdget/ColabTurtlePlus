from IPython.display import display, HTML
import time
import math
import re

""" 
Original Created at: 23rd October 2018
        by: Tolga Atam
v2.1.0 Updated at: 15th March 2021
         by: Tolga Atam
Module for drawing classic Turtle figures on Google Colab notebooks.
It uses html capabilites of IPython library to draw svg shapes inline.
Looks of the figures are inspired from Blockly Games / Turtle (blockly-games.appspot.com/turtle)

--------
Modified April 2021 by Larry Riddle
Changed some default values to match classic turtle.py package
  default background color is white, default pen color is black, default pen thickness is 1
  default mode is "standard"
  center of window has coordinates (0,0)
Added option for selecting a mode when initializing the turtle graphics
  "standard" : default direction is to the right (east) and positive angles measured counterclockwise
  "logo" : default directon is upward (north) and positive angles are measured clockwise with 0° pointing up.
  "svg": This is a special mode to handle how the original ColabTurtle worked. The coordinate system is the same
         as that used with SVG. The upper left corner is (0,0) with positive x direction being to the right, and the 
         positive y direction being to the bottom. Positive angles are measured clockwise with 0° pointing right.
Added functions to print or save the svg coding for the image.
Added additional shapes from classic turtle.py: 'classic' (the default shape), 'arrow', 'square', 'triangle', 'circle','turtle2', 'blank'
  The circle shape in the original ColabTurtle has been renamed to 'ring'.
  The turtle2 shape is the same as the turtle shape in the classic turtle.py package.
Added speed=0 option that displays final image with no animation. 
  Added done function so that final image is displayed on screen when speed=0.
Added setworldcoordinates function to allow for setting world coordinate system. This sets the mode to "world".
  This should be done immediately after initializing the turtle window.
Added towards function to return the angle between the line from turtle position to specified position.
Implemented begin_fill and end_fill functions from aronma/ColabTurtle_2 github. Added fillcolor function and fillrule function.
  The fillrule function can be used to specify the SVG fill_rule (nonzero or evenodd). The default is evenodd to match turtle.py behavior.
  When calling begin_fill, a value for the fill_rule can be given that will apply only to that fill.
  Because the fill is controlled by svg rules, the result may differ from classic turtle fill.
Implemented circle (arc) function from aronma/ColabTurtle_2 github. Modified these to match behavior of circle function in
  classic turtle.py package. If the radius is positive, the center of the circle is to the left of the turtle and the
  path is drawn in the counterclockwise direction. If the radius is negative, the center of the circle is to the right of
  the turtle and path is drawn in the clockwise direction. Number of steps is not used here since the circle is drawn using
  the svg circle function.
Modified the color function to set both the pencolor as well as the fillcolor, just as in classic turtle.py package.
Added dot function to draw a dot with given diameter and color.
Added shapesize function to scale the turtle shape.
Added stamp, clearstamp, and clearstamps to stamp a copy of the turtle shape onto the canvas at the current turtle position, or to
  delete stamps.
Added pen function.
Added tilt and tiltangle functions.
Original ColabTurtle defaults can be set by calling OldDefaults() after importing the ColabTurtle package but before initializeTurtle.
  This sets default background to black, default pen color to white, default pen width to 4, default shape to Turtle, and
  default window size to 800x500. It also sets the mode to "svg".

"""

DEFAULT_WINDOW_SIZE = (800, 600)
DEFAULT_SPEED = 5
DEFAULT_TURTLE_VISIBILITY = True
DEFAULT_PEN_COLOR = 'black'
DEFAULT_TURTLE_DEGREE = 0
DEFAULT_BACKGROUND_COLOR = 'white'
DEFAULT_FILL_COLOR = 'black'
DEFAULT_BORDER_COLOR = ""
DEFAULT_IS_PEN_DOWN = True
DEFAULT_SVG_LINES_STRING = ""
DEFAULT_PEN_WIDTH = 1
DEFAULT_OUTLINE_WIDTH = 1
DEFAULT_STRETCHFACTOR = (1,1)
DEFAULT_TILT_ANGLE = 0
DEFAULT_FILL_RULE = 'evenodd'
DEFAULT_FILL_OPACITY = 1
# All 140 color names that modern browsers support, plus 'none'. Taken from https://www.w3schools.com/colors/colors_names.asp
VALID_COLORS = ('black', 'navy', 'darkblue', 'mediumblue', 'blue', 'darkgreen', 'green', 'teal', 'darkcyan', 'deepskyblue', 'darkturquoise', 
                'mediumspringgreen', 'lime', 'springgreen', 'aqua', 'cyan', 'midnightblue', 'dodgerblue', 'lightseagreen', 'forestgreen', 'seagreen', 
                'darkslategray', 'darkslategrey', 'limegreen', 'mediumseagreen', 'turquoise', 'royalblue', 'steelblue', 'darkslateblue', 'mediumturquoise', 
                'indigo', 'darkolivegreen', 'cadetblue', 'cornflowerblue', 'rebeccapurple', 'mediumaquamarine', 'dimgray', 'dimgrey', 'slateblue', 'olivedrab', 
                'slategray', 'slategrey', 'lightslategray', 'lightslategrey', 'mediumslateblue', 'lawngreen', 'chartreuse', 'aquamarine', 'maroon', 'purple', 
                'olive', 'gray', 'grey', 'skyblue', 'lightskyblue', 'blueviolet', 'darkred', 'darkmagenta', 'saddlebrown', 'darkseagreen', 'lightgreen', 
                'mediumpurple', 'darkviolet', 'palegreen', 'darkorchid', 'yellowgreen', 'sienna', 'brown', 'darkgray', 'darkgrey', 'lightblue', 'greenyellow', 
                'paleturquoise', 'lightsteelblue', 'powderblue', 'firebrick', 'darkgoldenrod', 'mediumorchid', 'rosybrown', 'darkkhaki', 'silver', 
                'mediumvioletred', 'indianred', 'peru', 'chocolate', 'tan', 'lightgray', 'lightgrey', 'thistle', 'orchid', 'goldenrod', 'palevioletred', 
                'crimson', 'gainsboro', 'plum', 'burlywood', 'lightcyan', 'lavender', 'darksalmon', 'violet', 'palegoldenrod', 'lightcoral', 'khaki', 
                'aliceblue', 'honeydew', 'azure', 'sandybrown', 'wheat', 'beige', 'whitesmoke', 'mintcream', 'ghostwhite', 'salmon', 'antiquewhite', 'linen', 
                'lightgoldenrodyellow', 'oldlace', 'red', 'fuchsia', 'magenta', 'deeppink', 'orangered', 'tomato', 'hotpink', 'coral', 'darkorange', 
                'lightsalmon', 'orange', 'lightpink', 'pink', 'gold', 'peachpuff', 'navajowhite', 'moccasin', 'bisque', 'mistyrose', 'blanchedalmond', 
                'papayawhip', 'lavenderblush', 'seashell', 'cornsilk', 'lemonchiffon', 'floralwhite', 'snow', 'yellow', 'lightyellow', 'ivory', 'white','none','')
#VALID_COLORS_SET = set(VALID_COLORS)
VALID_MODES = ('standard','logo','world','svg')
DEFAULT_TURTLE_SHAPE = 'classic'
VALID_TURTLE_SHAPES = ('turtle', 'ring', 'classic', 'arrow', 'square', 'triangle', 'circle', 'turtle2', 'blank') 
DEFAULT_MODE = 'standard'
SVG_TEMPLATE = """
      <svg width="{window_width}" height="{window_height}">  
        <rect width="100%" height="100%" style="fill:{background_color};stroke:{kolor};stroke-width:1"/>
        {stampsB}
        {lines}
        {dots}
        {stampsT}
        {turtle}
      </svg>
    """
TURTLE_TURTLE_SVG_TEMPLATE = """<g id="turtle" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<path style="stroke:{pen_color};fill-rule:evenodd;fill:{turtle_color};fill-opacity:1;" transform="scale({sx},{sy})" d="m 1.1536693,-18.56101 c -2.105469,1.167969 -3.203125,3.441407 -3.140625,6.5 l 0.011719,0.519532 -0.300782,-0.15625 c -1.308594,-0.671875 -2.828125,-0.824219 -4.378906,-0.429688 -1.9375,0.484375 -3.8906253,2.089844 -6.0117193,4.9257825 -1.332031,1.785156 -1.714843,2.644531 -1.351562,3.035156 l 0.113281,0.125 h 0.363281 c 0.71875,0 1.308594,-0.265625 4.6679693,-2.113282 1.199219,-0.660156 2.183594,-1.199218 2.191406,-1.199218 0.00781,0 -0.023437,0.089844 -0.074218,0.195312 -0.472657,1.058594 -1.046876,2.785156 -1.335938,4.042969 -1.054688,4.574219 -0.351562,8.453125 2.101562,11.582031 0.28125,0.355469 0.292969,0.253906 -0.097656,0.722656 -2.046875,2.4609375 -3.027344,4.8984375 -2.734375,6.8046875 0.050781,0.339844 0.042969,0.335938 0.679688,0.335938 2.023437,0 4.15625,-1.316407 6.21875,-3.835938 0.222656,-0.269531 0.191406,-0.261719 0.425781,-0.113281 0.730469,0.46875 2.460938,1.390625 2.613281,1.390625 0.160157,0 1.765625,-0.753906 2.652344,-1.246094 0.167969,-0.09375 0.308594,-0.164062 0.308594,-0.160156 0.066406,0.105468 0.761719,0.855468 1.085937,1.171875 1.613282,1.570312 3.339844,2.402343 5.3593747,2.570312 0.324219,0.02734 0.355469,0.0078 0.425781,-0.316406 0.375,-1.742187 -0.382812,-4.058594 -2.1445307,-6.5585935 l -0.320312,-0.457031 0.15625,-0.183594 c 3.2460927,-3.824218 3.4335927,-9.08593704 0.558593,-15.816406 l -0.050781,-0.125 1.7382807,0.859375 c 3.585938,1.773437 4.371094,2.097656 5.085938,2.097656 0.945312,0 0.75,-0.863281 -0.558594,-2.507812 C 11.458356,-11.838353 8.3333563,-13.268041 4.8607003,-11.721166 l -0.363281,0.164063 0.019531,-0.09375 c 0.121094,-0.550781 0.183594,-1.800781 0.121094,-2.378907 -0.203125,-1.867187 -1.035157,-3.199218 -2.695313,-4.308593 -0.523437,-0.351563 -0.546875,-0.355469 -0.789062,-0.222657" >
</g>"""
TURTLE_RING_SVG_TEMPLATE = """<g id="ring" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<ellipse stroke="{pen_color}" stroke-width="3" fill="transparent" rx="{rx}" ry = "{ry}" cx="0" cy="{cy}" />
<polygon points="0,5 5,0 -5,0" transform="scale({sx},{sy})" style="fill:{turtle_color};stroke:{pen_color};stroke-width:1" />
</g>"""
TURTLE_CLASSIC_SVG_TEMPLATE = """<g id="classic" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<polygon points="-5,-4.5 0,-2.5 5,-4.5 0,4.5" transform="scale({sx},{sy})" style="stroke:{pen_color};fill:{turtle_color};stroke-width:{pw}" >
</g>"""
TURTLE_ARROW_SVG_TEMPLATE = """<g id="arrow" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<polygon points="-10,-5 0,5 10,-5" transform="scale({sx},{sy})" style="stroke:{pen_color};fill:{turtle_color};stroke-width:{pw}" >
</g>"""
TURTLE_SQUARE_SVG_TEMPLATE = """<g id="square" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<polygon points="10,-10 10,10 -10,10 -10,-10" transform="scale({sx},{sy})" style="stroke:{pen_color};fill:{turtle_color};stroke-width:{pw}" >
</g>"""
TURTLE_TRIANGLE_SVG_TEMPLATE = """<g id="triangle" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<polygon points="10,-8.66 0,8.66 -10,-8.66" transform="scale({sx},{sy})" style="stroke:{pen_color};fill:{turtle_color};stroke-width:{pw}" >
</g>"""
TURTLE_CIRCLE_SVG_TEMPLATE = """<g id="ellipse" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<ellipse stroke="{turtle_color}" style="stroke:{pen_color};fill:{turtle_color};stroke-width:{pw}" rx="{rx}" ry = "{ry}" cx="0" cy="0" >
</g>"""
TURTLE_TURTLE2_SVG_TEMPLATE = """<g id="turtle2" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<polygon points="0,-16 2,-14 1,-10 4,-7 7,-9 9,-8 6,-5 7,-1 5,3 8,6 6,8 4,5 0,7 -4,5 -6,8 -8,6 -5,3 -7,-1 -6,-5 -9,-8 -7,-9 -4,-7 -1,-10 -2,-14" transform="scale({sx},{sy})" style="stroke:{pen_color};stroke-width:1;fill:{turtle_color}" >
</g>"""

shapeDict = {"turtle":TURTLE_TURTLE_SVG_TEMPLATE, 
              "ring":TURTLE_RING_SVG_TEMPLATE, 
              "classic":TURTLE_CLASSIC_SVG_TEMPLATE,
              "arrow":TURTLE_ARROW_SVG_TEMPLATE,
              "square":TURTLE_SQUARE_SVG_TEMPLATE,
              "triangle":TURTLE_TRIANGLE_SVG_TEMPLATE,
              "circle":TURTLE_CIRCLE_SVG_TEMPLATE,
              "turtle2":TURTLE_TURTLE2_SVG_TEMPLATE,
              "blank":""}

SPEED_TO_SEC_MAP = {0: 0, 1: 1.5, 2: 1, 3: 0.75, 4: 0.5, 5: 0.3, 6: 0.25, 7: 0.2, 8: 0.15, 9: 0.10, 10: 0.05, 11: 0.025, 12: 0.01, 13: 0.005}

# Helper function that maps [0,13] speed values to ms delays
def _speedToSec(speed):
    return SPEED_TO_SEC_MAP[speed]

timeout = _speedToSec(DEFAULT_SPEED)
turtle_speed = DEFAULT_SPEED
is_turtle_visible = DEFAULT_TURTLE_VISIBILITY
pen_color = DEFAULT_PEN_COLOR
window_size = DEFAULT_WINDOW_SIZE
turtle_pos = (DEFAULT_WINDOW_SIZE[0] / 2, DEFAULT_WINDOW_SIZE[1] / 2)
turtle_degree = DEFAULT_TURTLE_DEGREE
background_color = DEFAULT_BACKGROUND_COLOR
is_pen_down = DEFAULT_IS_PEN_DOWN
svg_lines_string = DEFAULT_SVG_LINES_STRING
pen_width = DEFAULT_PEN_WIDTH
turtle_shape = DEFAULT_TURTLE_SHAPE
_mode = DEFAULT_MODE
border_color = DEFAULT_BORDER_COLOR
is_filling = False
fill_color = DEFAULT_FILL_COLOR
stretchfactor = DEFAULT_STRETCHFACTOR
tilt_angle = DEFAULT_TILT_ANGLE
outline_width = DEFAULT_OUTLINE_WIDTH
fill_rule = DEFAULT_FILL_RULE
fill_opacity = DEFAULT_FILL_OPACITY

drawing_window = None

# Construct the display for turtle
def initializeTurtle(window=None, speed=None, mode=None):
    global window_size
    global drawing_window
    global turtle_speed
    global is_turtle_visible
    global pen_color
    global turtle_pos
    global turtle_degree
    global background_color
    global is_pen_down
    global svg_lines_string
    global svg_fill_string
    global fill_rule
    global svg_dots_string
    global svg_stampsB_string
    global svg_stampsT_string
    global pen_width
    global turtle_shape
    global _mode
    global xmin,ymin,xmax,ymax
    global xscale
    global yscale
    global timeout
    global stampdictB, stampdictT
    global stampnum
    global stamplist
    global tilt_angle
    
    if window == None:
        window_size = DEFAULT_WINDOW_SIZE
    elif not (isinstance(window, tuple) and len(window) == 2 and isinstance(
            window[0], int) and isinstance(window[1], int)):
        raise ValueError('Window must be a tuple of 2 integers')
    else:
        window_size = window

    if speed == None:
         turtle_speed = DEFAULT_SPEED
    elif isinstance(speed,int) == False or speed not in range(0, 14):
        raise ValueError('Speed must be an integer in the interval [0,13]')
    else:
        turtle_speed = speed
    timeout = _speedToSec(turtle_speed)
    
    if mode == None:
        _mode = DEFAULT_MODE
    elif mode not in VALID_MODES:
        raise ValueError('Mode must be standard, world, logo, or svg')
    else:
        _mode = mode
    
    if _mode != "svg":
        xmin,ymin,xmax,ymax = -window_size[0]/2,-window_size[1]/2,window_size[0]/2,window_size[1]/2
        xscale = window_size[0]/(xmax-xmin)
        yscale = window_size[1]/(ymax-ymin)
    else:
        xmin,ymax = 0,0
        xscale = 1
        yscale = -1
       
    is_turtle_visible = DEFAULT_TURTLE_VISIBILITY
    turtle_pos = (window_size[0] / 2, window_size[1] / 2)
    turtle_degree = DEFAULT_TURTLE_DEGREE if (_mode in ["standard","world"]) else (270 - DEFAULT_TURTLE_DEGREE)
    background_color = DEFAULT_BACKGROUND_COLOR
    pen_color = DEFAULT_PEN_COLOR
    is_pen_down = DEFAULT_IS_PEN_DOWN
    svg_lines_string = DEFAULT_SVG_LINES_STRING
    pen_width = DEFAULT_PEN_WIDTH
    turtle_shape = DEFAULT_TURTLE_SHAPE
    tilt_angle = DEFAULT_TILT_ANGLE
    is_filling = False
    svg_fill_string = ''
    svg_dots_string = ''
    svg_stampsB_string = ''
    svg_stampsT_string = ''
    fill_color = DEFAULT_FILL_COLOR
    fill_rule = DEFAULT_FILL_RULE
    stampdictB = {}
    stampdictT = {}
    stampnum = 0
    stamplist=[]

    drawing_window = display(HTML(_generateSvgDrawing()), display_id=True)
    #time.sleep(timeout)   
 

# Helper function for generating svg string of the turtle
def _generateTurtleSvgDrawing():
    if is_turtle_visible:
        vis = 'visible'
    else:
        vis = 'hidden'

    turtle_x = turtle_pos[0]
    turtle_y = turtle_pos[1]
    degrees = turtle_degree + tilt_angle
    template = ''
    
    if turtle_shape in ['turtle','turtle2']:
        degrees += 90
    elif turtle_shape == 'ring':
        turtle_y += 10*stretchfactor[1]+4
        degrees -= 90
    else:
        degrees -= 90        
    
    return shapeDict[turtle_shape].format(turtle_color=fill_color,
                           pen_color=pen_color,
                           turtle_x=turtle_x, 
                           turtle_y=turtle_y,
                           visibility=vis, 
                           degrees=degrees,
                           sx=stretchfactor[0],
                           sy=stretchfactor[1],
                           rx=10*stretchfactor[0],
                           ry=10*stretchfactor[1],
                           cy=-(10*stretchfactor[1]+4),
                           pw = outline_width,
                           rotation_x=turtle_pos[0], 
                           rotation_y=turtle_pos[1])



# Helper function for generating the whole svg string
def _generateSvgDrawing():
    return SVG_TEMPLATE.format(window_width=window_size[0], 
                               window_height=window_size[1],
                               background_color=background_color,
                               fill=svg_fill_string,
                               lines=svg_lines_string,
                               dots=svg_dots_string,
                               stampsB=svg_stampsB_string,
                               stampsT=svg_stampsT_string,
                               turtle=_generateTurtleSvgDrawing(),
                               kolor=border_color)


# Helper functions for updating the screen using the latest positions/angles/lines etc.
# If the turtle speed is 0, the update is skipped so animation is done.
# If the delay is False (or 0), update immediately without any delay
def _updateDrawing(delay=True):
    if drawing_window == None:
        raise AttributeError("Display has not been initialized yet. Call initializeTurtle() before using.")
    if (turtle_speed != 0):
        drawing_window.update(HTML(_generateSvgDrawing()))         
        if delay: time.sleep(timeout)          
            
     
        
# Convert user coordinates to SVG coordinates
def _convertx(x):
    return (x-xmin)*xscale 
def _converty(y):
    return (ymax-y)*yscale


# Helper function for managing any kind of move to a given 'new_pos' and draw lines if pen is down
# Animate turtle motion along line
def _moveToNewPosition(new_pos, units):
    global turtle_pos
    global svg_lines_string
    global svg_fill_string
    global timeout
    # rounding the new_pos to eliminate floating point errors.
    new_pos = ( round(new_pos[0],3), round(new_pos[1],3) )   
    timeout_orig = timeout
  
   
    start_pos = turtle_pos           
    svg_lines_string_orig = svg_lines_string       
    s = 1 if units > 0 else -1            
    if turtle_speed != 0 and turtle_shape != 'blank' and is_turtle_visible:
        initial_pos = turtle_pos         
        alpha = math.radians(turtle_degree)
        timeout = timeout/5
        tenx, teny = 10/xscale, 10/abs(yscale)
        dunits = s*10/max(xscale,abs(yscale))
        while s*units > 0:
            dx = min(tenx,s*units)
            dy = min(teny,s*units)
            turtle_pos = (initial_pos[0] + s * dx * xscale * math.cos(alpha), initial_pos[1] + s * dy * abs(yscale) * math.sin(alpha))
            if is_pen_down:
                svg_lines_string += \
                    """<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-linecap="round" style="stroke:{pen_color};stroke-width:{pen_width}" />""".format(
                        x1=initial_pos[0],
                        y1=initial_pos[1],
                        x2=turtle_pos[0],
                        y2=turtle_pos[1],
                        pen_color=pen_color, 
                        pen_width=pen_width) 
            initial_pos = turtle_pos
            _updateDrawing()
            units -= dunits
    if is_pen_down:
        svg_lines_string = svg_lines_string_orig + \
            """<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-linecap="round" style="stroke:{pen_color};stroke-width:{pen_width}" />""".format(
                        x1=start_pos[0],
                        y1=start_pos[1],
                        x2=new_pos[0],
                        y2=new_pos[1],
                        pen_color=pen_color, 
                        pen_width=pen_width)
    if is_filling:
        svg_fill_string += """ L {x1} {y1} """.format(x1=new_pos[0],y1=new_pos[1])  
    turtle_pos = new_pos
    timeout = timeout_orig
    #_updateDrawing()

        
# Helper function for drawing arcs of radius 'r' to 'new_pos' and draw line if pen is down.
# Modified from aronma/ColabTurtle_2 github to allow arc on either side of turtle.
# Positive radius has circle to left of turtle moving counterclockwise.
# Negative radius has circle to right of turtle moving clockwise.
def _arctoNewPosition(r,new_pos):
    global turtle_pos
    global svg_lines_string
    global svg_fill_string
    
    sweep = 0 if r > 0 else 1  # SVG arc sweep flag
    rx = r*xscale
    ry = r*abs(yscale)
    
    start_pos = turtle_pos
    if is_pen_down:  
        svg_lines_string += \
        """<path d="M {x1} {y1} A {rx} {ry} 0 0 {s} {x2} {y2}" stroke-linecap="round" fill="transparent" fill-opacity="0" style="stroke:{pen_color};stroke-width:{pen_width}"/>""".format(
            x1=start_pos[0], 
            y1=start_pos[1],
            rx = rx,
            ry = ry,
            x2=new_pos[0],
            y2=new_pos[1],
            pen_color=pen_color,
            pen_width=pen_width,
            s=sweep)    
    if is_filling:
        svg_fill_string += """ A {rx} {ry} 0 0 {s} {x2} {y2} """.format(rx=r,ry=r,x2=new_pos[0],y2=new_pos[1],s=sweep)
    
    turtle_pos = new_pos
    #_updateDrawing()    
    
        
# Initialize the string for the svg path of the filled shape.
# Modified from aronma/ColabTurtle_2 github repo
# The current svg_lines_string is stored to be used when the fill is finished because the svg_fill_string will include
# the svg code for the path generated between the begin and end fill commands.
# When calling begin_fill, a value for the fill_rule can be given that will apply only to that fill.
def begin_fill(rule=None, opacity=None):
    global is_filling
    global svg_lines_string_orig
    global svg_fill_string
    if rule is None:
         rule = fill_rule
    if opacity is None:
         opacity = fill_opacity
    rule = rule.lower()
    if not rule in ['evenodd','nonzero']:
        raise ValueError("The fill-rule must be 'nonzero' or 'evenodd'.")
    if (opacity < 0) or (opacity > 1):
        raise ValueError("The fill_opacity should be between 0 and 1.")
    if not is_filling:
        svg_lines_string_orig = svg_lines_string
        svg_fill_string = """<path fill-rule="{rule}" fill-opacity="{opacity}" d="M {x1} {y1} """.format(
                x1=turtle_pos[0],
                y1=turtle_pos[1],
                rule=rule,
                opacity = opacity)
        is_filling = True
    
# Terminate the string for the svg path of the filled shape
# Modified from aronma/ColabTurtle_2 github repo
# The original svg_lines_string was previously stored to be used when the fill is finished because the svg_fill_string will include
# the svg code for the path generated between the begin and end fill commands. 
def end_fill():
    global is_filling   
    global svg_lines_string
    global svg_fill_string
    if is_filling:
        is_filling = False
        svg_fill_string += """" stroke-linecap="round" style="stroke:{pencolor};stroke-width:{penwidth}" fill="{fillcolor}" />""".format(
                pencolor=pen_color,
                penwidth=pen_width,
                fillcolor=fill_color)
        svg_lines_string = svg_lines_string_orig + svg_fill_string
        _updateDrawing()
     
# Allow user to set the svg fill-rule. Options are only 'nonzero' or 'evenodd'. If no argument, return current fill-rule.
# This can be overridden for an individual object by setting the fill-rule as an argument to begin_fill().
def fillrule(rule=None):
    global fill_rule
    if rule is None:
        return fill_rule
    if not isinstance(rule,str):
        raise ValueError("The fill-rule must be 'nonzero' or 'evenodd'.")   
    rule = rule.lower()
    if not rule in ['evenodd','nonzero']:
        raise ValueError("The fill-rule must be 'nonzero' or 'evenodd'.")   
    fill_rule = rule

# Allow user to set the svg fill-opacity. If no argument, return current fill-opacity.
# This can be overridden for an individual object by setting the fill-opacity as an argument to begin_fill().
def fillopacity(opacity=None):
    global fill_opacity
    if opacity is None:
        return fill_opacity
    if not isinstance(opacity,(int,float)):
        raise ValueError("The fill-opacity must be a number between 0 and 1.")
    if (opacity < 0) or (opacity > 1):
        raise ValueError("The fill_opacity should be between 0 and 1.")
    fill_opacity = opacity

    
# Helper function to draw a circular arc
# Modified from aronma/ColabTurtle_2 github repo
# Positive radius has arc to left of turtle, negative radius has arc to right of turtle.
def _arc(radius, degrees):
    global turtle_degree
    alpha = math.radians(turtle_degree)
    theta = math.radians(degrees)
    
    s = radius/abs(radius)  # 1=left, -1=right
    gamma = alpha-s*theta

    circle_center = (turtle_pos[0] + radius*xscale*math.sin(alpha), turtle_pos[1] - radius*abs(yscale)*math.cos(alpha))
    ending_point = (round(circle_center[0] - radius*xscale*math.sin(gamma),3) , round(circle_center[1] + radius*abs(yscale)*math.cos(gamma),3))
  
    _arctoNewPosition(radius,ending_point)
    
    turtle_degree = (turtle_degree - s*degrees) % 360
    _updateDrawing()

# Since SVG has some ambiguity when using an arc path for a complete circle,
# the circle function is broken into chunks of at most 90 degrees.
# From aronma/ColabTurtle_2 github
# Positive radius has circle to left of turtle, negative radius has circle to right of turtle.
# This circle function does NOT use the steps argument found in classical turtle.py. The kwargs
# will ignore any keyword parameter using steps.
def circle(radius, extent=360, **kwargs):
    if not isinstance(radius, (int,float)):
        raise ValueError('Circle radius should be a number')
    if not isinstance(extent, (int,float)):
        raise ValueError('Extent should be a number')      
    if extent < 0:
        raise ValueError('Extent should be a positive number')
     
    while extent > 0:
        _arc(radius,min(90,extent))
        extent += -90        

        
# Draw a dot with diameter size, using color
# If size is not given, the maximum of pen_width+4 and 2*pen_width is used.
def dot(size = None, *color):
    global svg_dots_string

    if not color:
        if isinstance(size, (str, tuple)):
            color = _processColor(size)
            size = pen_width + max(pen_width,4)
        else:
            color = pen_color
            if not size:
                size = pen_width + max(pen_width,4)
    else:
        if size is None:
            size = pen_width + max(pen_width,4)
        color = _processColor(color[0])
    svg_dots_string += """<circle cx="{cx}" cy="{cy}" r="{radius}" fill="{kolor}" fill-opacity="1" />""".format(
            radius=size/2,
            cx=turtle_pos[0],
            cy=turtle_pos[1],
            kolor=color)
    _updateDrawing()
 

# Makes the turtle move forward by 'units' units
def forward(units):
    if not isinstance(units, (int,float)):
        raise ValueError('Units must be a number.')
    alpha = math.radians(turtle_degree)
    new_pos = (turtle_pos[0] + units * xscale * math.cos(alpha), turtle_pos[1] + units * abs(yscale) * math.sin(alpha))
    _moveToNewPosition(new_pos,units)

fd = forward # alias

# Makes the turtle move backward by 'units' units
def backward(units):
    if not isinstance(units, (int,float)):
        raise ValueError('Units must be a number.')
    forward(-1 * units)

bk = backward # alias
back = backward # alias


# Makes the turtle move right by 'degrees' degrees (NOT radians)
# Uses SVG animation to rotate turtle.
# But this doesn't work for turtle=ring and if stretch factors are different for x and y directions,
# so in that case break the rotation into pieces of at most 30 degrees.
def right(degrees):
    global turtle_degree
    global stretchfactor
    global timeout
    if not isinstance(degrees, (int,float)):
        raise ValueError('Degrees must be a number.')  
    timeout_orig = timeout
    timeout = timeout/3
    if turtle_speed == 0 or turtle_shape == 'blank' or not is_turtle_visible:
        turtle_degree = (turtle_degree + degrees) % 360
        _updateDrawing()
    elif turtle_shape != 'ring' and stretchfactor[0]==stretchfactor[1]:
        stretchfactor_orig = stretchfactor
        template = shapeDict[turtle_shape]        
        tmp = """<animateTransform id = "one" attributeName="transform" 
                      type="scale"
                      from="1 1" to="{sx} {sy}"
                      begin="0s" dur="0.001s"
                      repeatCount="1"
                      additive="sum"
                      fill="freeze"
            /><animateTransform attributeName="transform"
                    type="rotate"
                    from="0 0 0" to ="{extent} 0 0"
                    begin="one.end" dur="{t}s"
                    repeatCount="1"
                    additive="sum"
                    fill="freeze"
          /></g>""".format(extent=degrees, t=timeout*abs(degrees)/90, sx=stretchfactor[0], sy=stretchfactor[1])
        newtemplate = template.replace("</g>",tmp)
        shapeDict.update({turtle_shape:newtemplate})
        stretchfactor = 1,1
        timeout = timeout*abs(degrees)/90+0.001
        _updateDrawing()
        turtle_degree = (turtle_degree + degrees) % 360
        shapeDict.update({turtle_shape:template})
        stretchfactor = stretchfactor_orig
        timeout = timeout_orig
    else: #turtle_shape == 'ring' or stretchfactor[0] != stretchfactor[1]
        turtle_degree_orig = turtle_degree
        timeout = timeout/3
        s = 1 if degrees > 0 else -1
        while s*degrees > 0:
            if s*degrees > 30:
                turtle_degree = (turtle_degree + s*30) % 360
            else:
                turtle_degree = (turtle_degree + degrees) % 360
            _updateDrawing()
            degrees -= s*30
        timeout = timeout_orig
        turtle_degree = (turtle_degree + degrees) % 360

rt = right # alias

# Makes the turtle move right by 'degrees' degrees (NOT radians, this library does not support radians right now)
def left(degrees):
    right(-1 * degrees)

lt = left


# Makes the turtle face a given direction
def face(degrees):
    global turtle_degree

    if not isinstance(degrees, (int,float)):
        raise ValueError('Degrees must be a number.')
    if _mode in ["standard","world"]: 
        new_degree = (360 - degrees) 
    elif _mode == "logo":
        new_degree = (270 + degrees) 
    else: # mode = "svg"
        new_degree = degrees % 360
    alpha = (new_degree - turtle_degree) % 360
    if turtle_speed !=0 and turtle_shape != 'blank' and is_turtle_visible:
        if alpha <= 180:
            right(alpha)
        else:
            left(360-alpha)
    else:
        turtle_degree = new_degree
        _updateDrawing()

setheading = face # alias
seth = face # alias


# Raises the pen such that following turtle moves will not cause any drawings
def penup():
    global is_pen_down
    is_pen_down = False

pu = penup # alias
up = penup # alias

# Lowers the pen such that following turtle moves will now cause drawings
def pendown():
    global is_pen_down
    is_pen_down = True

pd = pendown # alias
down = pendown # alias

def isdown():
    return is_pen_down


# Update the speed of the moves, [0,13]
# If argument is omitted, it returns the speed.
def speed(speed = None):
    global timeout
    global turtle_speed
    
    if speed is None:
        return turtle_speed

    if isinstance(speed,int) == False or speed not in range(0, 14):

                raise ValueError('Speed must be an integer in the interval [0,13].')
        
    turtle_speed = speed
    timeout = _speedToSec(speed)

# Call this function at end of turtle commands when speed=0 (no animation) so that final image is drawn
def done():
    if drawing_window == None:
        raise AttributeError("Display has not been initialized yet. Call initializeTurtle() before using.")
    drawing_window.update(HTML(_generateSvgDrawing()))        


# Move the turtle to a designated 'x' x-coordinate, y-coordinate stays the same
def setx(x):
    if not isinstance(x, (int,float)):
        raise ValueError('new x position must be a number.')
    goto(x, gety())

# Move the turtle to a designated 'y' y-coordinate, x-coordinate stays the same
def sety(y):
    if not isinstance(y, (int,float)):
        raise ValueError('New y position must be a number.')
    goto(getx(), y)

# Move turtle to center of widnow and set its heading to its 
# start-orientation (which depends on the mode).
def home():
    global turtle_degree
    if _mode != 'svg':
        goto(0,0)
    else:
        goto( (window_size[0] / 2, window_size[1] / 2) )
    if _mode in ['standard','world']:
        if turtle_degree <= 180:
            left(turtle_degree)
        else:
            right(360-turtle_degree)        
    else:
        if turtle_degree < 90:
            left(turtle_degree+90)
        elif turtle_degree < 270:
            right(270-turtle_degree)
        else:
            left(turtle_degree-270)
    

# Move the turtle to a designated position.
def goto(x, y=None):
    global turtle_degree
    global tilt_angle
    if isinstance(x, tuple) and y is None:
        if len(x) != 2:
            raise ValueError('The tuple argument must be of length 2.')
        y = x[1]
        x = x[0]
    if not isinstance(x, (int,float)):
        raise ValueError('New x position must be a number.')
    if not isinstance(y, (int,float)):
        raise ValueError('New y position must be a number.')
    tilt_angle_orig = tilt_angle
    turtle_angle_orig = turtle_degree
    alpha = towards(x,y)
    units = distance(x,y)
    if _mode in ["standard","world"]: 
        turtle_degree = (360 - alpha) % 360
        tilt_angle = turtle_angle_orig+tilt_angle+alpha
    elif _mode == "logo":
        turtle_degree = (270 + alpha) % 360
        tilt_angle = turtle_angle_orig+tilt_angle-alpha-270
    else: # mode = "svg"
        turtle_degree = alpha % 360
        tilt_angle = turtle_angle_orig+tilt_angle-alpha
    _moveToNewPosition((_convertx(x), _converty(y)),units)
    tilt_angle = tilt_angle_orig
    turtle_degree = turtle_angle_orig

setpos = goto # alias
setposition = goto # alias


# Retrieve the turtle's currrent 'x' x-coordinate in current coordinate system
def getx():
    return(turtle_pos[0]/xscale+xmin)

xcor = getx # alias

# Retrieve the turtle's currrent 'y' y-coordinate in current coordinate system
def gety():
    return(ymax-turtle_pos[1]/yscale)

ycor = gety # alias

# Retrieve the turtle's current position as a (x,y) tuple vector in current coordinate system
def position():
    return (turtle_pos[0]/xscale+xmin, ymax-turtle_pos[1]/yscale)

pos = position # alias

# Retrieve the turtle's current angle
def getheading():
    if _mode in ["standard","world"]:
        return (360 - turtle_degree) % 360
    elif _mode == "logo":
        return (turtle_degree - 270) % 360
    else: # mode = "svg"
        return turtle_degree % 360

heading = getheading # alias


# Switch turtle visibility to ON
def showturtle():
    global is_turtle_visible
    is_turtle_visible = True
    _updateDrawing(0)

st = showturtle # alias

# Switch turtle visibility to OFF
def hideturtle():
    global is_turtle_visible
    is_turtle_visible = False
    _updateDrawing(0)

ht = hideturtle # alias

def isvisible():
    return is_turtle_visible


def _validateColorString(color):
    if color in VALID_COLORS: # 140 predefined html color names
        return True
    if re.search("^#(?:[0-9a-fA-F]{3}){1,2}$", color): # 3 or 6 digit hex color code
        return True
    if re.search("rgb\(\s*(?:(?:\d{1,2}|1\d\d|2(?:[0-4]\d|5[0-5]))\s*,?){3}\)$", color): # rgb color code
        return True
    return False

def _validateColorTuple(color):
    if len(color) != 3:
        return False
    if not isinstance(color[0], int) or not isinstance(color[1], int) or not isinstance(color[2], int):
        return False
    if not 0 <= color[0] <= 255 or not 0 <= color[1] <= 255 or not 0 <= color[2] <= 255:
        return False
    return True

def _processColor(color):
    if isinstance(color, str):
        if color == "": color = "none"
        color = color.lower().strip()
        if not _validateColorString(color):
            raise ValueError('Color is invalid. It can be a known html color name, 3-6 digit hex string, or rgb string.')
        return color
    elif isinstance(color, tuple):
        if not _validateColorTuple(color):
            raise ValueError('Color tuple is invalid. It must be a tuple of three integers, which are in the interval [0,255]')
        return 'rgb(' + str(color[0]) + ',' + str(color[1]) + ',' + str(color[2]) + ')'
    else:
        raise ValueError('The color parameter must be a color string or a tuple')

# Change the background color of the drawing area
# If color='none', the drawing window will have no background fill.
# If no params, return the current background color
def bgcolor(color = None, c2 = None, c3 = None):
    global background_color
    if color is None:
        return background_color
    elif c2 is not None:
        if c3 is None:
            raise ValueError('If the second argument is set, the third arguments must be set as well to complete the rgb set.')
        color = (color, c2, c3)

    background_color = _processColor(color)
    _updateDrawing(0)

# Change the color of the pen
# If no params, return the current pen color
def pencolor(color = None, c2 = None, c3 = None):
    global pen_color
    if color is None:
        return pen_color
    elif c2 is not None:
        if c3 is None:
            raise ValueError('If the second argument is set, the third arguments must be set as well to complete the rgb set.')
        color = (color, c2, c3)

    pen_color = _processColor(color)
    _updateDrawing(0)

# Change the fill color
# If no params, return the current fill color
def fillcolor(color = None, c2 = None, c3 = None):
    global fill_color
    if color is None:
        return fill_color
    elif c2 is not None:
        if c3 is None:
            raise ValueError('If the second argument is set, the third arguments must be set as well to complete the rgb set.')
        color = (color, c2, c3)

    fill_color = _processColor(color)
    _updateDrawing(0)

# Return or set pencolor and fillcolor
def color(*args):
    global pen_color
    global fill_color
    if args:
        narg = len(args)
        if narg == 1:
            pen_color = fill_color = _processColor(args[0])
        elif narg == 2:
            pen_color = _processColor(args[0])
            fill_color = _processColor(args[1])
        elif narg == 3:
            kolor = (args[0],args[1],args[2])
            pen_color = fill_color = _processColor(kolor)
        else:
            raise ValueError('Syntax: color(colorstring), color((r,g,b)), color(r,g,b), color(string1,string2), color((r1,g1,b1),(r2,g2,b2))')
    else:
        return pen_color,fill_color
    _updateDrawing(0)

        
# Change the width of the lines drawn by the turtle, in pixels
# If the function is called without arguments, it returns the current width
def width(width = None):
    global pen_width

    if width is None:
        return pen_width
    else:
        if not isinstance(width, int):
            raise ValueError('New width value must be an integer.')
        if not width > 0:
            raise ValueError('New width value must be positive.')

        pen_width = width
    _updateDrawing(0)

pensize = width  #alias


# Calculate the distance between the turtle and a given point
def distance(x, y=None):
    if isinstance(x, tuple) and y is None:
        if len(x) != 2:
            raise ValueError('The tuple argument must be of length 2.')
        y = x[1]
        x = x[0]

    if not isinstance(x, (int,float)):
        raise ValueError('The x position must be a number.')

    if not isinstance(y, (int,float)):
        raise ValueError('The y position must be a number.')
    
    return round(math.sqrt( (getx() - x) ** 2 + (gety() - y) ** 2 ), 8)


# Return the angle between the line from turtle position to position specified by (x,y)
# This depends on the turtle’s start orientation which depends on the mode - standard/world or logo.  
def towards(x, y=None):
    if isinstance(x, tuple) and y is None:
        if len(x) != 2:
            raise ValueError('The tuple argument must be of length 2.')
        y = x[1]
        x = x[0] 
        
    if not isinstance(x, (int,float)):
        raise ValueError('The x position must be a number.')

    if not isinstance(y, (int,float)):
        raise ValueError('The y position must be a number.') 
    
    dx = x - getx()
    dy = y - gety()
    if _mode == "svg":
        dy = -dy
    result = round(math.atan2(dy,dx)*180.0/math.pi, 10) % 360.0
    if _mode in ["standard","world"]:
        return result
    elif _mode == "logo":
        return (90 - result) % 360
    else:  # mode = "svg"
        return (360 - result) % 360
 
        
# Clear any text or drawing on the screen
def clear():
    global svg_lines_string
    global svg_fill_string
    global svg_dots_string

    svg_lines_string = ""
    svg_fill_string = ""
    svg_dots_string = ""
    _updateDrawing(0)


def write(obj, **kwargs):
    global svg_lines_string
    global turtle_pos
    text = str(obj)
    font_size = 12
    font_family = 'Arial'
    font_type = 'normal'
    align = 'start'

    if 'align' in kwargs and kwargs['align'] in ('left', 'center', 'right'):
        if kwargs['align'] == 'left':
            align = 'start'
        elif kwargs['align'] == 'center':
            align = 'middle'
        else:
            align = 'end'

    if "font" in kwargs:
        font = kwargs["font"]
        if len(font) != 3 or isinstance(font[0], int) == False \
                          or isinstance(font[1], str) == False \
                          or font[2] not in {'bold','italic','underline','normal'}:
            raise ValueError('Font parameter must be a triplet consisting of font size (int), font family (str) and font type. Font type can be one of {bold, italic, underline, normal}')
        font_size = font[0]
        font_family = font[1]
        font_type = font[2]
        
    style_string = ""
    style_string += "font-size:" + str(font_size) + "px;"
    style_string += "font-family:'" + font_family + "';"

    if font_type == 'bold':
        style_string += "font-weight:bold;"
    elif font_type == 'italic':
        style_string += "font-style:italic;"
    elif font_type == 'underline':
        style_string += "text-decoration: underline;"
            
    svg_lines_string += """<text x="{x}" y="{y}" fill="{fill_color}" text-anchor="{align}" style="{style}">{text}</text>""".format(
            x=turtle_pos[0], 
            y=turtle_pos[1], 
            text=text, 
            fill_color=pen_color, 
            align=align, 
            style=style_string)
    
    _updateDrawing()


# Set turtle shape to shape with given name or, if name is not given, return name of current shape
def shape(name=None):
    global turtle_shape
    if name is None:
        return turtle_shape
    elif name.lower() not in VALID_TURTLE_SHAPES:
        raise ValueError('Shape is invalid. Valid options are: ' + str(VALID_TURTLE_SHAPES))
    
    turtle_shape = name.lower()
    _updateDrawing()


# Set turtle mode (“standard”, “logo”, “world”, or "svg") and reset the window. If mode is not given, current mode is returned.
def mode(mode=None):
    global _mode
    if mode is None:
        return _mode
    elif mode.lower() not in VALID_MODES:
        raise ValueError('Mode is invalid. Valid options are: ' + str(VALID_MODES))
    _mode = mode.lower()   
    reset()
   
        
# Return turtle window width
def window_width():
    return window_size[0]

# Return turtle window height
def window_height():
    return window_size[1]


# Save the image as an SVG file using given filename. Set turtle=True to include turtle in svg output
def saveSVG(file, turtle=False):
    if drawing_window == None:
        raise AttributeError("Display has not been initialized yet. Call initializeTurtle() before using.")
    if not isinstance(file, str):
        raise ValueError("File name must be a string")
    if not file.endswith(".svg"):
        file += ".svg"
    text_file = open(file, "w")
    header = ("""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">\n""").format(
            w=window_size[0],
            h=window_size[1]) 
    header += ("""<rect width="100%" height="100%" style="fill:{fillcolor};stroke:{kolor};stroke-width:1" />\n""").format(
            fillcolor=background_color,
            kolor=border_color)
    image = svg_lines_string.replace("/>","/>\n")
    stampsB = svg_stampsB_string.replace("</g>","</g>\n")
    stampsT = svg_stampsT_string.replace("</g>","</g>\n")
    dots = svg_dots_string.replace(">",">\n")
    turtle_svg = (_generateTurtleSvgDrawing() + " \n") if turtle else ""
    output = header + stampsB + image + dots + stampsT + turtle_svg + "</svg>"
    text_file.write(output)
    text_file.close()

# Print the SVG code for the image to the screen. Set turtle=True to include turtle in svg output.
def showSVG(turtle=False):
    if drawing_window == None:
        raise AttributeError("Display has not been initialized yet. Call initializeTurtle() before using.")
    header = ("""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">\n""").format(
            w=window_size[0],
            h=window_size[1]) 
    header += ("""<rect width="100%" height="100%" style="fill:{fillcolor};stroke:{kolor};stroke-width:1" />\n""").format(
            fillcolor=background_color,
            kolor=border_color)
    image = svg_lines_string.replace(">","/>\n")
    stampsB = svg_stampsB_string.replace("</g>","</g>\n")
    stampsT = svg_stampsT_string.replace("</g>","</g>\n")    
    dots = svg_dots_string.replace(">",">\n")
    turtle_svg = (_generateTurtleSvgDrawing() + " \n") if turtle else ""
    output = header + stampsB + image + dots + stampsT + turtle_svg + "</svg>"
    print(output) 


# Set up user-defined coordinate system using lower left and upper right corners.
# ATTENTION: in user-defined coordinate systems angles may appear distorted.
def setworldcoordinates(llx, lly, urx, ury):
    global xmin
    global xmax
    global ymin
    global ymax
    global xscale
    global yscale
    global _mode
    
    if drawing_window == None:
        raise AttributeError("Display has not been initialized yet. Call initializeTurtle() before using.")
    elif (urx-llx <= 0):
        raise ValueError("Lower left x-coordinate should be less than upper right x-coordinate")
    elif (ury-lly <= 0):
        raise ValueError("Lower left y-coordinate should be less than upper right y-coordinate")
                       
    xmin = llx
    ymin = lly
    xmax = urx
    ymax = ury
    xscale = window_size[0]/(xmax-xmin)
    yscale = window_size[1]/(ymax-ymin)
    _mode = "world"
    

# Show a border around the graphics window. Default (no parameters) is gray. A border can be turned off by setting color='none'. 
def showBorder(color = None, c2 = None, c3 = None):
    global border_color
    if color is None:
        color = "gray"
    elif c2 is not None:
        if c3 is None:
            raise ValueError('If the second argument is set, the third arguments must be set as well to complete the rgb set.')
        color = (color, c2, c3)

    border_color = _processColor(color)
    _updateDrawing(0)

# Hide the border around the graphics window.    
def hideBorder():
    global border_color
    border_color = "none"
    _updateDrawing(0)


# Set the defaults used in the original version of ColabTurtle package
def OldDefaults():
    global DEFAULT_BACKGROUND_COLOR
    global DEFAULT_PEN_COLOR
    global DEFAULT_PEN_WIDTH
    global DEFAULT_MODE
    global DEFAULT_TURTLE_SHAPE
    global DEFAULT_WINDOW_SIZE
    global DEFAULT_TURTLE_DEGREE
    
    DEFAULT_BACKGROUND_COLOR = "black"
    DEFAULT_PEN_COLOR = "white"
    DEFAULT_PEN_WIDTH = 4
    DEFAULT_MODE = 'svg'
    DEFAULT_TURTLE_SHAPE = "turtle"
    DEFAULT_WINDOW_SIZE = (800, 500)
    


# Delete the turtle’s drawings from the screen, re-center the turtle and set (most) variables to the default values.
def reset():
    global is_turtle_visible
    global pen_color
    global background_color
    global is_pen_down
    global pen_width
    global svg_lines_string
    global svg_fill_string
    global svg_dots_string
    global turtle_degree  
    global turtle_pos
    global fill_color
    global border_color
    global turtle_shape
    global stretchfactor
    global tilt_angle
    global outline_width

    is_turtle_visible = True
    pen_color = DEFAULT_PEN_COLOR
    fill_color = DEFAULT_FILL_COLOR
    border_color = DEFAULT_BORDER_COLOR
    background_color = DEFAULT_BACKGROUND_COLOR
    #turtle_shape = DEFAULT_TURTLE_SHAPE
    is_pen_down = True
    pen_width = DEFAULT_PEN_WIDTH
    stretchfactor = DEFAULT_STRETCHFACTOR
    tilt_angle = DEFAULT_TILT_ANGLE
    outline_width = DEFAULT_OUTLINE_WIDTH
    svg_lines_string = ""
    svg_fill_string = ""
    svg_dots_string = ""
    svg_stampsB_string = ""
    svg_stampsT_string = ""
    stampdictB = {}
    stampdictT = {}
    stampnum = 0
    stamplist = []
    turtle_degree = DEFAULT_TURTLE_DEGREE if (_mode in ["standard","world"]) else (270 - DEFAULT_TURTLE_DEGREE)
    turtle_pos = (window_size[0] / 2, window_size[1] / 2)
    _updateDrawing(0)


# Scale the size of the turtle
# stretch_wid scales perpendicular to orientation
# stretch_len scales in direction of turtle's orientation
def shapesize(stretch_wid=None, stretch_len=None, outline=None):
    global stretchfactor
    global outline_width

    if stretch_wid is stretch_len is outline is None:
        return stretchfactor[0], stretchfactor[1], outline_width

    if stretch_wid == 0 or stretch_len == 0:
        raise ValueError("stretch_wid/stretch_len must not be zero")
    if stretch_wid is not None:
        if not isinstance(stretch_wid, (int,float)):
            raise ValueError('The stretch_wid position must be a number.')        
        if stretch_len is None:
            stretchfactor = stretch_wid, stretch_wid
        else:
            if not isinstance(stretch_len, (int,float)):
                raise ValueError('The stretch_len position must be a number.')                
            stretchfactor = stretch_wid, stretch_len
    elif stretch_len is not None:
        if not isinstance(stretch_len, (int,float)):
            raise ValueError('The stretch_len position must be a number.')         
        stretchfactor = stretch_len, stretch_len
    if outline is None:
        outline = outline_width
    elif not isinstance(outline, (int,float)):
        raise ValueError('The outline must be a positive number.')        
    outline_width = outline
        
turtlesize = shapesize #alias


# Stamp a copy of the turtle shape onto the canvas at the current turtle position.
# The argument determines whether the stamp appears below other items (layer=0) or above other items (layer=1) in 
# the order that SVG draws items. So if layer=0, a stamp may be covered by a filled object, for example, even if
# the stamp is originally drawn on top of the object during the animation. To prevent this, set layer=1 (or any nonzero number).
# Returns a stamp_id for that stamp, which can be used to delete it by calling clearstamp(stamp_id).
def stamp(layer=0):
    global svg_stampsB_string
    global svg_stampsT_string
    global stampnum
    global stamplist
    stampnum += 1
    stamplist.append(stampnum)
    if layer != 0:
        stampdictT[stampnum] = _generateTurtleSvgDrawing()
        svg_stampsT_string += stampdictT[stampnum]
    else:
        stampdictB[stampnum] = _generateTurtleSvgDrawing()
        svg_stampsB_string += stampdictB[stampnum]
    _updateDrawing(0)
    return stampnum

# Helper function to do the work for clearstamp() and clearstamps()
def _clearstamp(stampid):
    global stampdictB
    global stampdictT
    global svg_stampsB_string
    global svg_stampsT_string  
    global stamplist
    tmp = ""
    if stampid in stampdictB.keys():
        stampdictB.pop(stampid)
        stamplist.remove(stampid)
        for n in stampdictB:
            tmp += stampdictB[n]
        svg_stampsB_string = tmp        
    elif stampid in stampdictT.keys():
        stampdictT.pop(stampid)
        stamplist.remove(stampid)
        for n in stampdictT:
            tmp += stampdictT[n]
        svg_stampsT_string = tmp
    _updateDrawing(0)

# Delete stamp with given stampid.
# stampid – an integer or tuple of integers, which must be return values of previous stamp() calls
def clearstamp(stampid):
    if isinstance(stampid,tuple):
        for subitem in stampid:
            _clearstamp(subitem)
    else:
        _clearstamp(stampid)

# Delete all or first/last n of turtle’s stamps. If n is None, delete all stamps, if n > 0 delete first n stamps,
# else if n < 0 delete last n stamps.
def clearstamps(n=None):
    if n is None:
        [_clearstamp(k) for k in stamplist]
    elif n > 0:
        [_clearstamp(k) for k in stamplist[:n]]
    elif n < 0:
        [_clearstamp(k) for k in stamplist[n:]]

# Get the color corresponding to position n in the valid color list
def getcolor(n):
    if (n < 0) or (n > 139):
        raise valueError("color request must be between 0 and 139")
    return VALID_COLORS[n]


# Return or set the pen's attributes
def pen(dictname=None, **pendict):
    global is_turtle_visible
    global is_pen_down
    global pen_color
    global fill_color
    global pen_width
    global turtle_speed
    global stretchfactor
    global outline_width
    global tilt_angle
    global timeout
    _pd = {"shown"          : is_turtle_visible,
           "pendown"        : is_pen_down,
           "pencolor"       : pen_color,
           "fillcolor"      : fill_color,
           "pensize"        : pen_width,
           "speed"          : turtle_speed,
           "stretchfactor"  : stretchfactor,
           "tilt"           : tilt_angle,
           "outline"        : outline_width
          }
    if not (dictname or pendict):
        return _pd
    if isinstance(dictname,dict):
        p = dictname
    else:
        p = {}
    p.update(pendict)
    if "shown" in p:
        is_turtle_visible = p["shown"]
    if "pendown" in p:
        is_pen_down = p["pendown"]
    if "pencolor" in p:
        pen_color = _processColor(p["pencolor"])
    if "fillcolor" in p:
        fill_color = _processColor(p["fillcolor"])
    if "pensize" in p:
        pen_width = p["pensize"]
    if "speed" in p:
        turtle_speed = p["speed"]
        timeout = _speedToSec(turtle_speed)
    if "stretchfactor" in p:
        sf = p["stretchfactor"]
        if isinstance(sf, (int,float)):
            sf = (sf,sf)
        stretchfactor = sf
    if "tilt" in p:
        tilt_angle = tilt
    if "outline" in p:
        outline_width = p["outline"]
    _updateDrawing(0)
    

# Rotate the turtle shape by angle from its current tilt-angle, but do not change the turtle’s heading (direction of movement).
def tilt(angle):
    global tilt_angle
    if _mode in ["standard","world"]:
        tilt_angle -= angle
    else:
        tilt_angle += angle
    _updateDrawing(0)

# Rotate the turtleshape to point in the direction specified by angle, regardless of its current tilt-angle.
# DO NOT change the turtle's heading (direction of movement). Deprecated since Python version 3.1.
def settiltangle(angle):
    global tilt_angle
    if _mode in ["standard","world"]:
        tilt_angle = -angle
    else:
        tilt_angle = angle
    _updateDrawing(0)    

# Set or return the current tilt-angle. 
# If angle is given, rotate the turtleshape to point in the direction specified by angle, regardless of its current tilt-angle. 
# Do not change the turtle’s heading (direction of movement). If angle is not given: return the current tilt-angle, 
# i. e. the angle between the orientation of the turtleshape and the heading of the turtle (its direction of movement).
def tiltangle(angle=None):
    global tilt_angle
    if angle == None:
        return tilt_angle
    else:
        settiltangle(angle)
   
