class ConstantVelocityModel:
    """
    A model that describes the motion of an object with constant
    velocity.
    """

    def __init__(self):
        self._velocity = None
        self._intercept = None

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        self._velocity = value

    @property
    def intercept(self):
        return self._intercept

    @intercept.setter
    def intercept(self, value):
        self._intercept = value

    def find_velocity_from_points(self, p1, p2, t1, t2):
        velocity = (p2 - p1) / (t2 - t1)
        self.velocity = velocity
        return velocity

    def find_intercept_from_point(self, p, t=0):
        """
        Returns the position-intercept for the current object. The velocity
        of the object must be known.
        """
        if not self.velocity:
            raise ValueError(
                "self.velocity is not defined, try using the method find_velocity_from_points."
            )
        if t == 0:
            self.intercept = p
            return self.intercept
        self.intercept = p - self.velocity * t
        return self.intercept

    def solve(self, p1, p2, t1, t2):
        self.find_velocity_from_points(p1, p2, t1, t2)
        self.find_intercept_from_point(self, p1, t1)
        return self.velocity, self.intercept

    def position(self, t):
        """
        Returns the position of an object at a given time.
        """
        return self.velocity * t + self.intercept
