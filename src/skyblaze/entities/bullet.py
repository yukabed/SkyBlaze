"""The player's bullet."""

import turtle

from .. import config


class Bullet(turtle.Turtle):
    """The single bullet the player can have in flight at any time."""

    def __init__(self):
        super().__init__()
        self.color(config.BULLET_COLOR)
        self.shape(config.BULLET_SHAPE)
        self.penup()
        self.speed(0)
        self.setheading(config.UP_HEADING)
        self.shapesize(*config.BULLET_SIZE)
        self.hideturtle()
        self.firing = False

    def launch(self, x, y):
        self.firing = True
        self.setposition(x, y)
        self.showturtle()

    def deactivate(self):
        """Hide the bullet and allow the next shot."""
        self.hideturtle()
        self.firing = False

    def park(self):
        """Move the bullet off-screen below the arena."""
        self.setposition(*config.BULLET_PARKING_POSITION)

    def advance(self):
        """Move up one step and retire the bullet once it leaves the arena."""
        if self.firing:
            self.sety(self.ycor() + config.BULLET_SPEED)
        if self.ycor() > config.BULLET_TOP_Y:
            self.deactivate()
