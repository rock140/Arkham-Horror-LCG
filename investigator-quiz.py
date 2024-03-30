import sys
import pandas as pd
from IPython.display import display
from collections import Counter
from duckduckgo_search import AsyncDDGS
from IPython.display import display, HTML 

all_investigators = {
    "Ashcan Pete": {"archetype": "The Drifter", "focus": "Balanced", "category": "Blue Collar Professionals"},
    "Ashcan Pete (Parallel)": {"archetype": "The Drifter", "focus": "Balanced", "category": "Blue Collar Professionals"},
    "Bob Jenkins": {"archetype": "The Salesman", "focus": "Support", "category": "White Collar Professionals"},
    "Calvin Wright": {"archetype": "The Haunted", "focus": "Balanced", "category": "Scholars and Researchers"},
    "Darrell Simmons": {"archetype": "The Photographer", "focus": "Investigation", "category": "Artists and Performers"},
    "Hank Samson": {"archetype": "The Farmhand", "focus": "Combat", "category": "Blue Collar Professionals"},
    "Patrice Hathaway": {"archetype": "The Violinist", "focus": "Balanced", "category": "Artists and Performers"},
    "Rita Young": {"archetype": "The Athlete", "focus": "Balanced", "category": "Others"},
    "Silas Marsh": {"archetype": "The Sailor", "focus": "Balanced", "category": "Scholars and Researchers"},
    "Stella Clark": {"archetype": "The Letter Carrier", "focus": "Balanced", "category": "Explorers and Adventurers"},
    "Wendy Adams": {"archetype": "The Urchin", "focus": "Balanced", "category": "Explorers and Adventurers"},
    "Wendy Adams (Parallel)": {"archetype": "The Urchin", "focus": "Balanced", "category": "Explorers and Adventurers"},
    "William Yorick": {"archetype": "The Gravedigger", "focus": "Combat", "category": "Blue Collar Professionals"},
    "Amanda Sharpe": {"archetype": "The Student", "focus": "Balanced", "category": "Others"},
    "Daisy Walker": {"archetype": "The Librarian", "focus": "Investigation", "category": "Scholars and Researchers"},
    "Daisy Walker (Parallel)": {"archetype": "The Librarian", "focus": "Investigation", "category": "Scholars and Researchers"},
    "Harvey Walters": {"archetype": "The Professor", "focus": "Investigation", "category": "Scholars and Researchers"},
    "Joe Diamond": {"archetype": "The Private Investigator", "focus": "Support", "category": "White Collar Professionals"},
    "Kate Winthrop": {"archetype": "The Scientist", "focus": "Investigation", "category": "Scholars and Researchers"},
    "Mandy Thompson": {"archetype": "The Researcher", "focus": "Balanced", "category": "Others"},
    "Minh Thi Phan": {"archetype": "The Secretary", "focus": "Investigation", "category": "Specialists and Consultants"},
    "Norman Withers": {"archetype": "The Astronomer", "focus": "Investigation", "category": "Scholars and Researchers"},
    "Rex Murphy": {"archetype": "The Reporter", "focus": "Investigation", "category": "White Collar Professionals"},
    "Rex Murphy (Parallel)": {"archetype": "The Reporter", "focus": "Investigation", "category": "White Collar Professionals"},
    "Ursula Downs": {"archetype": "The Explorer", "focus": "Investigation", "category": "Explorers and Adventurers"},
    "Vincent Lee": {"archetype": "The Doctor", "focus": "Support", "category": "White Collar Professionals"},
    "Alessandra Zorzi": {"archetype": "The Countess", "focus": "Support", "category": "Others"},
    "Finn Edwards": {"archetype": "The Bootlegger", "focus": "Combat", "category": "Blue Collar Professionals"},
    "Jenny Barnes": {"archetype": "The Dilettante", "focus": "Support", "category": "White Collar Professionals"},
    "Kymani Jones": {"archetype": "Security Consultant", "focus": "Combat", "category": "Blue Collar Professionals"},
    "Monterey Jack": {"archetype": "The Archeologist", "focus": "Investigation", "category": "Explorers and Adventurers"},
    "Monterey Jack (Parallel)": {"archetype": "The Archeologist", "focus": "Investigation", "category": "Explorers and Adventurers"},
    "Preston Fairmount": {"archetype": "The Millionaire", "focus": "Support", "category": "Specialists and Consultants"},
    "Sefina Rousseau": {"archetype": "The Painter", "focus": "Balanced", "category": "Artists and Performers"},
    "Skids O'Toole": {"archetype": "The Ex-Con", "focus": "Combat", "category": "Blue Collar Professionals"},
    "Skids O'Toole (Parallel)": {"archetype": "The Ex-Con", "focus": "Combat", "category": "Blue Collar Professionals"},
    "Tony Morgan": {"archetype": "The Bounty Hunter", "focus": "Combat", "category": "Blue Collar Professionals"},
    "Trish Scarborough": {"archetype": "The Spy", "focus": "Investigation", "category": "White Collar Professionals"},
    "Winnifred Habbamock": {"archetype": "The Aviatrix", "focus": "Support", "category": "Others"},
    "Carolyn Fern": {"archetype": "The Psychologist", "focus": "Support", "category": "White Collar Professionals"},
    "Carson Sinclair": {"archetype": "The Butler", "focus": "Support", "category": "White Collar Professionals"},
    "Daniela Reyes": {"archetype": "The Mechanic", "focus": "Combat", "category": "Blue Collar Professionals"},
    "Leo Anderson": {"archetype": "The Expedition Leader", "focus": "Support", "category": "White Collar Professionals"},
    "Mark Harrigan": {"archetype": "The Soldier", "focus": "Combat", "category": "Blue Collar Professionals"},
    "Nathanial Cho": {"archetype": "The Boxer", "focus": "Combat", "category": "Blue Collar Professionals"},
    "Sister Mary": {"archetype": "The Nun", "focus": "Support", "category": "White Collar Professionals"},
    "Tommy Muldoon": {"archetype": "The Rookie Cop", "focus": "Support", "category": "Blue Collar Professionals"},
    "Roland Banks": {"archetype": "The Fed", "focus": "Investigation", "category": "White Collar Professionals"},
    "Roland Banks (Parallel)": {"archetype": "The Fed", "focus": "Investigation", "category": "White Collar Professionals"},
    "Wilson Richards": {"archetype": "The Handyman", "focus": "Support", "category": "Others"},
    "Zoey Samaras": {"archetype": "The Chef", "focus": "Combat", "category": "Blue Collar Professionals"},
    "Zoey Samaras (Parallel)": {"archetype": "The Chef", "focus": "Combat", "category": "Blue Collar Professionals"},
    "Agnes Baker": {"archetype": "The Waitress", "focus": "Combat", "category": "Blue Collar Professionals"},
    "Agnes Baker (Parallel)": {"archetype": "The Waitress", "focus": "Combat", "category": "Blue Collar Professionals"},
    "Akachi Onyele": {"archetype": "The Shaman", "focus": "Support", "category": "Others"},
    "Amina Zidane": {"archetype": "The Operator", "focus": "Support", "category": "Others"},
    "Dexter Drake": {"archetype": "The Magician", "focus": "Support", "category": "Artists and Performers"},
    "Diana Stanley": {"archetype": "The Redeemed Cultist", "focus": "Support", "category": "Others"},
    "Father Mateo": {"archetype": "The Priest", "focus": "Support", "category": "Others"},
    "Gloria Goldberg": {"archetype": "The Writer", "focus": "Investigation", "category": "Scholars and Researchers"},
    "Jaqueline Fine": {"archetype": "The Psychic", "focus": "Support", "category": "Others"},
    "Jim Culver": {"archetype": "The Musician", "focus": "Combat", "category": "Blue Collar Professionals"},
    "Jim Culver (Parallel)": {"archetype": "The Musician", "focus": "Combat", "category": "Blue Collar Professionals"},
    "Kōhaku Narukami": {"archetype": "The Folklorist", "focus": "Balanced", "category": "Explorers and Adventurers"},
    "Lily Chen": {"archetype": "The Martial Artist", "focus": "Combat", "category": "Blue Collar Professionals"},
    "Luke Robinson": {"archetype": "The Dreamer", "focus": "Balanced", "category": "Scholars and Researchers"},
    "Marie Lambeau": {"archetype": "The Entertainer", "focus": "Support", "category": "Artists and Performers"},
    "Charlie Kane": {"archetype": "The Politician", "focus": "Support", "category": "White Collar Professionals"},
    "Lola Hayes": {"archetype": "The Actress", "focus": "Balanced", "category": "Artists and Performers"},
    "Subject 5U-21": {"archetype": "The Anomaly", "focus": "Balanced", "category": "Others"}
}

final_available_investigators = []

def investigator_quiz():
    global final_available_investigators
    
    print("Welcome to the Arkham Horror Investigator Personality Quiz!")
    print("Answer the following questions to discover which investigator best matches your style.\n")

    questions = [
        ("1. When it comes to investigating mysteries in Arkham, what's your preferred approach?\n"
         "   a) I enjoy taking the lead, gathering as many clues as possible to solve the case.\n"
         "   b) I prefer facing monsters head-on, ready to fight whatever comes our way.\n"
         "   c) I like to balance both investigation and combat, adapting to the situation as needed.\n"
         "   d) I prefer providing support to my team, assisting them in various tasks.\n"),
        ("2. Which type of investigator role resonates with you the most?\n"),
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
            # Filter available categories based on the filtered investigators
            available_categories = set(all_investigators[invest]['category'] for invest in available_investigators)
            # Generate options based on available categories
            answer_options = list(chr(ord('a') + idx) for idx in range(len(available_categories)))
            for idx, category in enumerate(available_categories):
                print(f"   {chr(ord('a') + idx)}) {category}")
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
            category_mapping = {chr(ord('a') + idx): category for idx, category in enumerate(available_categories)}
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
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSbHAB0LLpdPo_9lbh2a-TG_9mIF-gd_cDtPIKWwUlfl3IpKezf_F0FisKkxZao1Qxgf9cJQEuqR3Jd/pub?gid=1668715228&single=true&output=csv"
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
            
if __name__ == "__main__":
    while True:
        investigator_quiz()
        keywords = ', '.join(final_available_investigators)

        # Get and display the first image for the specified keywords
        await get_and_display_images(keywords)

        # Get data for the specified investigators
        investigator_data = get_investigator_data(sheet_url)

        # Display investigator data
        display_investigator_data(investigator_data)

        # Prompt user if they are satisfied
        satisfaction = input("Are you satisfied with the provided information? (yes/no): ").lower()
        if satisfaction == 'yes':
            break