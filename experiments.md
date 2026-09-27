# Part 2 experiments



| Run | Start | Step | Budget | Score | Attempts | Seconds | First non-zero | Best reached at | Notes |
|---|---|---|---|---|---|---|---|---|---|
| A1 | all 0.5 | 0.1 | 1000 | 0.3900 | 1008 | 0.36 | 1 | 114 | baseline; no improvement after attempt 114 |
| A2 | all 0.3 | 0.1 | 1000 | 0.4409 | 1008 | 0.35 | 79 | 263 | on ties it drifted up knob 0 (0.3 to 0.6) until it hit non-zero; no improvement after attempt 263 |
| A3 | all 0.4 | 0.1 | 1000 | 0.4409 | 1008 | 0.35 | 67 | 305 | same end point as A2 |
| A4 | all 0.6 | 0.1 | 1000 | 0.0000 | 1002 | 0.36 | never | - | never left zero; drifted to all knobs = 1.0 |
| A5 | all 0.7 | 0.1 | 1000 | 0.0000 | 1008 | 0.37 | never | - | never left zero; drifted to all knobs = 1.0 |
| A6 | all 0.8 | 0.1 | 1000 | 0.0000 | 1008 | 0.36 | never | - | never left zero; drifted to all knobs = 1.0 |
| A7 | all 0.9 | 0.1 | 1000 | 0.0000 | 1002 | 0.37 | never | - | never left zero; drifted to all knobs = 1.0 |
| A8 | all 0.1 | 0.1 | 1000 | 0.0000 | 1007 | 0.37 | never | - | never left zero; drifted knobs 0 to 4 up to 1.0 |
| A9 | all 0.2 | 0.1 | 1000 | 0.0000 | 1010 | 0.36 | never | - | never left zero; drifted knobs 0 to 4 up to 1.0 |

Attempts vary between 1002 and 1010 because the budget is only checked between whole steps, and each step can cost a different number of attempts (neighbours clipped at the 0/1 boundary are removed as duplicates).
