from math import cos, sin
import numpy

def makeRotationZ(angle):
        radian = angle * numpy.pi / 180.0
        c = cos(radian)
        s = sin(radian)
        return numpy.array([
                            [c, -s, 0, 0],
                            [s,  c, 0, 0],
                            [0,  0, 1, 0], 
                            [0,  0, 0, 1]
                            ]).astype(float)


def makeRotation(angle, axis =(1,1,1)):
        radian = angle * numpy.pi / 180.0
        c = cos(radian)
        s = sin(radian)
        u =1-c
        ux,uy,uz = axis[0],axis[1],axis[2]

        # make the axis vector unit
        d = numpy.sqrt(numpy.square(ux)+numpy.square(uy)+numpy.square(uz))
        ax = ux/d
        ay = uy/d
        az = uz/d

        # for latter use in the mat
        ax2 = numpy.square(ax)
        ay2 = numpy.square(ay)
        az2 = numpy.square(az)
        return numpy.array([
                        [u*ax2+c,        u*ax*ay-s*az,   u*ax*az+s*ay,    0],
                        [u*ax*ay+s*az,   u*ay2 + c,      u*ay*az-s*ax,    0],
                        [u*ax*az-s*ay,   u*ay*az+s*ax,   u*az2+c,         0], 
                        [0,              0,              0,               1]
                            ]
                            ).astype(float)



