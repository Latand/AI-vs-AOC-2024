import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

print("Starting analysis...")

# --------------------------------------------------------------------
# SAMPLE JSON LOADING (if needed):
try:
    with open("model_performance.json", "r") as f:
        data = json.load(f)
        print("Successfully loaded model_performance.json")
except FileNotFoundError:
    print("Warning: model_performance.json not found. Using sample data.")
    # Add sample data structure here if needed
    data = {}
# --------------------------------------------------------------------

print("\nConverting data to DataFrame...")
# 1) Convert to a Pandas DataFrame for easier manipulation
# --------------------------------------------------------
rows = []
for day, models in data.items():
    for model_name, parts in models.items():
        for part_key, score in parts.items():
            rows.append(
                {"day": day, "model": model_name, "part": part_key, "score": score}
            )

df = pd.DataFrame(rows)
print(f"Created DataFrame with {len(df)} rows")

# Make sure day is a meaningful sort key
df["day_num"] = df["day"].str.replace("day", "").astype(int)
df = df.sort_values(by="day_num")

print("\nCalculating statistics...")
# 2) Compute total tasks solved per model/part
summary_model_part = df.groupby(["model", "part"])["score"].sum().reset_index()
summary_model_part.rename(columns={"score": "total_solved"}, inplace=True)

# 3) Compute attempts per model/part
attempts_model_part = df.groupby(["model", "part"])["score"].count().reset_index()
attempts_model_part.rename(columns={"score": "num_attempts"}, inplace=True)

# Merge statistics
model_part_stats = pd.merge(
    summary_model_part, attempts_model_part, on=["model", "part"]
)

# 4) Calculate success rates
model_part_stats["success_rate"] = (
    model_part_stats["total_solved"] / model_part_stats["num_attempts"] * 100
)

print("\nCalculating overall performance metrics...")
# 5) Calculate overall performance
overall_model = df.groupby("model")["score"].agg(["sum", "count"]).reset_index()
overall_model["overall_success_rate"] = (
    overall_model["sum"] / overall_model["count"] * 100
)

print("\nGenerating plots...")


# 6) Success rate by model & part plot
def plot_success_rate_by_model_part(model_part_stats):
    plt.figure(figsize=(10, 6))
    sns.barplot(data=model_part_stats, x="model", y="success_rate", hue="part")
    plt.title("Success Rate by Model and Part")
    plt.ylabel("Success Rate (%)")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Part")
    plt.tight_layout()
    plt.savefig("success_rate_by_model_part.png")
    print("Saved plot: success_rate_by_model_part.png")
    plt.close()


plot_success_rate_by_model_part(model_part_stats)


# 7) Overall success rate plot
def plot_overall_success_rate(overall_model):
    plt.figure(figsize=(10, 6))
    sns.barplot(data=overall_model, x="model", y="overall_success_rate")
    plt.title("Overall Success Rate by Model (All Parts Combined)")
    plt.ylabel("Success Rate (%)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("overall_success_rate.png")
    print("Saved plot: overall_success_rate.png")
    plt.close()


plot_overall_success_rate(overall_model)

print("\nAnalyzing results...")
# Print analysis results
print("\n=== Model Performance Statistics ===")
print("\nTotal solved + success rates per model & part:")
print(model_part_stats.to_string())

print("\nOverall success rate per model (both parts):")
print(overall_model[["model", "overall_success_rate"]].to_string())

best_model = overall_model.loc[overall_model["overall_success_rate"].idxmax()]
print(
    f"\nBest performing model: {best_model['model']} with {best_model['overall_success_rate']:.1f}% success rate"
)

day_sums = df.groupby("day")["score"].sum().reset_index()
best_day = day_sums.loc[day_sums["score"].idxmax()]
print(f"\nMost successful day: {best_day['day']} with {best_day['score']} total solves")

worst_day = day_sums.loc[day_sums["score"].idxmin()]
print(
    f"Most challenging day: {worst_day['day']} with {worst_day['score']} total solves"
)

part_variance = model_part_stats.groupby("part")["success_rate"].var().reset_index()
print("\nVariance in success rates by part:")
print(part_variance.to_string())

print("\nGenerating daily scores distribution plot...")


def plot_daily_scores_distribution(df):
    daily_model_sums = df.groupby(["day_num", "model"])["score"].sum().reset_index()
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=daily_model_sums, x="day_num", y="score", hue="model", marker="o")
    plt.title("Distribution of Daily Scores by Model")
    plt.xlabel("Day")
    plt.ylabel("Total Tasks Solved (per day)")
    plt.xticks(daily_model_sums["day_num"].unique())
    plt.legend(title="Model", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig("daily_scores_distribution.png")
    print("Saved plot: daily_scores_distribution.png")
    plt.close()


plot_daily_scores_distribution(df)

print("\nRanking models by overall success rate:")
overall_model_sorted = overall_model.sort_values(
    by="overall_success_rate", ascending=False
)
print(overall_model_sorted[["model", "overall_success_rate"]].to_string())

print("\nAnalysis complete!")
