def validate_population(history):
    if len(history) < 2:
        print("Not enough experiment data.")
        return

    first = history[0]
    last = history[-1]

    print("\n=== EVOLUTION REPORT ===")

    print("Initial population:", first["population"])
    print("Final population:", last["population"])

    print("Initial fitness:", round(first["average_fitness"], 2))
    print("Final fitness:", round(last["average_fitness"], 2))

    print("Initial age:", round(first["average_age"], 2))
    print("Final age:", round(last["average_age"], 2))

    print("Maximum generation:", last["max_generation"])

    if last["average_age"] > first["average_age"]:
        print("Survival duration increased.")
    else:
        print("No survival improvement detected.")  