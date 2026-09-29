"""
Unit tests for TrustGuard AI backend response utils, label normalization, and score semantics.
"""
import sys
import unittest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend.utils.response_utils import (
    clamp_score,
    authenticity_classification,
    normalize_fake_probability
)


class TestBackendUtils(unittest.TestCase):

    def test_score_clamping(self):
        self.assertEqual(clamp_score(-15), 0.0)
        self.assertEqual(clamp_score(0), 0.0)
        self.assertEqual(clamp_score(45.5), 45.5)
        self.assertEqual(clamp_score(100), 100.0)
        self.assertEqual(clamp_score(150), 100.0)
        self.assertEqual(clamp_score(None), 0.0)
        self.assertEqual(clamp_score("invalid"), 0.0)

    def test_score_classification_semantics(self):
        # <= 30 -> LIKELY_GENUINE
        c5 = authenticity_classification(5.0)
        self.assertEqual(c5["classification"], "LIKELY_GENUINE")
        self.assertEqual(c5["status"], "safe")
        self.assertIn("GENUINE", c5["label"])

        c30 = authenticity_classification(30.0)
        self.assertEqual(c30["classification"], "LIKELY_GENUINE")

        # < 70 -> UNCERTAIN
        c50 = authenticity_classification(50.0)
        self.assertEqual(c50["classification"], "UNCERTAIN")
        self.assertEqual(c50["status"], "warning")

        c69 = authenticity_classification(69.9)
        self.assertEqual(c69["classification"], "UNCERTAIN")

        # >= 70 -> LIKELY_FAKE
        c70 = authenticity_classification(70.0)
        self.assertEqual(c70["classification"], "LIKELY_FAKE")
        self.assertEqual(c70["status"], "danger")

        c95 = authenticity_classification(95.0)
        self.assertEqual(c95["classification"], "LIKELY_FAKE")
        self.assertEqual(c95["status"], "danger")

    def test_authenticity_conversion(self):
        fake_prob_10 = 10.0
        authenticity_10 = clamp_score(100.0 - fake_prob_10)
        self.assertEqual(authenticity_10, 90.0)

        fake_prob_80 = 80.0
        authenticity_80 = clamp_score(100.0 - fake_prob_80)
        self.assertEqual(authenticity_80, 20.0)

    def test_model_label_normalization_real0_fake1(self):
        # Case A: 0 = Real, 1 = Fake
        id2label = {0: "Real", 1: "Fake"}
        
        # 90% Real, 10% Fake => fakeProbability = 10%
        probs1 = {0: 0.9, 1: 0.1}
        fake_prob1 = normalize_fake_probability(probs1, id2label)
        self.assertEqual(fake_prob1, 10.0)

        # 20% Real, 80% Fake => fakeProbability = 80%
        probs2 = {0: 0.2, 1: 0.8}
        fake_prob2 = normalize_fake_probability(probs2, id2label)
        self.assertEqual(fake_prob2, 80.0)

    def test_model_label_normalization_fake0_real1(self):
        # Case B: 0 = Fake, 1 = Real
        id2label = {0: "Fake", 1: "Real"}

        # 95% Fake, 5% Real => fakeProbability = 95%
        probs1 = {0: 0.95, 1: 0.05}
        fake_prob1 = normalize_fake_probability(probs1, id2label)
        self.assertEqual(fake_prob1, 95.0)

        # 10% Fake, 90% Real => fakeProbability = 10%
        probs2 = {0: 0.10, 1: 0.90}
        fake_prob2 = normalize_fake_probability(probs2, id2label)
        self.assertEqual(fake_prob2, 10.0)


if __name__ == "__main__":
    unittest.main()
