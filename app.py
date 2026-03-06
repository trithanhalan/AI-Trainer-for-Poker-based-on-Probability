#!/usr/bin/env python3
"""
PokerMind — AI Poker Trainer Based on Probability
Teaches poker strategy using real-time hand evaluation, pot odds calculation,
and expected value analysis. Built with Streamlit.
"""

import streamlit as st
import random
from itertools import combinations
from collections import Counter

# ──────────────────────────────────────────────
# Card & Deck Logic
# ──────────────────────────────────────────────

SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
RANK_VALUES = {r: i for i, r in enumerate(RANKS, 2)}

HAND_RANKINGS = {
    9: "Royal Flush",
    8: "Straight Flush",
    7: "Four of a Kind",
    6: "Full House",
    5: "Flush",
    4: "Straight",
    3: "Three of a Kind",
    2: "Two Pair",
    1: "One Pair",
    0: "High Card"
}


def create_deck():
    return [(r, s) for r in RANKS for s in SUITS]


def card_str(card):
    rank, suit = card
    color = "🔴" if suit in ['♥', '♦'] else "⚫"
    return f"{rank}{suit}"


def evaluate_hand(cards):
    """Evaluate a 5-card poker hand and return (rank, description)."""
    ranks = sorted([RANK_VALUES[c[0]] for c in cards], reverse=True)
    suits = [c[1] for c in cards]
    rank_counts = Counter(ranks)
    counts = sorted(rank_counts.values(), reverse=True)
    
    is_flush = len(set(suits)) == 1
    is_straight = (max(ranks) - min(ranks) == 4 and len(set(ranks)) == 5)
    
    # Check for A-2-3-4-5 straight (wheel)
    if set(ranks) == {14, 2, 3, 4, 5}:
        is_straight = True
        ranks = [5, 4, 3, 2, 1]  # Ace counts as 1
    
    if is_flush and is_straight:
        if max(ranks) == 14 and min(ranks) == 10:
            return (9, "Royal Flush")
        return (8, "Straight Flush")
    if counts == [4, 1]:
        return (7, "Four of a Kind")
    if counts == [3, 2]:
        return (6, "Full House")
    if is_flush:
        return (5, "Flush")
    if is_straight:
        return (4, "Straight")
    if counts == [3, 1, 1]:
        return (3, "Three of a Kind")
    if counts == [2, 2, 1]:
        return (2, "Two Pair")
    if counts == [2, 1, 1, 1]:
        return (1, "One Pair")
    return (0, "High Card")


def best_hand(cards):
    """Find the best 5-card hand from any number of cards."""
    if len(cards) < 5:
        return evaluate_hand(cards + [('2', '♠')] * (5 - len(cards)))
    
    best = (0, "High Card")
    for combo in combinations(cards, 5):
        result = evaluate_hand(list(combo))
        if result[0] > best[0]:
            best = result
    return best


def calculate_outs(hole_cards, community_cards, deck):
    """Calculate outs — cards that improve the hand."""
    current_hand = best_hand(hole_cards + community_cards)
    outs = []
    
    for card in deck:
        if card in hole_cards or card in community_cards:
            continue
        new_hand = best_hand(hole_cards + community_cards + [card])
        if new_hand[0] > current_hand[0]:
            outs.append(card)
    
    return outs


def calculate_pot_odds(pot_size, bet_to_call):
    """Calculate pot odds as a percentage."""
    if bet_to_call == 0:
        return 100.0
    return (bet_to_call / (pot_size + bet_to_call)) * 100


def monte_carlo_win_rate(hole_cards, community_cards, num_simulations=1000):
    """Estimate win rate using Monte Carlo simulation against a random hand."""
    deck = create_deck()
    remaining = [c for c in deck if c not in hole_cards and c not in community_cards]
    
    wins = 0
    ties = 0
    
    for _ in range(num_simulations):
        sim_deck = remaining.copy()
        random.shuffle(sim_deck)
        
        # Deal remaining community cards
        cards_needed = 5 - len(community_cards)
        idx = 0
        sim_community = community_cards + sim_deck[idx:idx + cards_needed]
        idx += cards_needed
        
        # Deal opponent hand
        opp_hand = sim_deck[idx:idx + 2]
        
        my_best = best_hand(hole_cards + sim_community)
        opp_best = best_hand(list(opp_hand) + sim_community)
        
        if my_best[0] > opp_best[0]:
            wins += 1
        elif my_best[0] == opp_best[0]:
            ties += 1
    
    return (wins + ties * 0.5) / num_simulations * 100


# ──────────────────────────────────────────────
# Streamlit UI
# ──────────────────────────────────────────────

st.set_page_config(
    page_title="PokerMind — AI Poker Trainer",
    page_icon="🃏",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp { font-family: 'Inter', sans-serif; }
    
    .poker-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #1a5c2e 0%, #0d3b1e 100%);
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
    }
    
    .poker-header h1 { font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; }
    .poker-header p { font-size: 1.1rem; opacity: 0.9; }
    
    .card-display {
        display: inline-block;
        padding: 8px 12px;
        margin: 4px;
        border-radius: 8px;
        font-size: 1.3rem;
        font-weight: 700;
        background: white;
        border: 2px solid #333;
        min-width: 50px;
        text-align: center;
    }
    
    .card-red { color: #e74c3c; }
    .card-black { color: #2c3e50; }
    
    .decision-call { background: #d4edda; border-radius: 8px; padding: 1rem; border-left: 4px solid #28a745; }
    .decision-fold { background: #f8d7da; border-radius: 8px; padding: 1rem; border-left: 4px solid #dc3545; }
    .decision-raise { background: #cce5ff; border-radius: 8px; padding: 1rem; border-left: 4px solid #007bff; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="poker-header">
    <h1>🃏 PokerMind</h1>
    <p>AI Poker Trainer — Learn Texas Hold'em strategy through probability</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state FIRST (before any widgets access it)
if "hole_cards" not in st.session_state:
    deck = create_deck()
    random.shuffle(deck)
    st.session_state.hole_cards = [deck[0], deck[1]]
    st.session_state.flop = [deck[2], deck[3], deck[4]]
    st.session_state.turn = deck[5]
    st.session_state.river = deck[6]

# Sidebar
with st.sidebar:
    st.header("🎮 Game Setup")
    
    mode = st.radio("Mode", ["🎲 Random Hand", "✋ Choose Cards"])
    
    if mode == "🎲 Random Hand":
        if st.button("🔄 Deal New Hand", use_container_width=True):
            deck = create_deck()
            random.shuffle(deck)
            st.session_state.hole_cards = [deck[0], deck[1]]
            st.session_state.flop = [deck[2], deck[3], deck[4]]
            st.session_state.turn = deck[5]
            st.session_state.river = deck[6]
    
    st.divider()
    st.header("💰 Pot Settings")
    pot_size = st.number_input("Pot Size ($)", min_value=1, value=100, step=10)
    bet_to_call = st.number_input("Bet to Call ($)", min_value=0, value=20, step=5)
    
    st.divider()
    st.header("⚙️ Settings")
    num_sims = st.slider("Monte Carlo Simulations", 100, 5000, 1000, step=100)

hole_cards = st.session_state.hole_cards
flop = st.session_state.flop
turn = st.session_state.turn
river = st.session_state.river

# Display cards
def display_cards(cards, label=""):
    cards_html = " ".join([
        f'<span class="card-display {"card-red" if c[1] in ["♥","♦"] else "card-black"}">{c[0]}{c[1]}</span>'
        for c in cards
    ])
    st.markdown(f"**{label}** {cards_html}", unsafe_allow_html=True)

st.subheader("🃏 Your Hand")
display_cards(hole_cards, "Hole Cards:")

# Street selector
street = st.radio("Board Stage", ["Pre-flop", "Flop", "Turn", "River"], horizontal=True)

community_cards = []
if street in ["Flop", "Turn", "River"]:
    community_cards = flop.copy()
    display_cards(flop, "Flop:")
if street in ["Turn", "River"]:
    community_cards.append(turn)
    display_cards([turn], "Turn:")
if street == "River":
    community_cards.append(river)
    display_cards([river], "River:")

st.divider()

# Analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Hand Analysis")
    
    all_cards = hole_cards + community_cards
    hand_rank, hand_name = best_hand(all_cards)
    
    st.metric("Current Hand", hand_name)
    st.metric("Hand Rank", f"{hand_rank}/9")
    
    # Win rate
    with st.spinner("Calculating win rate..."):
        win_rate = monte_carlo_win_rate(hole_cards, community_cards, num_sims)
    
    st.metric("Estimated Win Rate", f"{win_rate:.1f}%")
    
    if win_rate >= 70:
        st.progress(win_rate / 100, text="Strong hand")
    elif win_rate >= 50:
        st.progress(win_rate / 100, text="Decent hand")
    elif win_rate >= 30:
        st.progress(win_rate / 100, text="Marginal hand")
    else:
        st.progress(win_rate / 100, text="Weak hand")

with col2:
    st.subheader("💰 Pot Odds & Decision")
    
    pot_odds = calculate_pot_odds(pot_size, bet_to_call)
    
    st.metric("Pot Odds", f"{pot_odds:.1f}%")
    st.metric("Pot Size", f"${pot_size}")
    st.metric("Bet to Call", f"${bet_to_call}")
    
    # Decision engine
    ev = (win_rate / 100 * pot_size) - ((1 - win_rate / 100) * bet_to_call)
    st.metric("Expected Value", f"${ev:+.2f}")
    
    if ev > 0 and win_rate > 60:
        st.markdown('<div class="decision-raise">🚀 <strong>RAISE</strong> — Strong expected value and high win probability</div>', unsafe_allow_html=True)
    elif ev > 0:
        st.markdown('<div class="decision-call">✅ <strong>CALL</strong> — Positive expected value, pot odds are favorable</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="decision-fold">❌ <strong>FOLD</strong> — Negative expected value, save your chips</div>', unsafe_allow_html=True)

# Outs analysis
if street in ["Flop", "Turn"] and len(community_cards) >= 3:
    st.divider()
    st.subheader("🎯 Outs Analysis")
    
    deck = create_deck()
    outs = calculate_outs(hole_cards, community_cards, deck)
    
    remaining_cards = 52 - len(hole_cards) - len(community_cards)
    outs_pct = (len(outs) / remaining_cards * 100) if remaining_cards > 0 else 0
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Number of Outs", len(outs))
    with col_b:
        st.metric("Probability (Next Card)", f"{outs_pct:.1f}%")
    with col_c:
        rule_of = len(outs) * (4 if street == "Flop" else 2)
        st.metric(f"Rule of {'4' if street == 'Flop' else '2'} Estimate", f"~{rule_of}%")
    
    if outs:
        display_cards(outs[:10], "Top Outs:")
        if len(outs) > 10:
            st.caption(f"... and {len(outs) - 10} more")

# Hand Rankings Reference
with st.expander("📖 Hand Rankings Reference"):
    st.markdown("""
    | Rank | Hand | Example |
    |------|------|---------|
    | 9 | **Royal Flush** | A♠ K♠ Q♠ J♠ 10♠ |
    | 8 | **Straight Flush** | 5♥ 6♥ 7♥ 8♥ 9♥ |
    | 7 | **Four of a Kind** | K♠ K♥ K♦ K♣ 3♠ |
    | 6 | **Full House** | J♠ J♥ J♦ 8♣ 8♠ |
    | 5 | **Flush** | A♦ J♦ 8♦ 5♦ 2♦ |
    | 4 | **Straight** | 4♠ 5♥ 6♦ 7♣ 8♠ |
    | 3 | **Three of a Kind** | Q♠ Q♥ Q♦ 7♣ 3♠ |
    | 2 | **Two Pair** | 10♠ 10♥ 4♦ 4♣ A♠ |
    | 1 | **One Pair** | 9♠ 9♥ A♦ J♣ 5♠ |
    | 0 | **High Card** | A♠ K♥ 9♦ 7♣ 3♠ |
    """)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #6c757d;'>"
    "Built by <a href='https://github.com/trithanhalan'>Alan</a> | "
    "PokerMind — Learn poker through probability, not luck"
    "</p>",
    unsafe_allow_html=True
)
