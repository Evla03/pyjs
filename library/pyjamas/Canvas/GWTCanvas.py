"""
* Copyright 2008 Google Inc.
*
* Licensed under the Apache License, Version 2.0 (the "License"); you may not
* use this file except in compliance with the License. You may obtain a copy of
* the License at
*
* http:#www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
* WARRANTIES OR CONDITIONS OF ANY KIND, either express or self.implied. See the
* License for the specific language governing permissions and limitations under
* the License.
"""

from pyjamas import DOM

from pyjamas.ui.FocusWidget import FocusWidget
from pyjamas.ui import Focus
from pyjamas.Canvas.Color import Color

from pyjamas.Canvas.LinearGradientImplDefault import LinearGradientImplDefault
from pyjamas.Canvas.RadialGradientImplDefault import RadialGradientImplDefault
from pyjamas.Canvas.GWTCanvasImplDefault import GWTCanvasImplDefault

from pyjamas.Canvas.LinearGradientImplIE6 import LinearGradientImplIE6
from pyjamas.Canvas.RadialGradientImplIE6 import RadialGradientImplIE6
from pyjamas.Canvas.GWTCanvasImplIE6 import GWTCanvasImplIE6



"""*
* 2D Graphics API. API mimicks functionality found in the Javascript canvas API
* (see <a href="http:#developer.mozilla.org/en/docs/Canvas_tutorial">canvas
* tutorial</a>).
*
* <p>
* Performance may scale differently for IE than for browsers with a native
* canvas self.implementation. Sub-pixel precision is supported where possible.
* </p>
"""
class GWTCanvas(FocusWidget):
    
    """*
    * Creates a GWTCanvas element. Element type depends on deferred binding.
    * Default is CANVAS HTML5 DOM element. In the case of IE it should be VML.
    *
    * <p>
    * Different coordinate spaces and pixel spaces will cause aliased scaling.
    * Use <code>scale(double,double)</code> and consistent coordinate and pixel
    * spaces for better results.
    * </p>
    *
    * @param coordX the size of the coordinate space in the x direction
    * @param coordY the size of the coordinate space in the y direction
    * @param pixelX the CSS width in pixels of the canvas element
    * @param pixelY the CSS height in pixels of the canvas element
    """
    def __init__(self, coordX=300, coordY=150, pixelX=300, pixelY=150,
                       **kwargs):
        
        """
        * Impl Instance. Compiler should statify all the methods, so we
        * do not end up with duplicate code for each canvas instance.
        """
        self.impl = self.getCanvasImpl()
        
        self.coordHeight = 0
        self.coordWidth = 0
        focusable = Focus.createFocusable()
        self.canvas = self.impl.createElement()
        DOM.appendChild(focusable, self.canvas)
        FocusWidget.__init__(self, focusable, **kwargs)

        self.setPixelWidth(pixelX)
        self.setPixelHeight(pixelY)
        self.setCoordSize(coordX, coordY)
    
    def getCanvasElement(self):
        return self.getElement().firstChild

    def getCanvasImpl(self):
        return GWTCanvasImplDefault()
    
    """*
    * Draws an arc. If the context has a non-empty path, then the method must add
    * a straight line from the last point in the path to the start point of the
    * arc.
    *
    * @param x center X coordinate
    * @param y center Y coordinate
    * @param radius radius of drawn arc
    * @param startAngle angle measured from positive X axis to start of arc CW
    * @param endAngle angle measured from positive X axis to end of arc CW
    * @param antiClockwise direction that the arc line is drawn
    """
    def arc(self, x, y, radius, startAngle, endAngle, antiClockwise):
        self.impl.arc(x, y, radius, startAngle, endAngle, antiClockwise)
    
    
    """*
    * Erases the current path and prepares it for a path.
    """
    def beginPath(self):
        self.impl.beginPath()
    
    
    """*
    * Clears the entire canvas.
    """
    def clear(self):
        # we used local references instead of looking up the attributes
        # on the DOM element
        self.impl.clear(self.coordWidth, self.coordHeight)
    
    
    """*
    * Closes the current path. "Closing" simply means that a line is drawn from
    * the last element in the path back to the first.
    """
    def closePath(self):
        self.impl.closePath()
    
    
    """*
    *
    * Creates a LinearGradient Object for use as a fill or stroke style.
    *
    * @param x0 x coord of start point of gradient
    * @param y0 y coord of start point of gradient
    * @param x1 x coord of end point of gradient
    * @param y1 y coord of end point of gradient
    * @return returns the CanvasGradient
    """
    def createLinearGradient(self, x0, y0, x1, y1):
        return LinearGradientImplDefault(x0, y0, x1, y1, self.getCanvasElement())
    
    
    """*
    *
    * Creates a RadialGradient Object for use as a fill or stroke style.
    *
    * @param x0 x coord of origin of start circle
    * @param y0 y coord of origin of start circle
    * @param r0 radius of start circle
    * @param x1 x coord of origin of end circle
    * @param y1 y coord of origin of end circle
    * @param r1 radius of the end circle
    * @return returns the CanvasGradient
    """
    def createRadialGradient(self, x0, y0, r0, x1, y1, r1):
        return RadialGradientImplDefault(x0, y0, r0, x1, y1, r1,
                                        self.getCanvasElement())
    
    
    """*
    *
    * Does nothing if the context's path is empty. Otherwise, it connects the
    * last point in the path to the given point <b>(x, y)</b> using a cubic
    * Bezier curve with control points <b>(cp1x, cp1y)</b> and <b>(cp2x,
    * cp2y)</b>. Then, it must add the point <b>(x, y)</b> to the path.
    *
    * This function corresponds to the
    * <code>bezierCurveTo(cp1x, cp1y, cp2x, cp2y, x, y)</code> method in canvas
    * element Javascript API.
    *
    * @param cp1x x coord of first Control Point
    * @param cp1y y coord of first Control Point
    * @param cp2x x coord of second Control Point
    * @param cp2y y coord of second Control Point
    * @param x x coord of point
    * @param y x coord of point
    """
    def cubicCurveTo(self, cp1x, cp1y, cp2x, cp2y, x, y):
        self.impl.cubicCurveTo(cp1x, cp1y, cp2x, cp2y, x, y)
    
    
    """*
    * Draws an input image at a given position on the canvas. Resizes image
    * according to specified width and height and samples from the specified
    * sourceY and sourceX.
    *
    * <p>
    * We recommend that the pixel and coordinate spaces be the same to provide
    * consistent positioning and scaling results
    * </p>
    *
    option 1:
    * @param img the image to be drawn
    * @param offsetX x coord of the top left corner in the destination space
    * @param offsetY y coord of the top left corner in the destination space
    * @param img The image to be drawn

    option 2:
    * @param offsetX x coord of the top left corner in the destination space
    * @param offsetY y coord of the top left corner in the destination space
    * @param width the size of the image in the destination space
    * @param height the size of the image in the destination space
    
    option 3:
    * @param img the image to be drawn
    * @param sourceX the start X position in the source image
    * @param sourceY the start Y position in the source image
    * @param sourceWidth the width in the source image you want to sample
    * @param sourceHeight the height in the source image you want to sample
    * @param destX the start X position in the destination image
    * @param destY the start Y position in the destination image
    * @param destWidth the width of drawn image in the destination
    * @param destHeight the height of the drawn image in the destination
    """
    def drawImage(self, img, *args):
        if isinstance(img, Widget):
            img_width = img.getWidth()
            img_height = img.getHeight()
        else:
            img_width = DOM.getIntAttribute(img, "offsetWidth")
            img_height = DOM.getIntAttribute(img, "offsetHeight")
        if len(args) == 8:
            self.impl.drawImage(img, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7])
        elif len(args) == 4:
            sourceX = 0
            sourceY = 0
            sourceWidth = img_width
            sourceHeight = img_height
            destX = args[0]
            destY = args[1]
            destWidth = args[2]
            destHeight = args[3]
            self.impl.drawImage(img, sourceX, sourceY,
                                     sourceWidth, sourceHeight,
                                     destX, destY, destWidth, destHeight)
        elif len(args) == 2:
            self.impl.drawImage(img, args[0], args[1])
    
    
    """*
    * Fills the current path according to the current fillstyle.
    """
    def fill(self):
        self.impl.fill()
    
    
    """*
    * Fills a rectangle of the specified dimensions, at the specified start
    * coords, according to the current fillstyle.
    *
    * @param startX x coord of the top left corner in the destination space
    * @param startY y coord of the top left corner in the destination space
    * @param width destination width of image
    * @param height destination height of image
    """
    def fillRect(self, startX, startY, width, height):
        self.impl.fillRect(startX, startY, width, height)
    
    """*
    * Places text, at the specified start
    * coords, according to the current fillstyle.
    *
    * @param startX x coord of the top left corner in the destination space
    * @param startY y coord of the top left corner in the destination space
    * @param maxWidth maximum width of text
    """
    def fillText(self, text, startX, startY, maxWidth=None):
        self.impl.fillText(text, startX, startY, maxWidth)
    
    
    """*
    * Returns the height in pixels of the canvas.
    *
    * @return returns the height in pixels of the canvas
    """
    def getCoordHeight(self):
        return self.coordHeight
    
    
    """*
    *
    * Returns the width in pixels of the canvas.
    *
    * @return returns the width in pixels of the canvas
    """
    def getCoordWidth(self):
        return self.coordWidth
    
    
    """*
    * See self.setter method for a fully detailed description.
    *
    * @return
    * @see GWTCanvas#setGlobalAlpha(double)
    """
    def getGlobalAlpha(self):
        return self.impl.getGlobalAlpha()
    
    
    """*
    * See self.setter method for a fully detailed description.
    *
    * @return
    * @see GWTCanvas#setGlobalCompositeOperation(String)
    """
    def getGlobalCompositeOperation(self):
        return self.impl.getGlobalCompositeOperation()
    
    
    """*
    * See self.setter method for a fully detailed description.
    *
    * @return
    * @see GWTCanvas#setLineCap(String)
    """
    def getLineCap(self):
        return self.impl.getLineCap()
    
    
    """*
    * See self.setter method for a fully detailed description.
    *
    * @return
    * @see GWTCanvas#setLineJoin(String)
    """
    def getLineJoin(self):
        return self.impl.getLineJoin()
    
    
    """*
    * See self.setter method for a fully detailed description.
    *
    * @return
    * @see GWTCanvas#setLineWidth(double)
    """
    def getLineWidth(self):
        return self.impl.getLineWidth()
    
    
    """*
    * See self.setter method for a fully detailed description.
    *
    * @return
    * @see GWTCanvas#setMiterLimit(double)
    """
    def getMiterLimit(self):
        return self.impl.getMiterLimit()
    
    
    """*
    * Adds a line from the last point in the current path to the point defined by
    * x and y.
    *
    * @param x x coord of point
    * @param y y coord of point
    """
    def lineTo(self, x, y):
        self.impl.lineTo(x, y)
    
    
    """*
    * Makes the last point in the current path be <b>(x,y)</b>.
    *
    * @param x x coord of point
    * @param y y coord of point
    """
    def moveTo(self, x, y):
        self.impl.moveTo(x, y)
    
    
    """*
    * Does nothing if the context has an empty path. Otherwise it connects the
    * last point in the path to the given point <b>(x, y)</b> using a quadratic
    * Bezier curve with control point <b>(cpx, cpy)</b>, and then adds the given
    * point <b>(x, y)</b> to the path.
    *
    * @param cpx x coord of the control point
    * @param cpy y coord of the control point
    * @param x x coord of the point
    * @param y y coord of the point
    """
    def quadraticCurveTo(self, cpx, cpy, x, y):
        self.impl.quadraticCurveTo(cpx, cpy, x, y)
    
    
    """*
    * Adds a rectangle to the current path, and closes the path.
    *
    * @param startX x coord of the top left corner of the rectangle
    * @param startY y coord of the top left corner of the rectangle
    * @param width the width of the rectangle
    * @param height the height of the rectangle
    """
    def rect(self, startX, startY, width, height):
        self.impl.rect(startX, startY, width, height)
    
    
    """*
    * Convenience function for resizing the canvas with consistent coordinate and
    * screen pixel spaces. Equivalent to doing:
    *
    * <pre><code>
    * canvas.setCoordSize(width, height)
    * canvas.setPixelHeight(height)
    * canvas.setPixelWidth(width)
    * </code></pre>
    *
    * @param width
    * @param height
    """
    def resize(self, width, height):
        self.setCoordSize(width, height)
        self.setPixelHeight(height)
        self.setPixelWidth(width)
    
    
    """*
    * Restores the last saved context from the context stack.
    """
    def restoreContext(self):
        self.impl.restoreContext()
    
    
    """*
    * Adds a rotation of the specified angle to the current transform.
    *
    * @param angle the angle to rotate by, <b>in radians</b>
    """
    def rotate(self, angle):
        self.impl.rotate(angle)
    
    
    """*
    * Saves the current context to the context stack.
    """
    def saveContext(self):
        self.impl.saveContext()
    
    
    """*
    * Adds a scale transformation to the current transformation matrix.
    *
    * @param x ratio that we must scale in the X direction
    * @param y ratio that we must scale in the Y direction
    """
    def scale(self, x, y):
        self.impl.scale(x, y)
    
    
    """*
    * Sets the background color of the canvas element.
    *
    * @param color the background color.
    """
    def setBackgroundColor(self, color):
        self.impl.setBackgroundColor(self.getCanvasElement(), str(color))
    
    
    """*
    * Sets the coordinate height of the Canvas.
    * <p>
    * This will erase the canvas contents!
    * </p>
    *
    * @param height the size of the y component of the coordinate space
    """
    def setCoordHeight(self, height):
        self.impl.setCoordHeight(self.getCanvasElement(), height)
        self.coordHeight = height
    
    
    """*
    * Sets the coordinate space of the Canvas.
    * <p>
    * This will erase the canvas contents!
    * </p>
    *
    * @param width the size of the x component of the coordinate space
    * @param height the size of the y component of the coordinate space
    """
    def setCoordSize(self, width, height):
        self.setCoordWidth(width)
        self.setCoordHeight(height)
    
    
    """*
    * Sets the coordinate width of the Canvas.
    * <p>
    * This will erase the canvas contents!
    * </p>
    *
    * @param width the size of the x component of the coordinate space
    """
    def setCoordWidth(self, width):
        self.impl.setCoordWidth(self.getCanvasElement(), width)
        self.coordWidth = width
    
    
    """*
    * Set the current Fill Style to the specified color gradient.
    *
    * @param grad {@link CanvasGradient}
    """
    def setFillStyle(self, grad):
        self.impl.setFillStyle(grad)
    
    
    """*
    * Set the global transparency to the specified alpha.
    *
    * @param alpha alpha value
    """
    def setGlobalAlpha(self, alpha):
        self.impl.setGlobalAlpha(alpha)
    
    
    """*
    * Determines how the canvas is displayed relative to any background content.
    * The string identifies the desired compositing mode. If you do not self.set this
    * value explicitly, the canvas uses the <code>GWTCanvas.SOURCE_OVER</code>
    * compositing mode.
    * <p>
    * The valid compositing operators are:
    * <ul>
    * <li><code>GWTCanvas.SOURCE_OVER</code>
    * <li><code>GWTCanvas.DESTINATION_OVER</code>
    * </ul>
    * <p>
    *
    * @param globalCompositeOperation
    """
    def setGlobalCompositeOperation(self, globalCompositeOperation):
        self.impl.setGlobalCompositeOperation(globalCompositeOperation)
    
    
    """*
    * A string value that determines the end style used when drawing a line.
    * Specify the string <code>GWTCanvas.BUTT</code> for a flat edge that is
    * perpendicular to the line itself, <code>GWTCanvas.ROUND</code> for round
    * endpoints, or <code>GWTCanvas.SQUARE</code> for square endpoints. If you do
    * not self.set this value explicitly, the canvas uses the
    * <code>GWTCanvas.BUTT</code> line cap style.
    *
    * @param lineCap
    """
    def setLineCap(self, lineCap):
        self.impl.setLineCap(lineCap)
    
    
    """*
    * A string value that determines the join style between lines. Specify the
    * string <code>GWTCanvas.ROUND</code> for round joins,
    * <code>GWTCanvas.BEVEL</code> for beveled joins, or
    * <code>GWTCanvas.MITER</code> for miter joins. If you do not self.set this value
    * explicitly, the canvas uses the <code>GWTCanvas.MITER</code> line join
    * style.
    *
    * @param lineJoin
    """
    def setLineJoin(self, lineJoin):
        self.impl.setLineJoin(lineJoin)
    
    
    """*
    * Sets the current context's linewidth. Line width is the thickness of a
    * stroked line.
    *
    * @param width the width of the canvas
    """
    def setLineWidth(self, width):
        self.impl.setLineWidth(width)
    
    
    """*
    * A double value with the miter limit. You use this property to specify
    * how the canvas draws the juncture between connected line segments. If the
    * line join is self.set to <code>GWTCanvas.MITER</code>, the canvas uses the miter
    * limit to determine whether the lines should be joined with a bevel instead
    * of a miter. The canvas divides the length of the miter by the line width.
    * If the result is greater than the miter limit, the style is converted to a
    * bevel.
    *
    * @param miterLimit
    """
    def setMiterLimit(self, miterLimit):
        self.impl.setMiterLimit(miterLimit)
    
    
    """*
    * Sets the CSS height of the canvas in pixels.
    *
    * @param height the height of the canvas in pixels
    """
    def setPixelHeight(self, height):
        self.impl.setPixelHeight(self.getCanvasElement(), height)
    
    
    """*
    * Sets the CSS width in pixels for the canvas.
    *
    * @param width width of the canvas in pixels
    """
    def setPixelWidth(self, width):
        self.impl.setPixelWidth(self.getCanvasElement(), width)
    
    
    """*
    * Set the current Stroke Style to the specified color gradient.
    *
    * @param grad {@link CanvasGradient}
    """
    def setStrokeStyle(self, grad):
        self.impl.setStrokeStyle(grad)
    
    
    """*
    * Strokes the current path according to the current stroke style.
    """
    def stroke(self):
        self.impl.stroke()
    
    
    """*
    * Strokes a rectangle defined by the supplied arguments.
    *
    * @param startX x coord of the top left corner
    * @param startY y coord of the top left corner
    * @param width width of the rectangle
    * @param height height of the rectangle
    """
    def strokeRect(self, startX, startY, width, height):
        self.impl.strokeRect(startX, startY, width, height)
    
    
    """*
    * <code>The transform(m11, m12, m21, m22, dx, dy)</code> method must multiply
    * the current transformation matrix with the input matrix. Input described
    * by:
    *
    * <pre>
    * m11   m21   dx
    * m12   m22   dy
    * 0      0     1
    *</pre>
    *
    * @param m11 top left cell of 2x2 rotation matrix
    * @param m12 top right cell of 2x2 rotation matrix
    * @param m21 bottom left cell of 2x2 rotation matrix
    * @param m22 bottom right cell of 2x2 rotation matrix
    * @param dx Translation in X direction
    * @param dy Translation in Y direction
    """
    def transform(self, m11, m12, m21, m22, dx, dy):
        self.impl.transform(m11, m12, m21, m22, dx, dy)
    
    
    """*
    * Applies a translation (linear shift) by x in the horizontal and by y in the
    * vertical.
    *
    * @param x amount to shift in the x direction
    * @param y amount to shift in the y direction
    """
    def translate(self, x, y):
        self.impl.translate(x, y)
    


