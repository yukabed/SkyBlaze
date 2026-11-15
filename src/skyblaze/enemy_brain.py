# SkyBlaze - the enemy 'brain' shared by all intelligent enemies (PlayerModel)
# (lines 146-315 of SkyBlaze_test_1.py, copied unchanged)

from constants import NB, SAMPLE
from helpers import clamp


# ---------------------------------------------------------------------------
# The enemy "brain": learns from the player's behaviour
# ---------------------------------------------------------------------------
class PlayerModel:
    """Everything the enemies have learned about the player.

    * pos_heat  - where the player likes to stand
    * shot_heat - from which lanes he shoots
    * kill_heat - from which lanes he actually scores kills
    * counts    - an order-2 Markov model of his actions (move left / right /
                  idle, fire) used to predict where he will be next
    All statistics decay over time (half-life = difficulty "memory"), so the
    enemies keep adapting if the player changes his tactics.
    """

    def __init__(self):
        self.x_lo = -300.0
        self.span = 600.0
        self.decay = 0.99
        self.reset()

    def reset(self):
        self.pos_heat = [0.0] * NB
        self.shot_heat = [0.0] * NB
        self.kill_heat = [0.0] * NB
        self.counts = [[0.0] * 6 for _ in range(36)]
        self.hist = []
        self.accuracy = 0.0
        self.samples = 0
        self.camp_x = 0.0
        self.camp = 0.0
        self.shot_conc = 0.0
        self.read = 0.0

    def configure(self, x_lo, x_hi):
        self.x_lo = x_lo
        self.span = x_hi - x_lo

    def begin_round(self, half_life, keep):
        """New round: keep part of the old knowledge, forget the rest."""
        self.decay = 0.5 ** (SAMPLE / half_life)
        self.pos_heat = [v * keep for v in self.pos_heat]
        self.shot_heat = [v * keep for v in self.shot_heat]
        self.kill_heat = [v * keep for v in self.kill_heat]
        self.counts = [[v * keep for v in row] for row in self.counts]
        self.samples = int(self.samples * keep)
        self.hist = []
        self.camp = self.shot_conc = self.read = 0.0

    # -- lanes -------------------------------------------------------------
    def bin_of(self, x):
        b = int((x - self.x_lo) / self.span * NB)
        return 0 if b < 0 else NB - 1 if b >= NB else b

    def x_of_bin(self, b):
        return self.x_lo + (b + 0.5) * self.span / NB

    @staticmethod
    def _bump(arr, b, amount):
        arr[b] += amount
        if b > 0:
            arr[b - 1] += amount * 0.5
        if b < NB - 1:
            arr[b + 1] += amount * 0.5

    # -- learning ----------------------------------------------------------
    def observe(self, x, move, fired):
        """Called every SAMPLE seconds. move: 0 idle, 1 left, 2 right."""
        d = self.decay
        self.pos_heat = [v * d for v in self.pos_heat]
        self.shot_heat = [v * d for v in self.shot_heat]
        self.kill_heat = [v * d for v in self.kill_heat]
        self.counts = [[v * d for v in row] for row in self.counts]
        self._bump(self.pos_heat, self.bin_of(x), 1.0)

        token = move * 2 + (1 if fired else 0)
        if len(self.hist) >= 2:
            row = self.counts[self.hist[-2] * 6 + self.hist[-1]]
            best = max(range(6), key=row.__getitem__)
            if row[best] >= 0.5:        # the model had an opinion: score it
                hit = 1.0 if best == token else 0.0
                self.accuracy += 0.08 * (hit - self.accuracy)
            row[token] += 1.0
        self.hist.append(token)
        if len(self.hist) > 2:
            del self.hist[0]
        self.samples += 1

        self.camp, ci = self._concentration(self.pos_heat, 30.0)
        self.camp_x = self.x_of_bin(ci)
        self.shot_conc, _ = self._concentration(self.shot_heat, 12.0)
        self.read = max(self.predictability(), self.camp, self.shot_conc)

    def record_shot(self, x):
        self._bump(self.shot_heat, self.bin_of(x), 1.0)

    def record_kill(self, x):
        self._bump(self.kill_heat, self.bin_of(x), 1.0)

    # -- knowledge ---------------------------------------------------------
    @staticmethod
    def _concentration(arr, evidence):
        """How strongly the heat is piled into one spot (0..1) and where."""
        total = sum(arr)
        if total <= 1e-6:
            return 0.0, NB // 2
        best, best_i = -1.0, 0
        for i in range(NB):
            s = arr[i]
            if i > 0:
                s += arr[i - 1]
            if i < NB - 1:
                s += arr[i + 1]
            if s > best:
                best, best_i = s, i
        base = 3.0 / NB
        c = clamp((best / total - base) / (0.6 - base), 0.0, 1.0)
        return c * min(1.0, total / evidence), best_i

    def predictability(self):
        """0..1 - how well the Markov model can foresee the player's actions."""
        return clamp((self.accuracy - 0.30) / 0.50, 0.0, 1.0) * min(1.0, self.samples / 40.0)

    @staticmethod
    def _fam(arr, b, evidence):
        total = sum(arr)
        if total <= 1e-6:
            return 0.0
        share = arr[b] / total * NB           # 1.0 = perfectly even spread
        return clamp((share - 1.5) / 2.5, 0.0, 1.0) * min(1.0, total / evidence)

    def lane_familiarity(self, x):
        """0..1 - how well the enemies know a bullet coming from lane x."""
        b = self.bin_of(x)
        return max(0.85 * self._fam(self.shot_heat, b, 12.0),
                   self._fam(self.kill_heat, b, 6.0))

    def predict_x(self, x, steps, speed):
        """Roll the Markov chain forward and return the player's likely x."""
        if self.samples < 20 or len(self.hist) < 2:
            return x
        a, b = self.hist[-2], self.hist[-1]
        for _ in range(steps):
            row = self.counts[a * 6 + b]
            best = max(range(6), key=row.__getitem__)
            if row[best] < 0.5:
                break
            m = best // 2
            if m == 1:
                x -= speed * SAMPLE
            elif m == 2:
                x += speed * SAMPLE
            a, b = b, best
        return clamp(x, self.x_lo, self.x_lo + self.span)

    def spawn_weights(self, avoid):
        """Lane weights for new enemies: they avoid the lanes the player favours."""
        tot_p, tot_k = sum(self.pos_heat), sum(self.kill_heat)
        max_p, max_k = max(self.pos_heat), max(self.kill_heat)
        ep = min(1.0, tot_p / 30.0)
        ek = min(1.0, tot_k / 6.0)
        weights = []
        for i in range(NB):
            h = 0.0
            if max_p > 1e-9:
                h += 0.4 * ep * self.pos_heat[i] / max_p
            if max_k > 1e-9:
                h += 0.6 * ek * self.kill_heat[i] / max_k
            weights.append(max(0.08, 1.0 - avoid * h))
        return weights
