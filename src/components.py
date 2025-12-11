import streamlit as st
import random
import time
from typing import Dict
from src.character import Character
from copy import copy

def character_sheet(character: Character):
    """Displays the full character sheet in a tabbed interface."""
    
    tabs = st.tabs(["Core", "Skills", "Combat", "Background", "Notes"])

    with tabs[0]:
        core_info(character)
        meta_currency_manager(character)
        conditions_manager(character)

    with tabs[1]:
        skills_display(character)

    with tabs[2]:
        # Placeholder for combat-related info
        st.header("Combat Info")
        st.text("Combat section coming soon!")

    with tabs[3]:
        background_display(character)

    with tabs[4]:
        notes_display(character)


def core_info(character: Character):
    # Allow editing of core character details
    character.name = st.text_input("Name", value=character.name)
    character.pronouns = st.text_input("Pronouns", value=character.pronouns)
    character.concept = st.text_input("Concept", value=character.concept)
    
    st.divider() 
    
    cols = st.columns(5)
    # Use a copy of the items to avoid issues with changing dict size during iteration if that were to happen
    for i, (ability, value) in enumerate(character.abilities.items()):
        with cols[i]:
            new_value = st.number_input(ability, value=value, min_value=0, step=1, key=f"ability_{ability}")
            character.abilities[ability] = new_value

def meta_currency_manager(character: Character):
    st.divider() 
    st.header("Meta-Currency")
    cols = st.columns(2)
    with cols[0]:
        new_intervention = st.number_input("Intervention Tokens", value=character.intervention_tokens, min_value=0, step=1)
        character.intervention_tokens = new_intervention
    with cols[1]:
        new_hero = st.number_input("Hero Tokens", value=character.hero_tokens, min_value=0, step=1)
        character.hero_tokens = new_hero

def conditions_manager(character: Character):
    st.divider() 
    st.header("Conditions")
    cols = st.columns(3)
    conditions_list = list(character.conditions.keys())
    for i in range(0, len(conditions_list), 3):
        with cols[0]:
            if i < len(conditions_list):
                character.conditions[conditions_list[i]] = st.checkbox(conditions_list[i], value=character.conditions[conditions_list[i]])
        with cols[1]:
            if i + 1 < len(conditions_list):
                character.conditions[conditions_list[i+1]] = st.checkbox(conditions_list[i+1], value=character.conditions[conditions_list[i+1]])
        with cols[2]:
            if i + 2 < len(conditions_list):
                character.conditions[conditions_list[i+2]] = st.checkbox(conditions_list[i+2], value=character.conditions[conditions_list[i+2]])


def skills_display(character: Character):
    st.header("Skills")

    # --- Add New Skill ---
    with st.expander("Add New Skill"):
        all_skills = []
        skill_categories_for_add = {
            "Crafting & Technical": ["Electronics", "Mechanics", "Engineering", "Computer", "Comms", "Gravitics", "Demolitions", "Screens"],
            "Exploration & Survival": ["Athletics", "Zero-G", "Survival", "Recon", "Navigation", "Grav Vehicle", "Wheeled Vehicle", "Tracked Vehicle", "Riding", "Winged Aircraft", "Rotor Aircraft", "Motorboats", "Ocean Ships", "Sailing Ships", "Submarine", "Mole"],
            "Social & Interpersonal": ["Leadership", "Instruction", "Barter", "Diplomacy", "Etiquette", "Streetwise", "Intimidation", "Deception", "Seduction", "Performance", "Empathy", "Willpower"],
            "Lore & Knowledge": ["Ecology", "Genetics", "Botanics", "Zoology", "Mathematics", "Chemistry", "Geology", "Physics", "History", "Psychology", "Economics", "Sociology", "Astronomy", "First Aid", "Surgery", "Pharmacology", "Linguistics", "Military Strategy", "Combat Tactics", "Veterinary Medicine"],
            "Combat": ["Archery", "Bludgeoning Weapons", "Natural Weapons", "Piercing Weapons", "Slashing Weapons", "Shotgun", "Slug Pistol", "Slug Rifle", "Energy Pistol", "Energy Rifle", "Heavy Weapons", "Mounted Weapons", "Battle Dress"],
        }
        for category in skill_categories_for_add.values():
            all_skills.extend(category)
        
        # Filter out skills the character already has
        available_skills = [skill for skill in all_skills if skill not in character.skills]
        
        new_skills_to_add = st.multiselect("Select skills to add", available_skills)
        
        if st.button("Add Selected Skills"):
            for skill in new_skills_to_add:
                if skill not in character.skills:
                    character.skills[skill] = 1 # Add new skill with a default value of 1
            st.success("Skills added! You can now edit their values below.")
            st.rerun()

    st.divider()

    # Group skills by category for better display
    skill_categories = {
        "Crafting & Technical": ["Electronics", "Mechanics", "Engineering", "Computer", "Comms", "Gravitics", "Demolitions", "Screens"],
        "Exploration & Survival": ["Athletics", "Zero-G", "Survival", "Recon", "Navigation", "Grav Vehicle", "Wheeled Vehicle", "Tracked Vehicle", "Riding", "Winged Aircraft", "Rotor Aircraft", "Motorboats", "Ocean Ships", "Sailing Ships", "Submarine", "Mole"],
        "Social & Interpersonal": ["Leadership", "Instruction", "Barter", "Diplomacy", "Etiquette", "Streetwise", "Intimidation", "Deception", "Seduction", "Performance", "Empathy", "Willpower"],
        "Lore & Knowledge": ["Ecology", "Genetics", "Botanics", "Zoology", "Mathematics", "Chemistry", "Geology", "Physics", "History", "Psychology", "Economics", "Sociology", "Astronomy", "First Aid", "Surgery", "Pharmacology", "Linguistics", "Military Strategy", "Combat Tactics", "Veterinary Medicine"],
        "Combat": ["Archery", "Bludgeoning Weapons", "Natural Weapons", "Piercing Weapons", "Slashing Weapons", "Shotgun", "Slug Pistol", "Slug Rifle", "Energy Pistol", "Energy Rifle", "Heavy Weapons", "Mounted Weapons", "Battle Dress"],
    }

    for category, skills_in_category in skill_categories.items():
        # Only show the expander if the character has any skills in that category
        if any(skill in character.skills for skill in skills_in_category):
            with st.expander(category, expanded=True):
                skills_to_show = [skill for skill in skills_in_category if skill in character.skills]
                for skill in skills_to_show:
                    cols = st.columns([3, 2])
                    with cols[0]:
                        st.write(skill)
                    with cols[1]:
                        # Clamp the value to be >= 0 to prevent Streamlit error
                        current_value = max(0, character.skills.get(skill, 0))
                        new_skill_value = st.number_input(
                            label=f"_{skill}_val", # Underscore to ensure unique key
                            value=current_value, 
                            min_value=0, 
                            max_value=10,
                            step=1,
                            label_visibility="collapsed"
                        )
                        character.skills[skill] = new_skill_value


def background_display(character: Character):
    st.header("Background")
    st.write(f"**Homeworld:** {character.homeworld}")
    st.write(f"**Upbringing:** {character.upbringing}")
    
    st.subheader("Lifepaths")
    for path in character.lifepaths:
        st.write(f"- {path}")
        
    st.subheader("Trait Pairs")
    for trait_pair in character.trait_pairs:
        if isinstance(trait_pair, dict) and 'positive' in trait_pair and 'negative' in trait_pair:
            st.write(f"- {trait_pair['positive']} / {trait_pair['negative']}")
        else:
            # Fallback for malformed data to prevent crash
            st.write(f"- (Invalid trait data: {trait_pair})")

    st.subheader("Beliefs, Instincts & Goals")
    character.beliefs = st.text_area("Beliefs", value=character.beliefs, height=100)
    character.instincts = st.text_area("Instincts", value=character.instincts, height=100)
    character.goals = st.text_area("Goals", value=character.goals, height=100)


def notes_display(character: Character):
    st.header("Inventory & Notes")
    character.inventory = st.text_area("Inventory", value="\n".join(character.inventory)).split("\n")
    character.notes = st.text_area("Notes", value=character.notes, height=200)


def character_creation_wizard():
    """A multi-step wizard for creating a new character."""
    if 'creation_step' not in st.session_state:
        st.session_state.creation_step = 1
        st.session_state.new_character = Character()

    # --- DATA FROM RULEBOOK ---
    homeworlds = {
        "Core World": "Wealthy, stable, bureaucratic.",
        "Frontier Colony": "Harsh survival, scarce resources.",
        "Trade Hub": "A crossroads of cultures and species.",
        "Industrial World": "Factories, shipyards, endless labor.",
        "Exotic World": "Harsh alien ecology or unusual traditions."
    }
    upbringings = {
        "Family": "Kinship and obligation.",
        "Institution": "Monastery, academy, guild, or military school.",
        "Street": "Hustling, surviving, improvising.",
        "Machine": "Raised among robots, AIs, or cybernetic systems."
    }
    lifepaths = {
        "Soldier": {"skills": ["Combat Tactics", "Slug Rifle", "First Aid"], "trait": "Hardened+Haunted"},
        "Marine": {"skills": ["Zero-G", "Energy Rifle", "Battle Dress"], "trait": "Loyal+Reckless"},
        "Officer": {"skills": ["Leadership", "Diplomacy", "Combat Tactics"], "trait": "Charismatic+Burdened"},
        "Mercenary": {"skills": ["Intimidation", "Heavy Weapons", "Streetwise"], "trait": "Ruthless+Pragmatic"},
        "Security Agent": {"skills": ["Recon", "Deception", "Slug Pistol"], "trait": "Watchful+Paranoid"},
        "Spacer": {"skills": ["Navigation", "Zero-G", "Mechanics"], "trait": "Starwise+Jaded"},
        "Scout": {"skills": ["Recon", "Survival", "Navigation"], "trait": "Curious+Lonely"},
        "Pilot": {"skills": ["Grav Vehicle", "Zero-G", "Comms"], "trait": "Hotshot+Steady Hand"},
        "Explorer": {"skills": ["Zoology", "Botany", "Survival"], "trait": "Bold+Obsessive"},
        "Prospector": {"skills": ["Geology", "Mechanics", "Wheeled Vehicle"], "trait": "Optimist+Greedy"},
        "Scholar": {"skills": ["History", "Linguistics", "Mathematics"], "trait": "Inquisitive+Detached"},
        "Physician": {"skills": ["First Aid", "Surgery", "Pharmacology"], "trait": "Compassionate+Clinical"},
        "Scientist": {"skills": ["Physics", "Chemistry", "Computer"], "trait": "Brilliant+Absent-Minded"},
        "Xenobiologist": {"skills": ["Zoology", "Ecology", "Genetics"], "trait": "Enthralled+Cautious"},
        "Historian": {"skills": ["History", "Sociology", "Astronomy"], "trait": "Traditionalist+Revisionist"},
        "Diplomat": {"skills": ["Diplomacy", "Etiquette", "Empathy"], "trait": "Silver-Tongued+Compromised"},
        "Trader": {"skills": ["Barter", "Economics", "Streetwise"], "trait": "Shrewd+Opportunist"},
        "Performer": {"skills": ["Performance", "Seduction", "Etiquette"], "trait": "Charming+Self-Destructive"},
        "Priest": {"skills": ["Empathy", "Willpower", "Sociology"], "trait": "Devout+Doubtful"},
        "Politician": {"skills": ["Leadership", "Diplomacy", "Deception"], "trait": "Ambitious+Jaded"},
        "Criminal": {"skills": ["Streetwise", "Deception", "Slug Pistol"], "trait": "Connected+Wanted"},
        "Smuggler": {"skills": ["Navigation", "Recon", "Barter"], "trait": "Bold+Two-Faced"},
        "Hacker": {"skills": ["Computer", "Electronics", "Deception"], "trait": "Elusive+Obsessed"},
        "Drifter": {"skills": ["Survival", "Athletics", "Streetwise"], "trait": "Lucky+Desperate"},
        "Rebel": {"skills": ["Intimidation", "Leadership", "Demolitions"], "trait": "Zealous+Burned Out"},
    }


    st.header(f"Character Creation: Step {st.session_state.creation_step}")
    char = st.session_state.new_character

    # --- STEP 1: Basic Info ---
    if st.session_state.creation_step == 1:
        st.subheader("Basic Information")
        char.name = st.text_input("Name", value=char.name)
        char.pronouns = st.text_input("Pronouns", value=char.pronouns)
        char.concept = st.text_input("Concept", value=char.concept)

    # --- STEP 2: Homeworld & Upbringing ---
    elif st.session_state.creation_step == 2:
        st.subheader("Homeworld")
        char.homeworld = st.selectbox("Choose your Homeworld", list(homeworlds.keys()))
        st.write(homeworlds[char.homeworld])
        
        st.subheader("Upbringing")
        char.upbringing = st.selectbox("Choose your Upbringing", list(upbringings.keys()))
        st.write(upbringings[char.upbringing])

        st.subheader("Allocate Abilities")
        st.write("You have 8 points to distribute between Will and Health (min 2, max 6).")
        
        will = st.slider("Will", min_value=2, max_value=6, value=char.abilities["Will"])
        health = 8 - will
        st.metric("Health", health)
        
        if health < 2 or health > 6:
            st.error("Health must also be between 2 and 6.")
        else:
            char.abilities["Will"] = will
            char.abilities["Health"] = health


    # --- STEP 3: Lifepaths ---
    elif st.session_state.creation_step == 3:
        st.subheader("Lifepaths")
        st.write("Select 2-4 lifepaths that define your character's history.")
        
        selected_lifepaths = st.multiselect("Choose Lifepaths", list(lifepaths.keys()), default=char.lifepaths)
        char.lifepaths = selected_lifepaths
        
        if len(char.lifepaths) > 4:
            st.warning("You can select a maximum of 4 lifepaths.")
        
        # Assign trait pairs from the first two lifepaths
        char.trait_pairs = []
        if len(char.lifepaths) > 0:
            trait_pair_str = lifepaths[char.lifepaths[0]]["trait"]
            positive, negative = trait_pair_str.split('+')
            char.trait_pairs.append({"positive": positive, "negative": negative})
        if len(char.lifepaths) > 1:
            trait_pair_str = lifepaths[char.lifepaths[1]]["trait"]
            positive, negative = trait_pair_str.split('+')
            char.trait_pairs.append({"positive": positive, "negative": negative})

        st.write("Your selected lifepaths:")
        st.write(char.lifepaths)
        st.write("Your trait pairs:")
        for trait in char.trait_pairs:
            st.write(f"- {trait['positive']} / {trait['negative']}")


    # --- STEP 4: Skills ---
    elif st.session_state.creation_step == 4:
        st.subheader("Distribute Skill Points")

        # Calculate total skill points
        total_skill_points = 2  # From Homeworld
        total_skill_points += 3  # From Upbringing
        total_skill_points += len(char.lifepaths) * 3

        # Reset skills if this is the first time entering step 4 with these lifepaths
        if "lifepaths_at_skill_step" not in st.session_state or st.session_state.lifepaths_at_skill_step != char.lifepaths:
            char.skills = {skill: 0 for skill in char.skills}
            for path in char.lifepaths:
                for skill in lifepaths[path]["skills"]:
                    char.skills[skill] += 1
            st.session_state.lifepaths_at_skill_step = char.lifepaths.copy()


        # Calculate spent points
        points_spent = sum(char.skills.values())
        points_remaining = total_skill_points - points_spent

        st.metric("Skill Points Remaining", points_remaining)

        if points_remaining < 0:
            st.error(f"You have spent {abs(points_remaining)} too many skill points!")

        skill_categories = {
            "Crafting & Technical": ["Electronics", "Mechanics", "Engineering", "Computer", "Comms", "Gravitics", "Demolitions", "Screens"],
            "Exploration & Survival": ["Athletics", "Zero-G", "Survival", "Recon", "Navigation", "Grav Vehicle", "Wheeled Vehicle", "Tracked Vehicle", "Riding", "Winged Aircraft", "Rotor Aircraft", "Motorboats", "Ocean Ships", "Sailing Ships", "Submarine", "Mole"],
            "Social & Interpersonal": ["Leadership", "Instruction", "Barter", "Diplomacy", "Etiquette", "Streetwise", "Intimidation", "Deception", "Seduction", "Performance", "Empathy", "Willpower"],
            "Lore & Knowledge": ["Ecology", "Genetics", "Botanics", "Zoology", "Mathematics", "Chemistry", "Geology", "Physics", "History", "Psychology", "Economics", "Sociology", "Astronomy", "First Aid", "Surgery", "Pharmacology", "Linguistics", "Military Strategy", "Combat Tactics", "Veterinary Medicine"],
            "Combat": ["Archery", "Bludgeoning Weapons", "Natural Weapons", "Piercing Weapons", "Slashing Weapons", "Shotgun", "Slug Pistol", "Slug Rifle", "Energy Pistol", "Energy Rifle", "Heavy Weapons", "Mounted Weapons", "Battle Dress"],
        }

        for category, skills_in_category in skill_categories.items():
            with st.expander(category):
                for skill in skills_in_category:
                    char.skills[skill] = st.number_input(skill, min_value=0, max_value=5, value=char.skills[skill], key=f"skill_{skill}")

    # --- STEP 5: Details ---
    elif st.session_state.creation_step == 5:
        st.subheader("Beliefs, Instincts, and Goals")
        char.beliefs = st.text_area("Beliefs", value=char.beliefs)
        char.instincts = st.text_area("Instincts", value=char.instincts)
        char.goals = st.text_area("Initial Goal", value=char.goals)

    # --- STEP 6: Review ---
    elif st.session_state.creation_step == 6:
        st.subheader("Review Your Character")
        # Display a summary of the character
        st.json(char.to_json())


    # --- Navigation ---
    st.divider()
    cols = st.columns([1, 1, 1, 1])
    with cols[0]:
        if st.session_state.creation_step > 1:
            if st.button("Previous"):
                st.session_state.creation_step -= 1
                st.rerun()
    with cols[3]:
        if st.session_state.creation_step < 6:
            if st.button("Next"):
                # Add validation logic here before going to the next step
                st.session_state.creation_step += 1
                st.rerun()
        else:
            if st.button("Finish & Save"):
                # Finalize character and save to session state
                st.session_state.character = char
                st.success(f"Character '{char.name}' created!")
                
                # Clean up creation state
                if 'creation_step' in st.session_state:
                    del st.session_state.creation_step
                if 'new_character' in st.session_state:
                    del st.session_state.new_character
                if 'lifepaths_at_skill_step' in st.session_state:
                    del st.session_state.lifepaths_at_skill_step

                st.info("Switching to Play Mode...")
                st.switch_page("pages/2_📝_Edit_Character.py")

def play_mode_sheet(character: Character):
    """Displays a simplified sheet for physical play with skill test tracking."""
    st.header(f"{character.name}")
    st.subheader(f"Concept: {character.concept}")
    st.divider()

    st.header("Skill Test")

    # --- Skill and Ability Selection ---
    skill_list = ["None"] + sorted(list(character.skills.keys()))
    selected_skill = st.selectbox("Choose a skill to test", skill_list)

    ability_list = list(character.abilities.keys())
    selected_ability = st.selectbox("Choose the governing ability", ability_list)

    # --- Dice Calculation ---
    num_dice = 0
    if selected_skill != "None" and selected_ability is not None:
        ability_value = character.get_ability_value(selected_ability)
        skill_value = character.get_skill_value(selected_skill)

        num_dice = ability_value + skill_value

        if skill_value == 0:
            st.warning("This is a Beginner's Luck test! The obstacle is doubled.")

        # Apply penalties from conditions
        penalty = 0
        # Simplified penalty rules for play mode, check rulebook for specifics
        if character.conditions.get("Tired") and selected_skill in ["Athletics", "Zero-G"] + [s for s in skill_list if "Weapon" in s or "Combat" in s]:
            penalty += 1
        if character.conditions.get("Sick") or character.conditions.get("Hurt"):
            penalty += 1
        if character.conditions.get("Mentally Fractured"):
            penalty += 1
        if character.conditions.get("Severely Injured"):
            penalty += 2
        
        if penalty > 0:
            st.warning(f"Applying -{penalty}D penalty from conditions.")
            num_dice -= penalty

        num_dice = max(0, num_dice)  # Ensure dice count is not negative

    st.metric("Dice to Roll", num_dice)

    # --- Record Test Outcome ---
    if selected_skill != "None":
        st.write(f"After rolling {num_dice} dice, record the outcome:")
        
        # Ensure the skill exists in the tests dictionary
        if selected_skill not in character.skill_tests:
            st.session_state.character.skill_tests[selected_skill] = {"successes": 0, "failures": 0}

        cols = st.columns(2)
        with cols[0]:
            if st.button("Success", use_container_width=True):
                # Record success
                st.session_state.character.skill_tests[selected_skill]["successes"] += 1
                st.success(f"Recorded a successful test for {selected_skill}!")
                time.sleep(1)
                check_skill_advancement(character, selected_skill, selected_ability)
                # Rerun to reflect changes
                if 'character' in st.session_state:
                    st.session_state.character = copy(character)
                time.sleep(1)
                st.rerun()

        with cols[1]:
            if st.button("Failure", use_container_width=True):
                st.session_state.character.skill_tests[selected_skill]["failures"] += 1
                st.error(f"Recorded a failed test for {selected_skill}.")
                time.sleep(1)
                # Check for learning a new skill (only on failures for unlearned skills)
                if character.skills.get(selected_skill, 0) <= 0:
                    check_skill_advancement(character, selected_skill, selected_ability)
                
                if 'character' in st.session_state:
                    st.session_state.character = copy(character)
                time.sleep(1)
                st.rerun()

    st.divider()

    # --- Display Core Abilities and Conditions ---
    st.header("Core Info")
    cols = st.columns(5)
    for i, (ability, value) in enumerate(character.abilities.items()):
        with cols[i]:
            st.metric(label=ability, value=value)
    
    with st.expander("Manage Conditions"):
        conditions_manager(character)

    st.divider()

    # --- Display Skills and Test Progress ---
    st.header("Skills Progress")
    
    skill_categories = {
        "Crafting & Technical": ["Electronics", "Mechanics", "Engineering", "Computer", "Comms", "Gravitics", "Demolitions", "Screens"],
        "Exploration & Survival": ["Athletics", "Zero-G", "Survival", "Recon", "Navigation", "Grav Vehicle", "Wheeled Vehicle", "Tracked Vehicle", "Riding", "Winged Aircraft", "Rotor Aircraft", "Motorboats", "Ocean Ships", "Sailing Ships", "Submarine", "Mole"],
        "Social & Interpersonal": ["Leadership", "Instruction", "Barter", "Diplomacy", "Etiquette", "Streetwise", "Intimidation", "Deception", "Seduction", "Performance", "Empathy", "Willpower"],
        "Lore & Knowledge": ["Ecology", "Genetics", "Botanics", "Zoology", "Mathematics", "Chemistry", "Geology", "Physics", "History", "Psychology", "Economics", "Sociology", "Astronomy", "First Aid", "Surgery", "Pharmacology", "Linguistics", "Military Strategy", "Combat Tactics", "Veterinary Medicine"],
        "Combat": ["Archery", "Bludgeoning Weapons", "Natural Weapons", "Piercing Weapons", "Slashing Weapons", "Shotgun", "Slug Pistol", "Slug Rifle", "Energy Pistol", "Energy Rifle", "Heavy Weapons", "Mounted Weapons", "Battle Dress"],
    }

    for category, skills_in_category in skill_categories.items():
        with st.expander(category):
            for skill in skills_in_category:
                if skill in st.session_state.character.skills:
                    skill_value = st.session_state.character.skills[skill]
                    tests = st.session_state.character.skill_tests.get(skill, {"successes": 0, "failures": 0})
                    successes = tests.get("successes", 0)
                    failures = tests.get("failures", 0)
                    
                    cols = st.columns([3, 1, 3, 3])
                    with cols[0]:
                        st.write(skill)
                    with cols[1]:
                        st.write(f"**{skill_value}**")
                    with cols[2]:
                        if skill_value > 0:
                            # Advancing an existing skill
                            successes_needed = skill_value + 1
                            st.progress(min(1.0, successes / successes_needed), text=f"{successes}/{successes_needed} S")
                        else:
                            # Learning a new skill (Beginner's Luck)
                            # Heuristic: Show progress for the more demanding requirement between Will and Health.
                            will_needed = max(1, 6 - st.session_state.character.get_ability_value("Will"))
                            health_needed = max(1, 6 - st.session_state.character.get_ability_value("Health") )
                            tests_needed = max(will_needed, health_needed)
                            total_tests = successes + failures
                            st.progress(min(1.0, total_tests / tests_needed), text=f"{total_tests}/{tests_needed} tests")
                    with cols[3]:
                        st.write(f"Fails: {failures}")

    st.divider()

    # --- Display Notes and Inventory ---
    with st.expander("Notes & Inventory"):
        notes_display(character)

def check_skill_advancement(character: Character, skill: str, ability: str):
    """Checks and handles skill advancement based on rulebook logic."""
    current_level = character.skills.get(skill, 0)
    tests = character.skill_tests.get(skill, {"successes": 0, "failures": 0})

    # Case 1: Learning a new skill (Beginner's Luck)
    if current_level <= 0:
        ability_value = character.get_ability_value(ability)
        tests_needed = max(1, 6 - ability_value) # Ensure at least 1 test is needed
        total_tests = tests["successes"] + tests["failures"]
        
        if total_tests >= tests_needed:
            character.skills[skill] = 1
            character.skill_tests[skill] = {"successes": 0, "failures": 0}
            st.balloons()
            st.success(f"**Skill Learned!** {skill} is now level 1!")
            time.sleep(1.5)

    # Case 2: Advancing an existing skill
    else:
        successes_needed = current_level + 1
        if tests["successes"] >= successes_needed:
            character.skills[skill] += 1
            character.skill_tests[skill] = {"successes": 0, "failures": 0}
            st.balloons()
            st.success(f"**Skill Advanced!** {skill} is now level {character.skills[skill]}!")
            time.sleep(1.5)
