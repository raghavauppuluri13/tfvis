# tfvis

Simple TF visualization

## Quick start

```bash

# only numpy and meshcat dependencies
pip install "tfvis@git+https://github.com/raghavauppuluri13/tfvis.git"

# if you want to run the examples, adds argparse and gtsam
pip install "tfvis[examples]@git+https://github.com/raghavauppuluri13/tfvis.git"
```

## Usage

### Playback
```python
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
```

### Realtime
```python
"""Play an animation of EEF poses using meshcat."""
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
R_start = gtsam.Rot3()  # Initialize the rotation, e.g., the default constructor for the identity rotation
R_end = gtsam.Rot3.Rodrigues(0.6, 0.2, 0.3)  # Example using Rodrigues' formula
t_start = gtsam.Point3(0, 0, 0)  # Initialize the translation
t_end = gtsam.Point3(0.5, 0.5, 0.5)  # Initialize the translation

# Create a Pose3 object
X_BE_start = gtsam.Pose3(R_start, t_start)
X_BE_end = gtsam.Pose3(R_end, t_end)

rtv.set_frame_tf("EEF", X_BE_start.matrix())
for t in np.linspace(0,1,1000):
    X_BE_at_t = X_BE_start.slerp(t, X_BE_end)
    rtv.set_frame_tf("EEF", X_BE_at_t.matrix())
    time.sleep(0.01)
```
