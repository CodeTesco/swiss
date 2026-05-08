A custom matchmaking engine designed for a multi-week, Swiss-system chess league. Instead of relying on traditional, compute-heavy parsing methods, it models tournament pairings as a Maximum Weight Matching problem in a bipartite graph using Python's NetworkX library. By calculating edge weights based on a hybrid system of League Points and Rapid Ratings, the algorithm mathematically guarantees optimal, competitive, and non-repeating matchups for every round.

Key Features:

Graph Theory Architecture: Utilizes NetworkX to evaluate all active players simultaneously, preventing the "dead-end" pairing errors common in greedy algorithms.

Hybrid Weighting Logic: Matches players dynamically by heavily penalizing point discrepancies while using Elo ratings as a secondary balancing weight.

Optimized for Series Play: Specifically engineered for a two-game (Home & Away) weekly fixture format, entirely eliminating the algorithmic overhead of piece-color balancing.

JSON State Management: Lightweight, persistent database handling for tracking player stats, match history, and active league standings across an 8-week season.
