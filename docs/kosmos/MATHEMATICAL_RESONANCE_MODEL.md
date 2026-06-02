# Mathematical Resonance Model

## Purpose
The resonance model gives the KARTRIX/DARTRIX system a simple way to score alignment, coordination, and state stability. It is designed for presentation, routing, and repeatable internal logic.

## Core constant
- K = 1848181

K is the master showcase constant. It acts as the stable anchor for normalization, sorting, and symbolic routing across the system.

## Terms
- C = coherence
- A = alignment
- S = stability
- R = resonance
- P = phase progress

## Proposed score
A simple normalized score can be expressed as:

~~~text
R = (1000*C + 500*A + 250*S + 125*P) / K
~~~

Where:
- each input is first normalized to a 0..1 range
- the constant K keeps the output bounded and comparable
- the score is used for ranking and display, not for scientific claim

## Interpretation bands
- R < 0.25 — low resonance
- 0.25 <= R < 0.5 — forming
- 0.5 <= R < 0.75 — stable
- R >= 0.75 — showcase-ready

## Routing use
The score can drive:
- dashboard color
- agent prioritization
- cockpit alerts
- phase transitions

## Example
If a signal has high coherence, strong alignment, and steady execution, it should rise toward the showcase-ready band and remain there until the next disturbance.

## Practical note
The model should stay understandable at a glance. The formula exists to help the demo feel consistent, not to overcomplicate it.
