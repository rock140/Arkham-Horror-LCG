import sys
import pandas as pd
import asyncio
from IPython.display import display, HTML
from collections import Counter
from duckduckgo_search import AsyncDDGS
import gspread

sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSbHAB0LLpdPo_9lbh2a-TG_9mIF-gd_cDtPIKWwUlfl3IpKezf_F0FisKkxZao1Qxgf9cJQEuqR3Jd/pub?gid=1668715228&single=true&output=csv"
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS3dKXeQnL0gMvWZKiEV3ichFA1BHbVnm1X4mjkfdzk4eiFYqFHiMxibc3EYXIhxYWZCO0zUN3GJzuo/pub?output=csv"

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_url)

# Process the DataFrame as needed
all_investigators = {}
for index, row in df.iterrows():
    investigator_name = row['Investigator']
    all_investigators[investigator_name] = {
        'archetype': row['Archetype'],
        'focus': row['Focus'],
        'category': row['Category']
    }

final_available_investigators = []

category_dict = {
    'Blue Collar Professionals': 'Hard-working individuals with practical skills and trades, often facing the horrors of Arkham in their everyday lives.',
    'White Collar Professionals': 'Intellectuals, academics, and professionals who delve into the mysteries of the occult and the unknown.',
    'Scholars and Researchers': 'Dedicated investigators who tirelessly pursue knowledge and study the eldritch secrets lurking in Arkham.',
    'Artists and Performers': 'Creative souls who channel their talents to confront the terrors of Arkham through art, music, and performance.',
    'Explorers and Adventurers': 'Fearless adventurers who brave the dark corners of Arkham, seeking out ancient relics and forbidden knowledge.',
    'Specialists and Consultants': 'Experts in their fields, offering specialized skills and knowledge to combat the supernatural threats that plague Arkham.',
    'Others': 'Outsiders, misfits, and those with unique perspectives who find themselves drawn into the mysteries of Arkham.'
}

def investigator_quiz():
    global final_available_investigators
    
    print("Welcome to the Arkham Horror Investigator Selection Quiz!")
    print("Answer the following questions to discover which investigator best matches your style.\n")

    questions = [
        ("1. When it comes to investigating mysteries in Arkham, what's your preferred approach?\n"
         "   a) I enjoy taking the lead, gathering as many clues as possible to solve the case.\n"
         "   b) I prefer facing monsters head-on, ready to fight whatever comes our way.\n"
         "   c) I like to balance both investigation and combat, adapting to the situation as needed.\n"
         "   d) I prefer providing support to my team, assisting them in various tasks.\n"),
        ("2. Imagine yourself in the eerie streets of Arkham. What role would you play amidst its mysteries?\n"),
        ("3. What archetype do you prefer for your investigator?\n")
    ]

    available_investigators = list(all_investigators.keys())  # Initialize with all investigators

    for i, question in enumerate(questions):
        print(question)
        sys.stdout.flush()  # Force output to be displayed immediately
        
        if i == 0:
            answer_options = ['a', 'b', 'c', 'd']
            focus_mapping = {'a': 'Investigation', 'b': 'Combat', 'c': 'Balanced', 'd': 'Support'}
        elif i == 1:
            # Display available categories along with descriptions
            print("Choose one of the following roles:")
            answer_options = []
            for idx, (category, description) in enumerate(category_dict.items(), start=1):
                option = chr(ord('a') + idx - 1)
                answer_options.append(option)
                print(f"   {option}) {category}: {description}")
        else:
            # Filter available archetypes based on the filtered investigators
            available_archetypes = set(all_investigators[invest]['archetype'] for invest in available_investigators)
            # Generate options based on available archetypes
            answer_options = list(chr(ord('a') + idx) for idx in range(len(available_archetypes)))
            for idx, archetype in enumerate(available_archetypes):
                print(f"   {chr(ord('a') + idx)}) {archetype}")
        
        response = input("Your answer: ").lower()  # Renamed 'answer' to 'response'
        print("Your answer:", response.upper())  # Print user's answer
        
        # Validate the answer
        while response not in answer_options:
            print("Please enter a valid option from the available choices.")
            response = input("Your answer: ").lower()
            print("Your answer:", response.upper())  # Print user's answer
        
        # Map user input to full strings
        if i == 0:
            response = focus_mapping[response]
        elif i == 1:
            category_mapping = {chr(ord('a') + idx): category for idx, category in enumerate(category_dict)}
            response = category_mapping[response]
        else:
            archetype_mapping = {chr(ord('a') + idx): archetype for idx, archetype in enumerate(available_archetypes)}
            response = archetype_mapping[response]
        
        # Filter available investigators based on the user's response
        available_investigators = filter_investigators(response, available_investigators, i)
        
        if not available_investigators:
            print("\nNo matching investigators found. Exiting quiz.")
            return

    final_available_investigators = available_investigators
    print("\nBased on your answers, you match with the following investigator(s):", final_available_investigators)

def filter_investigators(response, available_investigators, i):
    filtered = []
    if i == 0:  # First question's responses
        for investigator in available_investigators:
            if all_investigators[investigator]['focus'] == response:
                filtered.append(investigator)
    elif i == 1:  # Second question's responses
        for investigator in available_investigators:
            if all_investigators[investigator]['category'] == response:
                filtered.append(investigator)
    else:  # Third question's responses
        for investigator in available_investigators:
            if all_investigators[investigator]['archetype'] == response:
                filtered.append(investigator)
    return filtered

def get_investigator_data(sheet_url):
    df = pd.read_csv(sheet_url)
    global final_available_investigators
    investigator_data = df[df['Investigators'].isin(final_available_investigators)]
    return investigator_data

def display_investigator_data(investigator_data):
    # Pandas Styling with alignment adjustment for both headers and data
    styles = [
        {'selector': 'th', 'props': [('text-align', 'left')]},  # Align headers to the left
        {'selector': 'td', 'props': [('text-align', 'left')]}  # Align data to the left
    ]
    styled_table = investigator_data.style.set_caption("Data for the specified investigators") \
        .set_table_styles(styles)
    display(styled_table)

def evaluate_relevance(image_result):
    relevance_score = 0
    
    # Check if the image has a title
    if 'title' in image_result:
        # Increase relevance if the title contains keywords
        if any(keyword in image_result['title'].lower() for keyword in ['arkham', 'horror', 'lcg']):
            relevance_score += 1
    
    # Check if the image has a source URL
    if 'source' in image_result:
        # Increase relevance if the source URL contains certain domains
        relevant_domains = ['arkhamdb.com', 'fantasyflightgames.com','arkhamhorrorlcg.fandom.com/','archivosarkham.com']
        if any(domain in image_result['source'] for domain in relevant_domains):
            relevance_score += 5
    
    # You can add more relevance criteria based on metadata, dimensions, etc.
    
    return relevance_score

async def get_and_display_images(keywords):
    async with AsyncDDGS() as ddgs:
        full_keywords = f"{keywords} Arkham Horror LCG"  # Concatenate "Arkham Horror LCG" with keywords
        results = await ddgs.images(full_keywords, max_results=5)  # Fetch multiple images for better selection
        best_image = None
        highest_relevance = -1  # Initialize with a low relevance score
        
        for result in results:
            # Evaluate relevance based on metadata, title, source, etc.
            relevance = evaluate_relevance(result)
            
            if relevance > highest_relevance:
                highest_relevance = relevance
                best_image = result
        
        if best_image:
            display(HTML(f'<img src="{best_image["image"]}" alt="{keywords}">'))
            print("Image URL:", best_image["image"])  # Print the image URL
        else:
            print("No relevant image found.")

def main():
    investigator_quiz()
    keywords = ', '.join(final_available_investigators)

    # Fetch and display images
    asyncio.create_task(get_and_display_images(keywords))

    # Get data for the specified investigators
    investigator_data = get_investigator_data(sheet_url)

    # Display investigator data
    display_investigator_data(investigator_data)

if __name__ == "__main__":
    main()
