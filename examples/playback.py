"""Play an animation of EEF poses using meshcat."""
from tfvis.visualizer import PlaybackVisualizer
import numpy as np
import argparse
import gtsam

def to_pose(xyzrpy):
    x, y, z, r, p, w = xyzrpy
    R = gtsam.Rot3.RzRyRx(r, p, w)
    return gtsam.Pose3(R, gtsam.Point3(x, y, z))

def read_ee_poses(ee_poses_fn):
    """
    Read EE poses from a file. One pose per line. Order: pose_id, x, y, z, roll, pitch, yaw
    :param ee_poses_fn: Path to file of poses.
    :return: List of gtsam.Pose3.
    """
    ee_poses = []
    with open(ee_poses_fn, "r") as f:
        for line in f:
            ixyzrpw = [float(a) for a in line.split()]
            ee_poses.append(to_pose(ixyzrpw[1:]))
    return ee_poses

argparser = argparse.ArgumentParser()
argparser.add_argument("--poses-path", type=str, required=True)
args = argparser.parse_args()


X_BEs = read_ee_poses(args.poses_path)
pbvis = PlaybackVisualizer()

pbvis.add_frame("BASE")
pbvis.set_frame_tf("BASE", np.eye(4))
pbvis.add_frame("EEF", "BASE")

for X_BE in X_BEs:
    pbvis.set_frame_tf("EEF", X_BE.matrix())
pbvis.push()
pbvis.keep_alive()
