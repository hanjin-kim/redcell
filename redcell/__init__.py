"""redcell — adversarial strategy scenario generator.

Given a strategy and a single worry, redcell:
  1. expands the worry into N distinct adversary scenarios across axes
     (competitor action, customer reaction, channel, regulatory, macro,
     internal execution),
  2. runs each as an independent linear simulation (no statistical
     M-trial averaging, no matched counterfactual — each scenario is one
     conditional plausible future),
  3. analyzes each trajectory honestly (axis-aligned, trace-grounded), and
  4. renders a scenario-card brief with workshop diligence questions.

This is a *pre-workshop thinking aid* — a hypothesis generator, NOT a
statistical estimator or a parameter-calibrated forecast.
"""

__version__ = "0.1.0"
