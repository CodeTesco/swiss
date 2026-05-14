import networkx as nx
import json
from pathlib import Path

class Player:
    def __init__(self, player_id, name, rating, points=0.0, played_against=None, active=True):
        self.id = player_id
        self.name = name
        self.rating = rating
        self.points = points
        self.played_against = set(played_against) if played_against else set()
        self.active = active
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "rating": self.rating,
            "points": self.points,
            "played_against": list(self.played_against),
            "active": self.active
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            player_id=data["id"],
            name=data["name"],
            rating=data["rating"],
            points=data.get("points", 0.0),
            played_against=data.get("played_against", []),
            active=data.get("active", True)
        )

BASE_DIR = Path(__file__).resolve().parent
TABLE_DATA = BASE_DIR / "league_standings.json"
LIVE_LEAGUE_DATA = BASE_DIR.parent / "Frontend Projects/League Table/league_standings.json"

def load_league_state():
    try:
        with open(TABLE_DATA, "r") as file:
            json_data = json.load(file)
            return [Player.from_dict(data) for data in json_data]
    except FileNotFoundError:
        print("File not found.")
        return []

def save_league_state(players_list):
    with open(TABLE_DATA, "w") as file:
        json_data = [player.to_dict() for player in players_list]
        json.dump(json_data, file, indent=4)

    with open(LIVE_LEAGUE_DATA, "w") as file:
        json_data = [player.to_dict() for player in players_list]
        json.dump(json_data, file, indent=4)
    print("League state saved successfully")

def record_result(p1, p2, p1_score, p2_score):
    p1.points += p1_score
    p2.points += p2_score

    p1.played_against.add(p2.id)
    p2.played_against.add(p1.id)

def calc_match_weight(p1, p2):
    if p2.id in p1.played_against or p1.id in p2.played_against:
        return -1

    base_score = 1000000

    points_diff = abs(p1.points - p2.points)
    points_penalty = points_diff * 10000

    rating_diff = abs(p1.rating - p2.rating)
    rating_penalty = rating_diff * 10

    weight = base_score - points_penalty - rating_penalty

    return weight

def generate_pairings(player_list):
    players = player_list[:]

    G = nx.Graph()

    for i in range(len(players)):
        p1 = players[i]
        G.add_node(p1.name)
        for p2 in players:
            if p1 == p2:
                continue

            weight = calc_match_weight(p1, p2)

            if weight > 0:
                G.add_edge(p1.name, p2.name, weight=weight)
    
    pairings = nx.max_weight_matching(G, maxcardinality=True)

    return pairings

def run_cli_updater():

    players = load_league_state()
    if not players:
        print("No players found")
        return

    print("\nLive Match Updater")
    print("Type 'q' at any time to save and exit.")

    while True:
        print("\n" + "-"*30)

        p1_input = input("Enter Player 1 Name: ").strip()
        if p1_input.lower() == 'q':
            break
            
        p2_input = input("Enter Player 2 Name: ").strip()
        if p2_input.lower() == 'q':
            break
            
        p1 = next((p for p in players if p.name.lower() == p1_input.lower()), None)
        p2 = next((p for p in players if p.name.lower() == p2_input.lower()), None)
        
        if not p1 or not p2:
            print("Could not find one or both of the players, check spelling.")
            continue
            
        try:
            print(f"\nWin = 1 | Draw = 0.5 | Lose = 0")
            p1_score = float(input(f"Enter points for {p1.name}: "))
            p2_score = float(input(f"Enter points for {p2.name}: "))
            
            if p1_score + p2_score > 1:
                print("Total points in a match cannot exceed 1.")
                continue
                
            record_result(p1, p2, p1_score, p2_score)
            print(f"Match recorded for {p1.name} [{p1_score}] vs [{p2_score}] {p2.name}")
            
        except ValueError:
            print("Invalid input")

    save_league_state(players)
    print("\nAll results saved.")

# to generate pairings
# players_list = load_league_state()
# pairings = generate_pairings(players_list)
# print(pairings)

# to update league
run_cli_updater()