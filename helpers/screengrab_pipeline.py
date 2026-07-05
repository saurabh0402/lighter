from gi.repository import Gst
import gi
import numpy as np

gi.require_version('Gst', '1.0')
Gst.init(None)

def build_pipeline(fd, node_id):
    pipeline_str = (
        f"pipewiresrc fd={fd} path={node_id} ! "
        "videoconvert ! video/x-raw,format=RGB ! "
        "appsink name=sink max-buffers=1 drop=true"
    )
    pipeline = Gst.parse_launch(pipeline_str)
    appsink = pipeline.get_by_name('sink')
    pipeline.set_state(Gst.State.PLAYING)
    return pipeline, appsink

def get_screengrab(appsink):
    sample = appsink.emit('pull-sample')
    if sample is None:
        return None
    buf = sample.get_buffer()
    caps = sample.get_caps()
    width = caps.get_structure(0).get_value('width')
    height = caps.get_structure(0).get_value('height')

    success, mapinfo = buf.map(Gst.MapFlags.READ)
    if not success:
        return None
    arr = np.frombuffer(mapinfo.data, dtype=np.uint8).reshape((height, width, 3))
    buf.unmap(mapinfo)

    return arr
