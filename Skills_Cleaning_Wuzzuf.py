import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import re
import csv

# Read the CSV file
dff = pd.read_csv("C:\\Users\\Alaa\\Desktop\\jobs.csv")

# Extract the paragraph column
paragraph_column = dff["Skills"]

# Join all paragraphs into a single string
all_text = " ".join(paragraph_column)

# Merge certain words together
all_text = re.sub(r'\b(power)\s*(bi)\b', r'powerbi', all_text, flags=re.IGNORECASE)
all_text = re.sub(r'\b(programming)\s*(language|languages)\b', r'programming', all_text, flags=re.IGNORECASE)
all_text = re.sub(r'\b(problem)\s*(solving)\b', r'problemsolving', all_text, flags=re.IGNORECASE)

# Tokenize the text into words (split by whitespace)
words = re.findall(r'\b\w+\b', all_text.lower())

# Define words to exclude
words_to_exclude = ["and", "in", "to", "of", "a", "skills", "data", "with", "or", "ability", "the", "knowledge", "s",
                    "ability", "strong", "as", "is", "excellent", "field", "for", "work", "science", "proficiency",
                    "related", "1", "2", "3", "4", "5", "relevant", "detail", "good", "using", "similar", "preferred",
                    "techniques", "such", "g", "plus", "must", "role,", "system", "environment", "including",
                    "advanced", "master", "independently", "at", "familiarity", "high", "multiple", "e", "on",
                     "years", "proven", "tools", "computer", "accounting", "working", "writing",
                    "written", "understanding", "management", "software", "information", "etc", "such"]

# Define a dictionary mapping skills to categories
skill_categories = {
    "excel": "Technical Skills",
    "sql": "Technical Skills",
    "powerbi": "Technical Skills",
    "tableau": "Technical Skills",
    "databases": "Technical Skills",
    "python": "Technical Skills",
    "warehousing": "Technical Skills",
    "etl": "Technical Skills",
    "statistical": "Analytical Skills",
    "reporting": "Analytical Skills",
    "research": "Analytical Skills",
    "communication": "Soft Skills",
    "team": "Soft Skills",
    "problem": "Soft Skills",
    "attention": "Soft Skills",
    "presentation": "Soft Skills",
    "degree": "Qualifications",
    "business": "Domain Knowledge",
    "finance": "Domain Knowledge",
    "marketing": "Domain Knowledge",
    "economics" : "Domain Knowledge",
    "bachelor": "Qualifications",
    "experience": "Qualifications",
    "english": "Qualifications"
}

# Filter out words to exclude
filtered_words = [word for word in words if word not in words_to_exclude]

# Count the frequency of each word
word_counts = Counter(filtered_words)

# Get the most common words and their frequencies
most_common_words = word_counts.most_common(120)

# Write the most common words to a CSV file
filename = "common_words.csv"

with open(filename, "w", newline="", encoding="utf-8") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Word", "Frequency"])
    for word, frequency in most_common_words:
        csv_writer.writerow([word, frequency])

# Read the CSV file
df = pd.read_csv("C:\\Users\\Alaa\\Documents\\New folder\\.venv\\common_words.csv")

skill_category_dict = {}
# Assign categories to each skill
for word in filtered_words:
    # If the word is in the skill_categories dictionary, get its category
    if word in skill_categories:
        skill_category = skill_categories[word]
    else:
        skill_category = "Other"  # Assign "Other" category if not found in the dictionary
    skill_category_dict[word] = skill_category


# Add the skill categories as a new column in the DataFrame
df["Skill Category"] = df["Word"].apply(lambda x: skill_category_dict.get(x.lower(), "Other"))

new_filename = "categorized_words.csv"

# Save the DataFrame to a new CSV file
df.to_csv(new_filename, index=False)
print(f"File '{filename}' saved.")

# Count the total frequency of each skill category
df = df[df['Skill Category'] != "Other"]
category_total_counts = df.groupby('Skill Category').Frequency.sum()

category_total_counts_sorted = category_total_counts.sort_values(ascending=False)
colors = plt.cm.viridis(np.linspace(0, 1, len(category_total_counts_sorted)))

# Plotting
plt.figure(figsize=(12, 7))
category_total_counts_sorted.plot(kind='bar', color=colors)
plt.title("Total Frequency of Skill Categories")
plt.xlabel("Skill Category")
plt.ylabel("Total Frequency")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

unique_categories = df['Skill Category'].unique()

# Create plots for each skill category
for category in unique_categories:
    # Filter dataframe for the current category
    category_df = df[df['Skill Category'] == category]
    
    # Count the occurrences of each skill
    category_counts = category_df['Frequency']
    skills = category_df['Word']
    
    # Sort skills and counts by count in descending order
    sorted_indices = np.argsort(category_counts)[::-1]
    sorted_skills = skills.iloc[sorted_indices]
    sorted_counts = category_counts.iloc[sorted_indices]
    
    # Define colors for each skill
    colors = plt.cm.tab10(np.linspace(0, 1, len(sorted_skills)))
    
    # Plotting
    plt.figure(figsize=(10, 7))
    for i, (skill, count) in enumerate(zip(sorted_skills, sorted_counts)):
        plt.bar(skill, count, color=colors[i])
    plt.title(f"Frequency of Skills - {category}")
    plt.xlabel("Skills")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()
