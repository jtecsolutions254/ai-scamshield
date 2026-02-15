import math

class RiskScorer:
    def __init__(self, alpha=1.2, beta=1.0, gamma=1.4, bias=0.0):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.bias = bias

    @staticmethod
    def _logit(p: float) -> float:
        eps = 1e-6
        p = min(1 - eps, max(eps, p))
        return math.log(p / (1 - p))

    @staticmethod
    def _sigmoid(x: float) -> float:
        return 1.0 / (1.0 + math.exp(-x))

    def score(self, p_ml: float, h: float, t: float):
        x = (self.alpha * self._logit(p_ml)) + (self.beta * h) + (self.gamma * t) + self.bias
        s = int(round(100 * self._sigmoid(x)))
        s = max(0, min(100, s))

        if s <= 24:
            level = "LOW"
        elif s <= 49:
            level = "MEDIUM"
        elif s <= 74:
            level = "HIGH"
        else:
            level = "CRITICAL"
        return s, level
