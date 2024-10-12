import requests
import time

# Define sections with the number of slides
sections = {
    1: ("brc.1", 9),
    2: ("brc.2", 9),
    3: ("brc.3", 14),
    4: ("brc.4", 23),
    5: ("brc.5", 30),
    6: ("brc.6", 10),
    7: ("brc.7", 13),
    8: ("brc.8", 26),
    9: ("brc.9", 14),
    10: ("brc.10", 16),
    11: ("brc.11", 14),
    12: ("brc.12", 1),
    13: ("brc.13", 1),
    14: ("brc.14", 2),
    15: ("brc.15", 8),
    16: ("hf.1", 10),
    17: ("hf.2", 12),
    18: ("hf.3", 5),
    19: ("hf.4", 13),
}

# Replace with your actual values
cookie = ''  # Replace with actual cookie
sesskey = ''     # Replace with actual sesskey


# Helper function to generate the correct `cmi__suspend_data`
def generate_suspend_data(section_number, slide_number):
    # Calculate the total slide number across all sections
    overall_slide_number = sum(sections[sec][1] for sec in range(1, section_number)) + slide_number
    
    section_progress = []
    for sec in range(1, len(sections) + 1):
        total_slides_in_section = sections[sec][1]
        if sec < section_number:
            section_progress += [total_slides_in_section - 1]
        elif sec == section_number:
            section_progress += [slide_number]
        else:
            section_progress += [0]
    
    # Create the progress string for each section
    section_progress_str = ','.join(map(str, section_progress))
    
    # Generate completion status for all slides
    completion_status = []
    for sec in range(1, len(sections) + 1):
        total_slides_in_section = sections[sec][1]
        if sec < section_number:
            completion_status += [2] * total_slides_in_section
        elif sec == section_number:
            completion_status += [2] * (slide_number) + [1] + [0] * (total_slides_in_section - slide_number - 1)
        else:
            completion_status += [0] * total_slides_in_section
    
    # Convert the completion status list to a string
    completion_status_str = ','.join(map(str, completion_status))
    
    # Return the complete `cmi__suspend_data`
    suspend_data = f"{overall_slide_number}|{section_progress_str}|{completion_status_str}|:undefined"
    print(f"Suspend data for section {section_number}, slide {slide_number}: {suspend_data}")
    return suspend_data

# Function to send requests
def send_request(section_number, slide_number):
    suspend_data = generate_suspend_data(section_number, slide_number)
    
    url = 'https://elearning.msf-usa.org/mod/scorm/datamodel.php'
    headers = {
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': cookie,
        'origin': 'https://elearning.msf-usa.org',
        'referer': f'https://elearning.msf-usa.org/mod/scorm/player.php?a=29&currentorg=org_msf_epackage_1&scoid=284&sesskey={sesskey}&display=popup&mode=normal',
        'user-agent': 'Mozilla/5.0'
    }
    data = {
        'id': '',
        'a': '29',
        'sesskey': sesskey,
        'attempt': '1',
        'scoid': '284',
        'cmi__suspend_data': suspend_data
    }
    
    # Send the POST request
    # response = requests.post(url, headers=headers, data=data)
    
    # # Validate response
    # if 'true' in response.text and '0' in response.text:
    #     print(f"Success for slide {slide_number} in section {section_number}: {response.text}")
    # else:
    #     raise ValueError(f"Unexpected response for slide {slide_number} in section {section_number}: {response.text}")

# Function to automate through a section
def complete_section(section_number, start_slide=1, time_delay=0):
    section_id, total_slides = sections[section_number]
    
    for slide in range(start_slide, start_slide+1):
        # Start the slide
        print(f"Starting slide {slide} in section {section_id}")
        send_request(section_number, slide)

        if time_delay > 0:
            time.sleep(time_delay)

# Function to validate input
def get_valid_input(prompt, validation_fn):
    while True:
        value = input(prompt)
        try:
            value = int(value)
            if validation_fn(value):
                return value
        except ValueError:
            print("Invalid input. Please enter a number.")

# Main script execution
if __name__ == "__main__":
    # Validate section number
    section_number = get_valid_input(
        "Enter the section number (1-20): ",
        lambda x: 1 <= x <= 20
    )
    
    # Validate starting slide number
    total_slides = sections[section_number][1]
    start_slide = get_valid_input(
        f"Enter the starting slide number (1-{total_slides - 1}): ",
        lambda x: 1 <= x <= total_slides
    )

    time_delay = input("Enter the time delay between requests in seconds (default is 0): ")
    time_delay = int(time_delay) if time_delay else 0

    # Run the automation for the given section
    complete_section(section_number, start_slide, time_delay)
