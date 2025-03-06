import math

class Vector:
    POS_Y_UNIT = [0, -1]
    POS_X_UNIT = [1, 0]
    POS_X_POS_Y_DIAG_UNIT = [1, 1]
    
    @classmethod
    def calculate_angle(cls, v1, v2) -> float:
        dot_product = v1[0] * v2[0] + v1[1] * v2[1]
        magnitude_v1 = math.sqrt(v1[0]**2 + v1[1]**2)
        magnitude_v2 = math.sqrt(v2[0]**2 + v2[1]**2)
        cos_theta = dot_product / (magnitude_v1 * magnitude_v2)
        angle = math.acos(cos_theta)
        return math.degrees(angle)

    @classmethod
    def calculate_signed_angle(cls, v1, v2) -> float:
        dot_product = v1[0] * v2[0] + v1[1] * v2[1]
        magnitude_v1 = math.sqrt(v1[0]**2 + v1[1]**2)
        magnitude_v2 = math.sqrt(v2[0]**2 + v2[1]**2)
        cos_theta = dot_product / (magnitude_v1 * magnitude_v2)

        angle = math.acos(max(-1, min(1, cos_theta)))
        
        cross_product = v1[0] * v2[1] - v1[1] * v2[0]
        if cross_product < 0:
            angle = -angle

        return math.degrees(angle)

    
    @classmethod
    def unit_vector(cls, v) -> list[float, float]:
        magnitude = math.sqrt(v[0]**2 + v[1]**2)
        return (v[0] / magnitude, v[1] / magnitude)