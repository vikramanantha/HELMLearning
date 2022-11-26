# Vikram Anantha
# Jul 12 2021
# Creating a zoom link with a Zoom API
# Tutorial: https://www.geeksforgeeks.org/how-to-create-a-meeting-with-zoom-api-in-python/
# HELM Learning

from helper_functions import *


# create json data for post requests

# send a request with headers including
# a token and meeting details

short_name = "physics"

def main():
    meetingdetails = {"topic": "<<tobemade>>",
				"type": 2,
				"start_time": "2019-06-14T10: 21: 57",
				"duration": "60",
				"timezone": "Europe/Madrid",
				"agenda": "HELM",
                "password": "PreMalone",
				"recurrence": {"type": 1,
								"repeat_interval": 1
								},
				"settings": {"host_video": "true",
							"participant_video": "true",
							"join_before_host": "False",
							"mute_upon_entry": "False",
							"watermark": "true",
							"audio": "voip",
							"auto_recording": "cloud",
                            
							}
				}
    headers = {'authorization': 'Bearer %s' % generateToken(),
			'content-type': 'application/json'}
    r = requests.post(
		f'https://api.zoom.us/v2/users/me/meetings',
	headers=headers, data=json.dumps(meetingdetails))
    
    print("\n creating zoom meeting ... \n")
	# print(r.text)
	# converting the output into json and extracting the details
    y = json.loads(r.text)
	# print(
	# 	y
    # )
    join_URL = y["join_url"]
    meetingPassword = y["password"]
    
    print(
		'Zoom Meeting Link: {} and your \nPw: "{}"\n'.format(join_URL, meetingPassword)
    )



# run the create meeting function
cnx, cursor = start()

zoom_link = createMeeting(short_name)
cursor.execute("UPDATE classes SET zoom = '{}' WHERE short_name = '{}'".format(zoom_link, short_name))
stop(cnx, cursor)

