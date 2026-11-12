# SkyBlaze - player weapon (fire / reset bullet)
# (lines 903-921 of SkyBlaze_test_1.py, copied unchanged)

from sound import play_sound


class PlayerMixin:
    def fire_bullet(self):
        # Declare bullet "fire" only if it is ready
        if self.state != "playing" or self.bullet_state != "ready":
            return
        self.bullet_state = "fire"
        play_sound("laser.wav")                       # sound for windows/linux/mac
        self.bx = self.player_x
        self.by = self.player_y + 10
        self.shot_id += 1
        # What do the enemies know about shots from this lane? (before learning it)
        self.dodge_p = self.diff["dodge_max"] * self.model.lane_familiarity(self.bx)
        self.model.record_shot(self.bx)
        self.fired_flag = True
        self.bullet.setposition(self.bx, self.by)
        self.bullet.showturtle()

    def reset_bullet(self):
        self.bullet.hideturtle()
        self.bullet_state = "ready"
