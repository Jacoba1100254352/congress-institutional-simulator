# Mechanism Ablation Summary

This report compares selected mechanism bundles with nearby ablations across the ablation campaign's broad and adversarial cases. Positive directional/productivity/revision-moderation deltas favor the full mechanism. Positive low-public-support reduction means fewer weakly supported enactments. Positive admin-cost added means the full mechanism is procedurally heavier.

| Family | Full scenario | Comparison | Δ directional | Δ productivity | Δ revision moderation | Low-public-support reduction | Admin cost added | Interpretation |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Policy tournament | `simple-majority-alternatives-pairwise` | `simple-majority` | 0.056 | 0.230 | 0.266 | 0.217 | 0.219 | helps, but with visible process cost |
| Risk routing | `risk-routed-majority` | `simple-majority` | 0.035 | 0.224 | 0.021 | -0.011 | 0.101 | helps, but with visible process cost |
| Risk routing | `risk-routed-majority` | `risk-routed-no-citizen-majority` | -0.002 | -0.000 | 0.000 | 0.001 | 0.008 | mixed or small effect |
| Anti-capture | `anti-capture-majority-bundle` | `simple-majority` | 0.013 | -0.009 | 0.002 | 0.067 | -0.005 | mixed or small effect |
| Anti-capture | `anti-capture-majority-bundle` | `public-interest-majority` | 0.024 | 0.061 | 0.000 | 0.043 | 0.005 | helps under this ablation screen |
| Affected groups | `compensation-majority` | `simple-majority` | -0.003 | 0.000 | 0.000 | -0.000 | 0.000 | mixed or small effect |
| Affected groups | `affected-consent-majority` | `compensation-majority` | -0.000 | -0.008 | 0.000 | 0.012 | -0.006 | mixed or small effect |
| Package bargaining | `multidimensional-package-majority` | `simple-majority` | -0.024 | 0.022 | -0.005 | -0.003 | 0.105 | component hurts this value profile |
| Package bargaining | `multidimensional-package-majority` | `package-bargaining-majority` | -0.015 | 0.013 | -0.002 | 0.004 | 0.065 | mixed or small effect |
| Reversibility | `law-registry-majority` | `simple-majority` | -0.009 | 0.029 | -0.009 | -0.034 | 0.044 | mixed or small effect |
