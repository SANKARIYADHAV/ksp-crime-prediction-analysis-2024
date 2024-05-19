from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import datetime

# Create a new chatbot
chatbot = ChatBot('PoliceDeploymentBot')

# Optionally, train the chatbot using a corpus
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english')  # You can customize training data as needed

# Function to generate a deployment plan based on user input
def generate_deployment_plan(location, event_type, start_time):
    # Your logic to generate deployment plan goes here
    # This is just a placeholder, replace it with your actual implementation
    return f"A deployment plan has been generated for {location} for {event_type} starting from {start_time}."

# Start interacting with the chatbot
print("Hello! I'm the Police Deployment Bot. How can I assist you today?")

while True:
    user_input = input("You: ")

    # Check if the user wants to exit
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break

    # Get the current date and time
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Process user input and generate a response
    response = None
    if "deployment plan" in user_input.lower():
        # Extract relevant information from user input (e.g., location, event type, start time)
        # For simplicity, let's assume the user provides this information directly in the input
        location = input("Please enter the location: ")
        event_type = input("Please enter the event type: ")
        start_time = current_time  # For simplicity, using the current time as the start time
        response = generate_deployment_plan(location, event_type, start_time)
    else:
        # If the chatbot doesn't understand, provide a generic response
        response = "I'm sorry, I didn't understand that. Could you please provide more details?"

    # Print the bot's response
    print("Bot:", response)
def assign_police_unit(crime):
    crime_to_police_unit = {
        'CrPC': ('Law and Order Police',50,"Increase patrolling in high-crime areas and coordinate with local communities for information sharing."),  
        'MOTOR VEHICLE ACCIDENTS NON-FATAL': ('Traffic Police', 5, "Respond to accidents promptly, manage traffic flow, and educate drivers on safe driving practices."),  
        'PUBLIC SAFETY': ('Law and Order Police', 12, "Implement community policing initiatives and enhance surveillance in public areas."),  
        'THEFT': ('Law and Order Police', 7, "Conduct undercover operations, increase patrols in theft-prone areas, and educate the public on crime prevention tips."),  
        'CYBER CRIME': ('Cyber Crime Police', 6, "Investigate cybercrime incidents, gather digital evidence, and collaborate with cybersecurity experts for prevention and detection."),  
        'Karnataka State Local Act': ('Law and Order Police', 9, "Enforce provisions of the Karnataka State Local Act and coordinate with local authorities for compliance."),  
        'MISSING PERSON': ('Missing Persons Bureau', 4, "Launch search operations, gather intelligence, and work with other agencies to locate missing individuals."),  
        'NARCOTIC DRUGS & PSHYCOTROPIC SUBSTANCES': ('Narcotics Control Bureau', 10, "Conduct undercover operations, intercept drug trafficking routes, and rehabilitate addicts."),  
        'CASES OF HURT': ('Law and Order Police', 6, "Investigate incidents, collect evidence, and ensure medical assistance for victims."),
        # Add more crimes, police units, and solutions as needed
    }
    
    if crime in crime_to_police_unit:
        return crime_to_police_unit[crime]
    else:
        return ('No specific police unit', 0, "No specific solution available for this type of crime.")  # Default values for police unit and number of officers

def crime_chatbot():
    print("Welcome to the Crime Chatbot!")
    print("Please enter the type of crime you're reporting or the solution you're seeking.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        elif user_input.lower() in {'solution', 'solutions'}:
            print("Chatbot: Please enter the type of crime for which you're seeking a solution.")
            user_input = input("You: ")
            _, _, solution = assign_police_unit(user_input)
            print("Chatbot: Here's a solution for the reported crime:", solution)
        elif user_input.lower() == 'deployment plan':
            print("Chatbot: Please enter the type of crime for which you want to know the deployment plan.")
            user_input = input("You: ")
            _, _, deployment_plan = assign_police_unit(user_input)
            print("Chatbot: The deployment plan for {} is: {}".format(user_input, deployment_plan))
        else:
            police_unit, num_officers, _ = assign_police_unit(user_input)
            print("Chatbot: For the crime of '{}', we recommend assigning {} officers to the '{}'.".format(user_input, num_officers, police_unit))

crime_chatbot()
