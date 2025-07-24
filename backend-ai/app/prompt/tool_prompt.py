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

Example input:
{{
  "from": "2025-07-29T00:00:00",
  "to": "2025-07-29T23:59:59"
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
