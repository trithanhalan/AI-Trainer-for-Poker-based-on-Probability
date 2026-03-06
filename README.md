# 🃏 PokerMind — AI Poker Trainer

> **Learn Texas Hold'em strategy through probability, not luck.** Real-time hand evaluation, Monte Carlo win rate simulation, pot odds calculator, and outs analysis.

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Live Demo](https://img.shields.io/badge/Live_Demo-Streamlit_Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://ai-trainer-for-poker-based-on-probability.streamlit.app/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## 🎯 What It Does

PokerMind evaluates your poker hand in real-time and teaches you the math behind every decision:

- **🃏 Hand Evaluation** — Identifies your best 5-card hand from any combination
- **📊 Monte Carlo Win Rate** — Estimates win probability against random opponents (1000+ simulations)
- **💰 Pot Odds Calculator** — Determines if a call is mathematically profitable
- **🎯 Outs Analysis** — Counts cards that improve your hand with Rule of 2/4
- **🧠 Decision Engine** — Recommends RAISE / CALL / FOLD based on expected value

## 🚀 Quick Start

```bash
git clone https://github.com/trithanhalan/AI-Trainer-for-Poker-based-on-Probability.git
cd AI-Trainer-for-Poker-based-on-Probability
pip install -r requirements.txt
streamlit run app.py
```

## 🧮 The Math Behind It

### Monte Carlo Simulation
Simulates 1000+ random hands to estimate win probability:
```
Win Rate = (Wins + 0.5 × Ties) / Total Simulations
```

### Pot Odds
```
Pot Odds % = Bet to Call / (Pot + Bet to Call)
```

### Expected Value (EV)
```
EV = (Win% × Pot Size) − (Lose% × Bet to Call)
EV > 0 → Profitable Call | EV < 0 → Fold
```

### Rule of 4 and 2
Quick outs estimation:
- **Flop:** Outs × 4 ≈ % chance to hit by river
- **Turn:** Outs × 2 ≈ % chance to hit on river

## 📁 Project Structure

```
AI-Trainer-for-Poker/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies  
├── README.md           # This file
└── LICENSE             # MIT License
```

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">
  Built by <a href="https://github.com/trithanhalan">Alan</a> — Probability is the house's edge. Understanding it is yours.
</p>
