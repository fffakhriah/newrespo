import streamlit as st
import csv
import random
import pandas as pd

# ---------------- READ CSV ---------------- #
def read_csv_to_dict(file_path):
    program_ratings = {}
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            program = row[0]
            ratings = [float(x) for x in row[1:]]
            program_ratings[program] = ratings
    return program_ratings

# ---------------- FITNESS FUNCTION ---------------- #
def fitness_function(schedule, ratings):
    total_rating = 0
    for time_slot, program in enumerate(schedule):
        total_rating += ratings[program][time_slot]
    return total_rating

# ---------------- GA FUNCTIONS ---------------- #
def crossover(schedule1, schedule2):
    crossover_point = random.randint(1, len(schedule1) - 2)
    child1 = schedule1[:crossover_point] + schedule2[crossover_point:]
    child2 = schedule2[:crossover_point] + schedule1[crossover_point:]
    return child1, child2

def mutate(schedule, all_programs):
    mutation_point = random.randint(0, len(schedule) - 1)
    new_program = random.choice(all_programs)
    schedule[mutation_point] = new_program
    return schedule

def genetic_algorithm(ratings, generations, population_size, crossover_rate, mutation_rate, elitism_size):
    all_programs = list(ratings.keys())
    schedule_length = len(all_programs)
    population = [random.sample(all_programs, schedule_length) for _ in range(population_size)]

    for _ in range(generations):
        new_population = []
        population.sort(key=lambda s: fitness_function(s, ratings), reverse=True)
        new_population.extend(population[:elitism_size])

        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population, k=2)
            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1.copy(), parent2.copy()
            if random.random() < mutation_rate:
                child1 = mutate(child1, all_programs)
            if random.random() < mutation_rate:
                child2 = mutate(child2, all_programs)
            new_population.extend([child1, child2])
        population = new_population[:population_size]

    best_schedule = max(population, key=lambda s: fitness_function(s, ratings))
    best_fitness = fitness_function(best_schedule, ratings)
    return best_schedule, best_fitness

# ---------------- STREAMLIT INTERFACE ---------------- #
st.title("📺 Genetic Algorithm TV Scheduling")
st.write("JIE42903 – Evolutionary Computing Assignment")

file_path = st.text_input("Enter CSV File Path", "C:/Users/User/Desktop/CE/program_ratings.csv")

try:
    ratings = read_csv_to_dict(file_path)
    st.success("CSV file loaded successfully!")

    CO_R = st.slider("Crossover Rate (CO_R)", 0.0, 0.95, 0.8)
    MUT_R = st.slider("Mutation Rate (MUT_R)", 0.01, 0.05, 0.02)
    GEN = st.number_input("Generations", min_value=10, max_value=500, value=100)
    POP = st.number_input("Population Size", min_value=10, max_value=200, value=50)
    EL_S = st.number_input("Elitism Size", min_value=1, max_value=5, value=2)

    if st.button("Run Genetic Algorithm"):
        best_schedule, best_fitness = genetic_algorithm(
            ratings, generations=GEN, population_size=POP,
            crossover_rate=CO_R, mutation_rate=MUT_R, elitism_size=EL_S
        )

        df = pd.DataFrame({
            "Time Slot": [f"{hour:02d}:00" for hour in range(6, 6 + len(best_schedule))],
            "Program": best_schedule
        })

        st.subheader("Optimal Schedule")
        st.table(df)
        st.write(f"**Total Ratings:** {best_fitness:.2f}")

except Exception as e:
    st.error(f"Error: {e}")

st.markdown("---")
st.caption("Developed by Rie | Designitech Services | JIE42903 Evolutionary Computing")
