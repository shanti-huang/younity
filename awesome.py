import os
import json
from groq import Groq
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

client_secrets_content = '''
{
  "installed": {
    "client_id": "308150010887-bfe4gbic2emcpob654p7lhnnvkk31lir.apps.googleusercontent.com",
    "project_id": "blues-hacks-2025",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "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",
    "redirect_uris": ["http://localhost:8080/"]
  }
}
'''
videos = []

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
    #api_key=os.getenv("GROQ_API_KEY"),
    api_key="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", )

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

extra = input(
    "Tell us if there's anywhere you really want to go, or anything you really want to do. Or skip. We don't care."
)

chat_completion = client.chat.completions.create(
    messages=[{
        "role":
        "user",
        #"content": f"based on all of{x} without referencing specific videors and{z}choose a specific major/program that one of the universities from{y} has, referencing their website"
        "content":
        f"{videos} is a list of videos that I like. based on it and {extra} choose a specific volunteer organization and role from{volunteer_opportunities}. just give me the http organization website, their address, minimum age, and the type of position like seasonal or once a week and a quick description"
    }],
    model="llama-3.3-70b-versatile",
)
basic = chat_completion.choices[0].message.content
print(basic)
