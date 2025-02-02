import os
import json
from groq import Groq
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

videos = []

client_secrets_content = '''
{
  "installed": {
    "client_id": "YOUR_CLIENT_ID",
    "project_id": "YOUR_PROJECT_ID",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "YOUR_CLIENT_SECRET",
    "redirect_uris": ["http://localhost:8080/"]
  }
}
'''

client_secrets = json.loads(client_secrets_content)

flow = InstalledAppFlow.from_client_config(
    client_secrets,
    scopes=['https://www.googleapis.com/auth/youtube.readonly'])
flow.run_local_server(port=8080, prompt="consent")
credentials = flow.credentials

youtube = build('youtube', 'v3', credentials=credentials)


def getlikedvideos():
    try:
        request = youtube.videos().list(part="snippet,contentDetails",
                                        myRating="like",
                                        maxResults=20)
        response = request.execute()

        print("API Response:", json.dumps(response, indent=2))

        if 'items' not in response:
            print("No items found in the response.")
        else:
            for item in response.get('items', []):
                video_title = item['snippet']['title']
                video_url = f"https://www.youtube.com/watch?v={item['id']}"
                videos.append(video_title)

    except Exception as e:
        print(f"An error occurred: {e}")


getlikedvideos()

client = Groq(
    api_key=YOUR_API_KEY
)

volunteer_opportunities = [{
    "Organization":
    "City of Toronto",
    "Roles": [
        "3Rs Ambassador Volunteer", "Animal Fostering Volunteer",
        "Cavalcade of Lights (Technical Role)",
        "Community Recreation Volunteer (Leadership Role)",
        "Cultural Centre and Art Gallery Volunteer (Display/Technical)",
        "Digital Citizen Advisor (Surveyor/Interviewer)",
        "Doors Open Toronto Volunteer",
        "Long-Term Care Home Volunteer (Personal Support Role)"
    ]
}, {
    "Organization":
    "Toronto and Region Conservation Authority (TRCA)",
    "Roles": [
        "Golf Course Starter/Marshal",
        "Day Camp at The Village at Black Creek",
        "Summer Camps at Lake St. George 2025", "Meadoway Ambassador",
        "York Region Nature Collaborative Volunteer",
        "Citizen Science Volunteer Program", "Invasive Management Volunteer",
        "Citizen Science Volunteer Program - Event Support",
        "Citizen Science Volunteer Program - Medicine Wheel Garden and Pollinator Plot Maintenance",
        "Citizen Science Volunteer Program - Turtle Nest Monitoring in Brampton",
        "Citizen Science Volunteer Program - Monitoring and Maintenance",
        "Kortright Community Events Volunteer"
    ]
}, {
    "Organization":
    "Toronto Public Library",
    "Roles": ["Volunteer Librarian (may differ based on personal location)"]
}, {
    "Organization": "Children’s Aid Society (CAS)",
    "Roles": ["Child Life Volunteer/Assistant"]
}, {
    "Organization": "Toronto Humane Society",
    "Roles": ["Pet Care Volunteer"]
}, {
    "Organization":
    "Daily Bread Food Bank",
    "Roles": [
        "Coordinator", "Sorting Donations (Hands-On)",
        "Food Sorting in the Production Hall",
        "Order Picking in the Warehouse", "Kitchen Assistance",
        "Administrative Roles", "Special Events"
    ]
}, {
    "Organization": "Habitat for Humanity Greater Toronto Area (GTA)",
    "Roles": ["Outreach Volunteer"]
}, {
    "Organization": "The Scott Mission",
    "Roles": ["Community Outreach Volunteer"]
}]

def community_service():
    extra = input(
        "Tell us if there's anywhere you really want to go, or anything you really want to do. Or skip. We don't care."
    )

    chat_completion = client.chat.completions.create(
    messages=[{
        "role":
        "user",
        "content": f"{videos} is a list of videos that I like. based on it and {extra} choose a specific volunteer organization and role from{volunteer_opportunities}. just give me the http organization website, their address, minimum age, and the type of position like seasonal or once a week and a quick description"
    }],
    model="llama-3.3-70b-versatile",
)
    basic = chat_completion.choices[0].message.content
    print(basic)

def uni():
    y = ("Algoma University", "Brock University", "St. Catharines", "Carleton University", "Ottawa", "University of Guelph", "Université de Hearst", "Lakehead University","Laurentian University",
"McMaster University", 
"Nipissing University",
"OCAD University",
"Université de l'Ontario français",
"Ontario Tech University",
"University of Ottawa",
"Queen's University",
"Royal Military College of Canada",
"University of Toronto",
"Toronto Metropolitan University (formerly Ryerson University)",
"Trent University",
"University of Waterloo",
"Western University",
"Wilfrid Laurier University",
"University of Windsor",
"York University")
    z= input("Tell us if there's anywhere you really want to go, or anything you really want to do. Or skip. We don't care.")

    chat_completion = client.chat.completions.create(
    messages=[
            {
                    "role": "user",
                    #"content": f"based on all of{x} without referencing specific videors and{z}choose a specific major/program that one of the universities from{y} has, referencing their website"
                    "content": f"primarily based on {videos}, a list of videos that I like and {z} choose a specific university from {y}. choose a program and a degree this university is known for based on all of{videos} and{z}.just give me the name of the university, the program and the degree."
            }
        ],
            model="llama-3.3-70b-versatile",
        )
    a=chat_completion.choices[0].message.content
    print(a)

    chat_completion = client.chat.completions.create(
    messages=[
            {
                    "role": "user",
                    #"content": f"based on all of{x} without referencing specific videors and{z}choose a specific major/program that one of the universities from{y} has, referencing their website"
                    "content": f"based on {videos} and {z}, tell me about my interests and how it relates to {a}. and then in point form, tell me the admission average of {a}, nessecary high school course credits, the location and a description ending with the http website of the degree at {a}"
            }
        ],
            model="llama-3.3-70b-versatile",
        )
    b=chat_completion.choices[0].message.content
    print(b)

def ask(): 
    option = input("Would you like to explore a university program or a volunteering program? input v for volunteer and u for university")

option = input("Would you like to explore a university program or a volunteering program? input v for volunteer and u for university")

if option == "v":
    community_service()
if option == "u":
    uni()
else:
    print("invalid input")
    ask()
