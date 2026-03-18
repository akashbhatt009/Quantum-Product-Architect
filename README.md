# Quantum-Product-Architect
An AI-driven decision-support engine for Product Managers and BAs. Features a dynamic dual-framework architecture (RICE/WSJF) and automated roadmap synthesis to prioritize high-value business ventures.

<img width="3402" height="1714" alt="image" src="https://github.com/user-attachments/assets/528145e1-493b-4c67-a04c-65143c2d3db6" />

## 🧮 Decision Logic & Framework Methodology

To ensure objective backlog grooming, this engine utilizes two primary quantitative models:

### 1. WSJF (Weighted Shortest Job First)
Used for **Economic Prioritization** in Scaled Agile (SAFe) environments. The system calculates the score based on the "Cost of Delay" divided by the "Job Size" (Effort).

$$WSJF = \frac{User-Business Value + Time Criticality + Risk Reduction}{Estimated Effort}$$

* **Goal:** Identify the "Quick Wins" that provide the highest business value in the shortest time.

### 2. RICE Framework
Used for **Growth and Reach** scoring in consumer-facing product development.

$$RICE Score = \frac{Reach \times Impact \times Confidence}{Effort}$$

* **Goal:** Balance massive user reach against the team's level of confidence in the projected impact.
