import igl


def downsample(vertex, face, max):
    U, G, J, I = igl.decimate(vertex, face, max)
    return U, G