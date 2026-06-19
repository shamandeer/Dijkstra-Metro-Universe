# Discrete Mathematics Application in Python
# Graph Theory and Dijkstra's Algorithm

import matplotlib.pyplot as plt
import networkx as nx

# Constants
INF = 9999
hazard_const = {
    "Radiation": 50,
    "Biohazard": 75,
    "Mental": 35,
    "Collapse": 50,
    "Various": 100,
    "None": 0,
}

faction_const = {
    "VDNKh": 0,
    "Hanza": 25,
    "Red Line": 75,
    "Fourth Reich": 75,
    "Polis": 0,
    "Bandits": 65,
    "Gangs": 35,
    "Arbat": 0,
    "1905": 0,
    "Mutants": 75,
    "Others": 0,
}

# Weight Calculation using distance, hazard constant, and faction constant
def calculate_weight(dist: int, hazard: str, faction: str) -> int:
    weight = dist
    if (hazard in hazard_const):
        weight += hazard_const[hazard]
    if (faction in faction_const):
        weight += faction_const[faction]
    return weight

# Metro Graph using Adjacency Lists
# Note: Biblioteka im. Lenina, Borovitskaya, Arbatskaya (Arbatsko-Pokrovskaya Line, not the one in Filyovskaya Line), and Aleksandrovsky Sad is combined into one Polis Station
metro_graph = {
    "Exhibition": {
        "Alekseyevskaya": calculate_weight(13, "None", "VDNKh"),
    },
    "Alekseyevskaya": {
        "Exhibition": calculate_weight(13, "None", "VDNKh"),
        "Rizhskaya": calculate_weight(17, "Mental", "VDNKh"),
    },
    "Rizhskaya": {
        "Alekseyevskaya": calculate_weight(17, "Mental", "VDNKh"),
        "Prospekt Mira": calculate_weight(16, "None", "Hanza"),
    },
    "Prospekt Mira": {
        "Rizhskaya": calculate_weight(16, "None", "VDNKh"),
        "Novoslobodskaya": calculate_weight(18, "None", "Hanza"),
        "Komsomolskaya": calculate_weight(16, "None", "Hanza"),
        "Sukharevskaya": calculate_weight(7, "Mental", "Bandits"), # bandits are game-only
    },
    "Sukharevskaya": {
        "Prospekt Mira": calculate_weight(7, "Mental", "Hanza"),
        "Turgenevskaya": calculate_weight(8, "Various", "Mutants"), # mutants are game-only
    },
    "Turgenevskaya": {
        "Sukharevskaya": calculate_weight(8, "Various", "Bandits"),
        # closed access to Sretensky Bulvar and Chistye Prudy
        "Kitay-Gorod": calculate_weight(12, "Various", "Bandits"),
    },
    "Kitay-Gorod": {
        "Turgenevskaya": calculate_weight(12, "Various", "Mutants"),
        "Tretyakovskaya": calculate_weight(16, "Biohazard", "Gangs"), # tretyakovskaya is technically divided into two areas: uninhabited, and Venice (controlled by a gang). to simplify, we will assume Venice as it is the most documented
        # while not listed in the map, Tretyakovskaya is a flooded station with some areas inhibited by mutant shrimps, so we assume the edges having biohazard penalty
        "Kuznetsky Most": calculate_weight(7, "None", "Red Line"), # in the game it was a Red Line armory under the guise of technicians
        "Taganskaya": calculate_weight(19, "None", "Hanza"),
    },
    "Tretyakovskaya": {
        "Kitay-Gorod": calculate_weight(16, "Biohazard", "Bandits"),
        "Novokuznetskaya": calculate_weight(1, "None", "Bandits"),
        "Oktyabrskaya": calculate_weight(17, "Biohazard", "Hanza"),
        "Marksistskaya": calculate_weight(16, "Mental", "Hanza"),
    },
    "Oktyabrskaya": {
        "Tretyakovskaya": calculate_weight(17, "Biohazard", "Gangs"),
        "Dobryninskaya": calculate_weight(9, "None", "Hanza"),
        "Park Kultury Koltsevaya": calculate_weight(11, "None", "Hanza"),
    },
    "Komsomolskaya": {
        "Prospekt Mira": calculate_weight(16, "None", "Hanza"),
        "Kurskaya": calculate_weight(20, "None", "Hanza"),
        "Krasnye Vorota": calculate_weight(8, "None", "Red Line"),
    },
    "Krasnye Vorota": {
        "Komsomolskaya": calculate_weight(8, "None", "Hanza"),
        "Chistye Prudy": calculate_weight(7, "None", "Red Line"),
    },
    "Chistye Prudy": {
        "Krasnye Vorota": calculate_weight(7, "None", "Red Line"),
        "Sretensky Bulvar": calculate_weight(1, "None", "Others"),
        "Lubyanka": calculate_weight(10, "None", "Red Line"),
    },
    "Lubyanka": {
        "Chistye Prudy": calculate_weight(10, "None", "Red Line"),
        "Kuznetsky Most": calculate_weight(1, "None", "Red Line"),
        "Okhotny Ryad": calculate_weight(7, "None", "Red Line"),
    },
    "Okhotny Ryad": {
        "Lubyanka": calculate_weight(7, "None", "Red Line"),
        "Teatralnaya": calculate_weight(2, "None", "Red Line"),
        "Polis Station": calculate_weight(8, "None", "Polis"),
    },
    "Polis Station": {
        "Okhotny Ryad": calculate_weight(8, "None", "Red Line"),
        "Kropotkinskaya": calculate_weight(8, "None", "Red Line"),
        "Chekhovskaya": calculate_weight(15, "None", "Fourth Reich"),
        "Polyanka": calculate_weight(16, "Various", "Mutants"), # in game, the area has ghosts/hallucinations and mutants, as well as anomalies
        "Ploshchad Revolyutsii": calculate_weight(11, "None", "Red Line"),
        "Smolenskaya": calculate_weight(21, "None", "Arbat Confederation"),
    },
    "Kropotkinskaya": {
        "Polis Station": calculate_weight(8, "None", "Polis"),
        "Park Kultury Sokolnicheskaya": calculate_weight(13, "None", "Red Line"),
    },
    "Park Kultury Sokolnicheskaya": {
        "Kropotkinskaya": calculate_weight(13, "None", "Red Line"),
    },
    "Park Kultury Koltsevaya": {
        "Oktyabrskaya": calculate_weight(11, "None", "Hanza"),
        "Kiyevskaya": calculate_weight(21, "None", "Hanza"),
    },
    "Trubnaya": {
        "Tsvetnoy Bulvar": calculate_weight(2, "None", "Others"),
    },
    "Sretensky Bulvar": {
        "Chistye Prudy": calculate_weight(1, "None", "Red Line"),
        "Chkalovskaya": calculate_weight(16, "Collapse", "Hanza"),
    },
    "Chkalovskaya": {
        "Kurskaya": calculate_weight(2, "None", "Hanza"),
        "Sretensky Bulvar": calculate_weight(16, "Collapse", "Others"),
    },
    "Marksistskaya": {
        "Tretyakovskaya": calculate_weight(16, "Mental", "Gangs"),
        "Taganskaya": calculate_weight(1, "None", "Hanza"),
    },
    "Taganskaya": {
        "Kurskaya": calculate_weight(18, "None", "Hanza"),
        "Marksistskaya": calculate_weight(1, "None", "Hanza"),
        "Paveletskaya": calculate_weight(13, "None", "Hanza"),
        "Kitay-Gorod": calculate_weight(19, "None", "Bandits"),
    },
    "Kuznetsky Most": {
        "Kitay-Gorod": calculate_weight(7, "None", "Bandits"),
        "Lubyanka": calculate_weight(1, "None", "Red Line"),
        "Pushkinskaya": calculate_weight(13, "None", "Fourth Reich"),
    },
    "Pushkinskaya": {
        "Kuznetsky Most": calculate_weight(13, "None", "Red Line"),
        "Chekhovskaya": calculate_weight(1, "None", "Fourth Reich"),
        "Barrikadnaya": calculate_weight(18, "None", "1905"),
    },
    "Barrikadnaya": {
        "Pushkinskaya": calculate_weight(18, "None", "Fourth Reich"),
        "Krasnopresnenskaya": calculate_weight(1, "None", "Hanza"),
    },
    "Krasnopresnenskaya": {
        "Barrikadnaya": calculate_weight(1, "None", "1905"),
        "Belorusskaya": calculate_weight(18, "None", "Hanza"),
        "Kiyevskaya": calculate_weight(23, "None", "Hanza"),
    },
    "Novoslobodskaya": {
        "Belorusskaya": calculate_weight(13, "None", "Hanza"),
        "Prospekt Mira": calculate_weight(18, "None", "Hanza"),
        "Tsvetnoy Bulvar": calculate_weight(13, "None", "Others"),
    },
    "Tsvetnoy Bulvar": {
        "Novoslobodskaya": calculate_weight(13, "None", "Hanza"),
        "Trubnaya": calculate_weight(2, "None", "Others"),
        "Chekhovskaya": calculate_weight(9, "None", "Fourth Reich"),
    },
    "Chekhovskaya": {
        "Pushkinskaya": calculate_weight(1, "None", "Hanza"),
        "Tverskaya": calculate_weight(2, "None", "Fourth Reich"),
        "Tsvetnoy Bulvar": calculate_weight(9, "None", "Others"),
        "Polis Station": calculate_weight(15, "Collapse", "Others"),
    },
    "Polyanka": {
        "Polis Station": calculate_weight(16, "Various", "Mutants"),
        "Serpukhovskaya": calculate_weight(12, "Various", "Hanza"),
    },
    "Dobryninskaya": {
        "Oktyabrskaya": calculate_weight(9, "None", "Hanza"),
        "Serpukhovskaya": calculate_weight(1, "None", "Hanza"),
        "Paveletskaya": calculate_weight(9, "None", "Hanza"),
    },
    "Serpukhovskaya": {
        "Dobryninskaya": calculate_weight(1, "None", "Hanza"),
        "Polyanka": calculate_weight(12, "Various", "Mutants"),
    },
    "Belorusskaya": {
        "Novoslobodskaya": calculate_weight(13, "None", "Hanza"),
        "Krasnopresnenskaya": calculate_weight(18, "None", "Hanza"),
        "Mayakovskaya": calculate_weight(10, "None", "Others"),
    },
    "Mayakovskaya": {
        "Belorusskaya": calculate_weight(10, "None", "Hanza"),
        "Tverskaya": calculate_weight(9, "None", "Fourth Reich"),
    },
    "Tverskaya": {
        "Mayakovskaya": calculate_weight(9, "None", "Others"),
        "Chekhovskaya": calculate_weight(2, "None", "Fourth Reich"),
        "Teatralnaya": calculate_weight(12, "None", "Red Line"),
    },
    "Teatralnaya": {
        "Tverskaya": calculate_weight(12, "None", "Fourth Reich"),
        "Okhotny Ryad": calculate_weight(2, "None", "Red Line"),
        "Ploshchad Revolyutsii": calculate_weight(2, "None", "Red Line"),
        "Novokuznetskaya": calculate_weight(19, "None", "Bandits"),
    },
    "Novokuznetskaya": {
        "Teatralnaya": calculate_weight(19, "None", "Red Line"),
        "Tretyakovskaya": calculate_weight(1, "None", "Gangs"),
        "Paveletskaya": calculate_weight(12, "Biohazard", "Hanza"), # missing door seal so mutants get in easily
        # technically an independent station but another part of it is hansa's ring, so we we will simplify it as such
    },
    "Paveletskaya": {
        "Dobryninskaya": calculate_weight(9, "None", "Hanza"),
        "Taganskaya": calculate_weight(13, "None", "Hanza"),
        "Novokuznetskaya": calculate_weight(12, "None", "Bandits"),
    },
    "Kiyevskaya": {
        "Krasnopresnenskaya": calculate_weight(23, "None", "Hanza"),
        "Park Kultury Koltsevaya": calculate_weight(21, "None", "Hanza"),
        "Smolenskaya": calculate_weight(11, "None", "Arbat Confederation"),
    },
    "Smolenskaya": {
        "Kiyevskaya": calculate_weight(11, "None", "Hanza"),
        "Polis Station": calculate_weight(17, "None", "Polis"),
    },
    "Ploshchad Revolyutsii": {
        "Polis Station": calculate_weight(11, "None", "Polis"),
        "Teatralnaya": calculate_weight(2, "None", "Red Line"),
        "Kurskaya": calculate_weight(24, "None", "Hanza"),
    },
    "Kurskaya": {
        "Komsomolskaya": calculate_weight(20, "None", "Hanza"),
        "Taganskaya": calculate_weight(18, "None", "Hanza"),
        "Chkalovskaya": calculate_weight(2, "None", "Hanza"),
        "Ploshchad Revolyutsii": calculate_weight(24, "None", "Red Line")
    },
}

# Dijkstra's Algorithm for the Metro System Navigation  
def Dijkstra(G: dict, a: str) -> dict:
    # Initialization
    Info: dict = {}
    N = len(G)
    for key in G.keys():
        Info.update({key: {"value": INF, "prev": None}})
    Info[a]["value"] = 0
    S = set()

    for i in range(N):
        # Find vertex with minimum L(u) that is not in S
        min_key = None
        min_val = INF
        for key in Info.keys():
            if (key not in S and Info[key]["value"] < min_val):
                min_key = key
                min_val = Info[key]["value"]
        if (min_key != None):
            S.add(min_key)
        else:
            print(f"Route unavailable to {min_key}")
            break
        for neighbor in G[min_key].keys():
            if (neighbor not in S):
                dst = Info[min_key]["value"] + G[min_key][neighbor]
                if (dst < Info[neighbor]["value"]):
                    Info[neighbor]["value"] = dst
                    Info[neighbor]["prev"] = min_key
    return Info

# for tracing output
def Trace_Dijkstra(Info: dict, a: str):
    for key in Info.keys():
        is_first = True
        if (key == a):
            continue
        trace_list = []
        trace_list.append(key)
        if (is_first):
            cur_weight = Info[key]["value"]
            is_first = False
        cur_prev = Info[key]["prev"]
        while (cur_prev != None):
            trace_list.insert(0, cur_prev)
            cur_prev = Info[cur_prev]["prev"]
        
        print(f"From {a} to {key} ({cur_weight}): {' - '.join(node for node in trace_list)}")

# computed visualization
def Visualize_Graph():
    G = nx.DiGraph()
    plt.figure(figsize=(20, 20))
    for node, neighbors in metro_graph.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(node, neighbor, weight=weight)
    pos = nx.spring_layout(G, k=6.7, iterations=67, seed = 6767)
    nx.draw_networkx_nodes(G, pos, node_size=500)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans_serif')
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.3, font_size=5)
    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def main():
    route = Dijkstra(metro_graph, "Polis Station")
    Trace_Dijkstra(route, "Polis Station")
    Visualize_Graph()

if __name__ == '__main__':
    main()