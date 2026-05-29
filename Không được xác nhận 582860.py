# =============================================================================
# TSP Solver: Repeated Nearest Neighbor --> Relocate
# Dataset: att48.tsp (48 capitals of the US)
# Pipeline: Greedy (RNN) -> Local Search (Relocate, Best Improvement)
# Style: Theo buoi 4.ipynb va buoi 5.ipynb
# =============================================================================

import math
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# =============================================================================
# PHAN 1: DOC DU LIEU
# EDGE_WEIGHT_TYPE = ATT => dung cong thuc pseudo-Euclidean
# =============================================================================

class Instance:
    """
    Luu tru thong tin bai toan TSP.
    - nodes: danh sach toa do (x, y) cua cac thanh pho (0-indexed)
    - dist : ma tran khoang cach (ATT pseudo-Euclidean)
    """
    def __init__(self):
        self.nodes = []
        self.dist  = []

    def att_distance(self, u, v):
        """
        Khoang cach ATT (pseudo-Euclidean) theo chuan TSPLIB.
        Cong thuc: rij = ceil(sqrt((xij^2 + yij^2) / 10))
        """
        xu, yu = self.nodes[u]
        xv, yv = self.nodes[v]
        xd = xu - xv
        yd = yu - yv
        r = math.sqrt((xd * xd + yd * yd) / 10.0)
        t = round(r)
        return t + 1 if t < r else t

    def build_distance_matrix(self):
        n = len(self.nodes)
        self.dist = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                d = self.att_distance(i, j)
                self.dist[i][j] = d
                self.dist[j][i] = d


def read_tsp_file(filepath):
    """
    Doc file .tsp dinh dang TSPLIB.
    Ho tro: NODE_COORD_SECTION, bo qua header.
    Tra ve: Instance da co danh sach nodes (0-indexed).
    """
    instance = Instance()
    in_coord_section = False

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line == "NODE_COORD_SECTION":
                in_coord_section = True
                continue
            if line in ("EOF", ""):
                continue
            if line[0].isalpha() and ":" in line:
                continue
            if in_coord_section:
                parts = line.split()
                # node_id (bo qua), x, y
                x, y = float(parts[1]), float(parts[2])
                instance.nodes.append((x, y))

    instance.build_distance_matrix()
    return instance


# =============================================================================
# PHAN 2: HAM TINH TOAN CHUNG
# =============================================================================

def tour_length(tour, dist):
    """
    Tinh tong khoang cach cua mot chu trinh Hamiltonian.
    tour: danh sach 0-indexed, khong lap lai dinh dau.
    Chi phi = sum D[tour[i]][tour[i+1]] + D[tour[-1]][tour[0]]
    """
    n = len(tour)
    total = 0
    for i in range(n):
        total += dist[tour[i]][tour[(i + 1) % n]]
    return total


def is_valid_tour(tour, n):
    """
    Kiem tra tinh dung dan cua tour:
    - Dung n thanh pho
    - Moi thanh pho xuat hien dung 1 lan
    - Khong co subtour
    """
    if len(tour) != n:
        return False, f"Tour co {len(tour)} dinh, can {n}"
    if sorted(tour) != list(range(n)):
        missing = set(range(n)) - set(tour)
        return False, f"Tour thieu cac dinh: {missing}"
    return True, "Hop le"


# =============================================================================
# PHAN 3: GREEDY - REPEATED NEAREST NEIGHBOR
# Xuat phat tu moi thanh pho, chay Nearest Neighbor, giu tour ngan nhat.
# Do phuc tap: O(n^3)
# =============================================================================

def nearest_neighbor(dist, start, n):
    """
    Nearest Neighbor bat dau tu dinh `start`.
    Tra ve: tour (list 0-indexed), tong khoang cach.
    """
    visited = [False] * n
    tour = [start]
    visited[start] = True
    current = start

    for _ in range(n - 1):
        best_dist = math.inf
        best_next = -1
        row = dist[current]
        for j in range(n):
            if not visited[j] and row[j] < best_dist:
                best_dist = row[j]
                best_next = j
        tour.append(best_next)
        visited[best_next] = True
        current = best_next

    return tour, tour_length(tour, dist)


def repeated_nearest_neighbor(instance):
    """
    Chay Nearest Neighbor tu tat ca cac dinh, chon tour tot nhat.
    
    Y tuong: Giam phu thuoc vao diem xuat phat cua single NN.
    Do phuc tap: O(n^3)
    
    Tra ve: (best_tour, best_cost, start_city_chosen)
    """
    n = len(instance.nodes)
    dist = instance.dist

    best_tour = None
    best_cost = math.inf
    best_start = 0

    for start in range(n):
        tour, cost = nearest_neighbor(dist, start, n)
        if cost < best_cost:
            best_cost = cost
            best_tour = tour[:]
            best_start = start

    return best_tour, best_cost, best_start


# =============================================================================
# PHAN 4: LOCAL SEARCH - RELOCATE (Best Improvement)
#
# Y tuong: Lay mot thanh pho ra khoi vi tri hien tai,
#          thu chen vao tat ca vi tri khac, chon vi tri tot nhat.
#
# Chap nhan: Best Improvement - moi vong lap chon move tot nhat trong
#             toan bo neighborhood truoc khi ap dung.
#
# Do phuc tap: O(n^2) moi vong lap
# =============================================================================

def delta_relocate(tour, dist, i, n):
    """
    Voi moi vi tri chen j, tinh delta chi phi khi relocate city tai i sang sau j.
    
    Khi xoa city tai i:
      - Xoa canh (prev_i -> city_i) va (city_i -> next_i)
      - Them canh (prev_i -> next_i)
    
    Khi chen city vao sau vi tri j_adj (chi so trong tour sau khi da xoa i):
      - Xoa canh (tour_new[j_adj] -> tour_new[j_adj+1])
      - Them canh (tour_new[j_adj] -> city_i) va (city_i -> tour_new[j_adj+1])
    
    De tranh nhap nhoang index, ham nay tinh remove_gain mot lan va
    tra ve (remove_gain, city, prev_city, next_city) de goi ham chen rieng.
    """
    prev_i = (i - 1) % n
    next_i = (i + 1) % n
    city = tour[i]
    p    = tour[prev_i]
    nx   = tour[next_i]
    # Chi phi thuan tuy khi xoa city tai i
    remove_gain = -dist[p][city] - dist[city][nx] + dist[p][nx]
    return remove_gain, city, p, nx


def relocate_best_improvement(instance, initial_tour):
    """
    Relocate voi chap nhan Best Improvement.
    
    Moi vong lap:
      1. Duyet tat ca city i: tinh chi phi xoa.
      2. Xay dung tour tam thoi (khong co city i).
      3. Thu chen city i vao moi vi tri j trong tour tam thoi.
      4. Chon move (i, j) co tong delta tot nhat.
      5. Ap dung move, lap lai.

    Dung khi khong co cai thien.
    Tra ve: (improved_tour, final_cost, so_vong_lap)
    """
    dist       = instance.dist
    n          = len(initial_tour)
    tour       = initial_tour[:]
    cost       = tour_length(tour, dist)
    iterations = 0

    while True:
        best_delta = 0   # chi chap nhan cai thien (delta am)
        best_i     = -1
        best_j     = -1  # vi tri chen trong tour_tmp (sau khi xoa i)

        for i in range(n):
            remove_gain, city, p, nx = delta_relocate(tour, dist, i, n)

            # Tour tam thoi: xoa city tai i
            tour_tmp = tour[:i] + tour[i+1:]
            m = n - 1  # so city trong tour_tmp

            # Thu chen city vao moi vi tri j trong tour_tmp
            for j in range(m):
                a = tour_tmp[j]
                b = tour_tmp[(j + 1) % m]
                insert_gain = -dist[a][b] + dist[a][city] + dist[city][b]
                delta = remove_gain + insert_gain

                if delta < best_delta:
                    best_delta = delta
                    best_i = i
                    best_j = j   # vi tri chen trong tour_tmp

        # Khong con cai thien -> dung
        if best_i == -1:
            break

        # Ap dung move tot nhat
        city = tour.pop(best_i)
        tour.insert(best_j + 1, city)

        cost += best_delta
        iterations += 1

    return tour, cost, iterations


# =============================================================================
# PHAN 5: KIEM TRA TINH DUNG DAN
# =============================================================================

def validate_solution(tour, instance, label=""):
    """In ket qua kiem tra tinh hop le cua tour."""
    n = len(instance.nodes)
    valid, msg = is_valid_tour(tour, n)
    status = "✓ HOP LE" if valid else "✗ LOI"
    print(f"  [{label}] Kiem tra: {status} — {msg}")
    return valid


# =============================================================================
# PHAN 6: TRUC QUAN HOA
# =============================================================================

def plot_tour(instance, tour, title, cost, ax, color='steelblue', node_color='white'):
    """Ve tour len mot subplot."""
    coords = instance.nodes
    n = len(tour)

    xs = [coords[i][0] for i in range(n)]
    ys = [coords[i][1] for i in range(n)]

    # Ve cac canh
    for k in range(n):
        u = tour[k]
        v = tour[(k + 1) % n]
        x1, y1 = coords[u]
        x2, y2 = coords[v]
        ax.plot([x1, x2], [y1, y2], color=color, lw=1.2, alpha=0.7)

    # Ve cac dinh
    for idx, city in enumerate(tour):
        x, y = coords[city]
        c = 'tomato' if idx == 0 else node_color
        sz = 120 if idx == 0 else 60
        ax.scatter(x, y, c=c, s=sz, zorder=5, edgecolors='gray', linewidths=0.5)
        ax.text(x, y, str(city + 1), fontsize=6.5,
                ha='center', va='center', color='black', weight='bold')

    ax.set_title(f"{title}\nTong khoang cach: {cost:,}", fontsize=11, pad=8)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2)
    ax.tick_params(labelsize=7)


def plot_comparison(instance, rnn_tour, rnn_cost, rls_tour, rls_cost, rnn_start):
    """Ve bieu do so sanh truoc va sau Local Search."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle(
        "TSP — att48: Repeated Nearest Neighbor  →  Relocate (Best Improvement)",
        fontsize=13, fontweight='bold', y=1.01
    )

    improvement = (rnn_cost - rls_cost) / rnn_cost * 100
    legend_patch = mpatches.Patch(color='tomato', label='Diem xuat phat (city 1-indexed = start+1)')

    plot_tour(instance, rnn_tour,
              f"[Greedy] Repeated Nearest Neighbor\n(Xuat phat tu city {rnn_start + 1})",
              rnn_cost, axes[0], color='steelblue')

    plot_tour(instance, rls_tour,
              f"[Local Search] Sau Relocate\n(Cai thien: {improvement:.2f}%)",
              rls_cost, axes[1], color='seagreen')

    for ax in axes:
        ax.legend(handles=[legend_patch], fontsize=8, loc='lower right')

    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/tsp_result.png', dpi=150, bbox_inches='tight')
    print("  [Bieu do] Da luu: tsp_result.png")


# =============================================================================
# PHAN 7: MAIN — CHAY TOAN BO PIPELINE
# =============================================================================

def main():
    filepath = "att48.tsp"
    print("=" * 60)
    print("  TSP SOLVER: Repeated Nearest Neighbor → Relocate")
    print("  Dataset: att48 (48 capitals of the US)")
    print("=" * 60)

    # ── Doc du lieu ──────────────────────────────────────────
    print("\n[1] Doc du lieu...")
    instance = read_tsp_file(filepath)
    n = len(instance.nodes)
    print(f"    So thanh pho (n) : {n}")
    print(f"    Edge weight type  : ATT (pseudo-Euclidean)")

    # ── Greedy: Repeated Nearest Neighbor ────────────────────
    print("\n[2] Greedy — Repeated Nearest Neighbor...")
    t0 = time.perf_counter()
    rnn_tour, rnn_cost, best_start = repeated_nearest_neighbor(instance)
    t_rnn = (time.perf_counter() - t0) * 1000

    validate_solution(rnn_tour, instance, "RNN")
    print(f"    Xuat phat tot nhat: city {best_start + 1}")
    print(f"    Tong khoang cach  : {rnn_cost:,}")
    print(f"    Thoi gian         : {t_rnn:.2f} ms")

    # ── Local Search: Relocate (Best Improvement) ────────────
    print("\n[3] Local Search — Relocate (Best Improvement)...")
    t0 = time.perf_counter()
    rls_tour, rls_cost, n_iter = relocate_best_improvement(instance, rnn_tour)
    t_rls = (time.perf_counter() - t0) * 1000

    validate_solution(rls_tour, instance, "Relocate")
    print(f"    So vong lap       : {n_iter}")
    print(f"    Tong khoang cach  : {rls_cost:,}")
    print(f"    Thoi gian         : {t_rls:.2f} ms")

    # ── So sanh ──────────────────────────────────────────────
    print("\n[4] Ket qua so sanh:")
    improvement = (rnn_cost - rls_cost) / rnn_cost * 100
    print(f"    {'Phuong phap':<35} {'Khoang cach':>15} {'Thoi gian (ms)':>15}")
    print(f"    {'-'*65}")
    print(f"    {'Repeated Nearest Neighbor':<35} {rnn_cost:>15,} {t_rnn:>15.2f}")
    print(f"    {'RNN + Relocate (Best Improvement)':<35} {rls_cost:>15,} {t_rls:>15.2f}")
    print(f"    {'Cai thien':<35} {improvement:>14.2f}%")
    print(f"    (Optimal att48 = 10,628)")
    gap = (rls_cost - 10628) / 10628 * 100
    print(f"    Gap so voi optimal: {gap:.2f}%")

    # ── Truc quan hoa ─────────────────────────────────────────
    print("\n[5] Tao bieu do...")
    plot_comparison(instance, rnn_tour, rnn_cost, rls_tour, rls_cost, best_start)

    print("\n[6] Thu tu tham quan sau Local Search (city 1-indexed):")
    print("    " + " → ".join(str(c + 1) for c in rls_tour) + f" → {rls_tour[0] + 1}")
    print("\n" + "=" * 60)
    print("  HOAN THANH")
    print("=" * 60)

    return rnn_cost, rls_cost, improvement


if __name__ == "__main__":
    main()
