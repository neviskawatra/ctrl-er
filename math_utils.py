import math

class Vector:
    @classmethod
    def calculate_angle(cls, v1, v2):
        dot_product = v1[0] * v2[0] + v1[1] * v2[1]
        magnitude_v1 = math.sqrt(v1[0]**2 + v1[1]**2)
        magnitude_v2 = math.sqrt(v2[0]**2 + v2[1]**2)
        cos_theta = dot_product / (magnitude_v1 * magnitude_v2)
        angle = math.acos(cos_theta)
        return math.degrees(angle)
    
    @classmethod
    def unit_vector(cls, v):
        magnitude = math.sqrt(v[0]**2 + v[1]**2)
        return (v[0] / magnitude, v[1] / magnitude)