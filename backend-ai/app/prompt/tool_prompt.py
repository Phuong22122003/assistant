schedule_room_booking_prompt = """
Use this tool to book a room during a specific time range.

Required input (JSON format):
- room_id: string (ID of the room)
- from: ISO datetime string (e.g., "2025-07-29T14:00:00")
- to: ISO datetime string (e.g., "2025-07-29T16:00:00")

Example input:
{{
  "room_id": "room-a",
  "from": "2025-07-29T14:00:00",
  "to": "2025-07-29T16:00:00"
}}

The tool returns a confirmation message indicating whether the booking was successful.
"""
check_room_available_prompt = """
Use this tool to check which rooms are available during a specific time range.

Required input (JSON format):
- from: ISO datetime string (e.g., "2025-07-29T00:00:00")
- to: ISO datetime string (e.g., "2025-07-29T23:59:59")
- keycloak_id: ...
Example input:
{{
  "from": "2025-07-29T00:00:00",
  "to": "2025-07-29T23:59:59",
  "keycloak_id":"..."
}}

Output:
A list of available rooms in the following format:
[
  {{
    "name": "Room A",
    "location": "Floor 1",
    "capacity": 20
  }},
  ...
]
"""

check_room_available_range_prompt = """
Use this tool to check the **available (free) time slots** of a specific room within a given time range.

Required input (JSON format):
- roomName: string (e.g., "Room A")
- from: ISO datetime string (e.g., "2025-07-29T00:00:00")
- to: ISO datetime string (e.g., "2025-07-29T23:59:59")
- keycloak_id: ...


Example input:
{{
  "roomName": "Room A",
  "from": "2025-07-29T00:00:00",
  "to": "2025-07-29T23:59:59"
}}

Output:
A list of **available time ranges** (when the room is free) in the following format:
[
  {{
    "startTime": "2025-07-29T00:00:00",
    "endTime": "2025-07-29T09:00:00"
  }},
  {{
    "startTime": "2025-07-29T10:30:00",
    "endTime": "2025-07-29T13:00:00"
  }},
  ...
]
"""
get_all_rooms_prompt = """
Use this tool to retrieve a list of all rooms.
Input: 
{{
  "keycloak_id":"..."
}}
Output:
A list of rooms in the following format:
[
  {{
    "name": "string",
    "location": "string",
    "capacity": 1073741824,
    "jwt: "..."
  }},
  ...
]
"""

create_simple_schedule_prompt = """
Use this tool to **create a simple schedule** (without participants or departments).

Required input (JSON format):
- title: string (e.g., "Weekly Meeting")
- type: "ONLINE" or "OFFLINE"
- startTime: ISO format datetime (e.g., "2025-07-25T14:00:00")
- endTime: ISO format datetime (e.g., "2025-07-25T15:00:00")
- roomName: string (required **only if type is OFFLINE**)

Example (OFFLINE):
{{
  "title": "Team sync-up",
  "type": "OFFLINE",
  "startTime": "2025-07-26T10:00:00",
  "endTime": "2025-07-26T11:00:00",
  "roomName": "Room A"
}}

Example (ONLINE):
{{
  "title": "Remote training",
  "type": "ONLINE",
  "startTime": "2025-07-26T09:00:00",
  "endTime": "2025-07-26T10:30:00"
}}

Output:
A confirmation message with the created schedule information, including schedule ID, owner, time, and room.
"""

