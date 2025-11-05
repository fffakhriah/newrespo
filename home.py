# ================================
# 🏠 HOME / MAIN PROGRAM
# ================================
from ga_genetic import run_three_trials  # Import GA logic from the other file

# ---------- SETTINGS ----------
CSV_PATH = r"C:\Users\User\Desktop\CE\program_ratings.csv"  # Your file path
GENERATIONS = 200
POPULATION_SIZE = 100
# Example parameter sets for 3 trials
param_sets = [
    (0.8, 0.02),
    (0.9, 0.04),
    (0.7, 0.01)
]
# -------------------------------

if __name__ == "__main__":
    print("\n🚀 Starting Genetic Algorithm TV Scheduling...\n")

    results = run_three_trials(
        CSV_PATH,
        param_sets,
        generations=GENERATIONS,
        pop_size=POPULATION_SIZE,
    )

    print("\n📊 Summary of 3 trials:")
    for r in results:
        print(f"Trial {r['trial']}: CO_R={r['co_r']}, MUT_R={r['mut_r']}, Score={round(r['score'],4)}")

    print("\n✅ All trials completed successfully!")
