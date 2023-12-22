import meshcat
from typing import Union
import meshcat.geometry as g
import time
import meshcat.transformations as tf
from meshcat.animation import Animation
import numpy as np
from tfvis.gui import SceneText
WORLD = "WORLD"

class TFGraph:
    def __init__(self):
        self.frames = {WORLD: WORLD}
    def add_frame(self, name: str, parent: str):
        assert WORLD not in name and name != WORLD, f"Frame name {name} is reserved, cannot have it in your name."
        assert WORLD in self.frames[parent], f"Parent frame {parent} is not attached to the world."
        self.frames[name] = self.frames[parent] + "/" + name
    def get_frame_path(self, name: str):
        assert name in self.frames, f"Frame {name} does not exist."
        return self.frames[name]

class TFAnimation:
    def __init__(self):
        self.vis = meshcat.Visualizer().open()
        self.anim = Animation()
        self.frame_i = 0
        self.graph = TFGraph()

    def add_frame(self, name: str, parent: Union[str, None] = WORLD):
        """
        Add a frame to the animation.
        :param name: Name of the frame.
        :param W_T_N: Pose of the frame in the parent frame.
        """
        self.graph.add_frame(name, parent)
        pth = self.graph.get_frame_path(name)
        self.vis[pth].set_object(g.triad(scale=1))
        self.vis[pth + '/frame_id'].set_object(SceneText(name))

    def set_frame_tf(self, name: str, P_T_N: np.ndarray):
        """
        Set the pose of a frame in the world frame.
        :param name: Name of the frame.
        :param P_T_N: Pose of the frame in the parent frame.
        """
        assert P_T_N.shape == (4, 4), f"Expected shape (4, 4), got {P_T_N.shape}"
        pth = self.graph.get_frame_path(name)
        with self.anim.at_frame(self.vis, self.frame_i) as frame:
            frame[pth].set_transform(P_T_N)
        self.frame_i += 1

    def push(self):
        """
        Push the animation to the meshcat server.
        """
        self.vis.set_animation(self.anim)
    def keep_alive(self):
        self.vis.wait()

class TFRealtimeVisualizer:
    def __init__(self):
        self.vis = meshcat.Visualizer().open()
        self.graph = TFGraph()

    def add_frame(self, name: str, parent: Union[str, None] = WORLD):
        """
        Add a frame to the animation.
        :param name: Name of the frame.
        :param W_T_N: Pose of the frame in the parent frame.
        """
        self.graph.add_frame(name, parent)
        pth = self.graph.get_frame_path(name)
        self.vis[pth].set_object(g.triad(scale=1))
        self.vis[pth + '/frame_id'].set_object(SceneText(name))

    def set_frame_tf(self, name: str, P_T_N: np.ndarray):
        """
        Set the pose of a frame in the world frame.
        :param name: Name of the frame.
        :param P_T_N: Pose of the frame in the parent frame.
        """
        assert P_T_N.shape == (4, 4), f"Expected shape (4, 4), got {P_T_N.shape}"
        pth = self.graph.get_frame_path(name)
        self.vis[pth].set_transform(W_T_N)
