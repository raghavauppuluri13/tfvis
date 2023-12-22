"""From https://github.com/meshcat-dev/meshcat-python/blob/master/src/meshcat/geometry.py"""
import meshcat.geometry as g
import numpy as np

class Plane(g.Geometry):

    def __init__(self, width=1, height=1, widthSegments=1, heightSegments=1):
        super(Plane, self).__init__()
        self.width = width
        self.height = height
        self.widthSegments = widthSegments
        self.heightSegments = heightSegments

    def lower(self, object_data):
        return {
            u"uuid": self.uuid,
            u"type": u"PlaneGeometry",
            u"width": self.width,
            u"height": self.height,
            u"widthSegments": self.widthSegments,
            u"heightSegments": self.heightSegments,
        }

class TextTexture(g.Texture):
    def __init__(self, text, font_size=30, font_face='sans-serif'):
        super(TextTexture, self).__init__()
        self.text = text
        # font_size will be passed to the JS side as is; however if the
        # text width exceeds canvas width, font_size will be reduced.
        self.font_size = font_size
        self.font_face = font_face

    def lower(self, object_data):
        return {
            u"uuid": self.uuid,
            u"type": u"_text",
            u"text": self.text,
            u"font_size": self.font_size,
            u"font_face": self.font_face,
        }

def SceneText(text, width=0.5, height=0.5, **kwargs):
    return g.Mesh(
        Plane(width=width,height=height),
        g.MeshPhongMaterial(map=TextTexture(text,**kwargs),transparent=True,
            needsUpdate=True)
        )


def triad(name, scale=1.0):
    """
    A visual representation of the origin of a coordinate system, drawn as three
    lines in red, green, and blue along the x, y, and z axes. The `scale` parameter
    controls the length of the three lines.

    Returns an `Object` which can be passed to `set_object()`
    """
    return g.LineSegments(
        g.PointsGeometry(position=np.array([
            [0, 0, 0], [scale, 0, 0],
            [0, 0, 0], [0, scale, 0],
            [0, 0, 0], [0, 0, scale]]).astype(np.float32).T,
            color=np.array([
            [1, 0, 0], [1, 0.6, 0],
            [0, 1, 0], [0.6, 1, 0],
            [0, 0, 1], [0, 0.6, 1]]).astype(np.float32).T
        ),
        )
