# Iterated Prisoner’s Dilemma — Optimization & ML

This project simulates the Iterated Prisoner’s Dilemma (IPD) and applies optimization methods (Genetic Algorithm, Hill Climb) to evolve strong strategies. It also includes utilities for baseline comparisons and dataset generation.

---

## ✅ What’s Included

### **Strategies**
- Baselines: `ALLC`, `ALLD`, `RAND`, `TFT`, `TF2T`, `STFT`
- Lookup-table strategies (64‑bit chromosome)

### **Optimization**
- Genetic Algorithm (`src/optim/genetic_algorithm.py`)
- Hill Climb (`src/optim/hill_climb.py`)
- Experiment runners for GA/Hill/GA sweeps

### **Evaluation**
- Tournament and head‑to‑head play
- Fitness evaluation against opponent pools

### **Outputs**
- Results saved to `results/tables/`
- Figures placeholder in `results/figures/`

---

## 📁 Folder Structure

```text
src/
  experiments/
    compare_best.py
    opponent_pool.py
    run_baselines.py
    run_ga.py
    run_ga_sweep.py
    run_hill_climb.py
  game/
    engine.py
    evaluate.py
    payoff.py
  ml/
    build_dataset.py
  optim/
    genetic_algorithm.py
    hill_climb.py
  strategies/
    baselines.py
    lookup_table.py

results/
  tables/
    baselines_tournament.csv
    ga_best.csv
    ga_best_vs_baselines.csv
    ga_fitness_history.csv
    ga_runs_summary.csv
    hill_best.csv
    hill_history.csv
  figures/
    .gitkeep

report/
  optimization.md
```

---

## ▶️ How to Run

From repo root:

```powershell
python -m src.experiments.run_baselines
# optional: python -m src.experiments.run_baselines --runs 500 --seed-start 42 --rounds 300
python -m src.experiments.run_ga
python -m src.experiments.run_hill_climb
python -m src.experiments.run_ga_sweep
python -m src.experiments.compare_best
```

---

## 🧪 Results

Generated results are stored in:

```
results/tables/
```

Examples:
- `baselines_tournament.csv`
- `baselines_tournament_summary.csv`
- `ga_best.csv`
- `ga_fitness_history.csv`
- `ga_best_vs_baselines.csv`
- `hill_best.csv`

---

## 📌 Notes

- Always run from the **project root** so `src.*` imports resolve.
- Baseline, GA, and Hill Climb runs are stochastic; set seeds for reproducibility.
- To compare a GA‑best strategy vs baselines, update `BEST` in `compare_best.py`.

---

## 📄 Report

See: `report/optimization.md`

---

