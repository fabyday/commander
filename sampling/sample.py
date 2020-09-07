import igl


def downsample(vertex, face, max_face):
    _, U, G, J, I = igl.decimate(vertex, face, max_face)
    return U, G


class DownSampleGenerator(object):
    def __init__(self, max_face):
        self.max_face = max_face

    def __call__(self, vertex, face):
        return downsample(vertex, face, self.max_face)