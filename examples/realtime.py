"""Visualize transforms in realtime"""
import time
from tfvis.visualizer import RealtimeVisualizer
import numpy as np
import argparse
import gtsam

rtv = RealtimeVisualizer()

rtv.add_frame("BASE")
rtv.set_frame_tf("BASE", np.eye(4))
rtv.add_frame("EEF", "BASE")

X_BE = gtsam.Pose3()
R_start = gtsam.Rot3()
R_end = gtsam.Rot3.Rodrigues(0.6, 0.2, 0.3)
t_start = gtsam.Point3(0, 0, 0)
t_end = gtsam.Point3(0.5, 0.5, 0.5)
X_BE_start = gtsam.Pose3(R_start, t_start)
X_BE_end = gtsam.Pose3(R_end, t_end)

rtv.set_frame_tf("EEF", X_BE_start.matrix())
for t in np.linspace(0,1,1000):
    X_BE_at_t = X_BE_start.slerp(t, X_BE_end)
    rtv.set_frame_tf("EEF", X_BE_at_t.matrix())
    time.sleep(0.01)
