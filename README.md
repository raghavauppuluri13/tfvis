# tfvis

Simple TF visualization

## Quick start

```bash

# only numpy and meshcat dependencies
pip install "tfvis@git+https://github.com/raghavauppuluri13/tfvis.git"

# if you want to run the examples, adds gtsam dependency
pip install "tfvis[examples]@git+https://github.com/raghavauppuluri13/tfvis.git"
```

## Usage

### Playback
```python
"""Playback EEF poses generated offline"""
from tfvis.visualizer import PlaybackVisualizer
import numpy as np
import gtsam

pbvis = PlaybackVisualizer()
pbvis.add_frame("BASE")
pbvis.set_frame_tf("BASE", np.eye(4))
pbvis.add_frame("EEF", "BASE")

R_start = gtsam.Rot3()
R_end = gtsam.Rot3.Rodrigues(0.6, 0.2, 0.3)
t_start = gtsam.Point3(0, 0, 0)
t_end = gtsam.Point3(0.5, 0.5, 0.5)
X_BE_start = gtsam.Pose3(R_start, t_start)
X_BE_end = gtsam.Pose3(R_end, t_end)
X_BEs = [X_BE_start.slerp(t, X_BE_end) for t in np.linspace(0,1,1000)]

for X_BE in X_BEs:
    pbvis.set_frame_tf("EEF", X_BE.matrix())
pbvis.push()
pbvis.keep_alive()
```

### Realtime
```python
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
```
