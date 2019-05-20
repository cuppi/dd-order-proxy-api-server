from math import sin, cos, sqrt, atan2, radians


class MathTool:
    @staticmethod
    def distance_between_location(l1, l2):
        # approximate radius of earth in km
        R = 6373.0
        lat1 = l1[0]
        lng1 = l1[1]
        lat2 = l2[0]
        lng2 = l2[1]

        dlng = lng2 - lng1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlng / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c
