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

conflict_schedule_info_prompt = """
Use this tool when the user tries to book a room but no rooms are available during the requested time range.
This tool will call an API to retrieve the list of existing room bookings that overlap with the given time range.
Each returned item includes the room name, full name of the user who booked it, their email, and the booked time range.
You can suggest the user to contact one of these users to negotiate a reschedule.

**Input format (JSON):**
{{
  "keycloak_id": "<user's keycloak ID>",
  "from": "YYYY-MM-DDTHH:MM:SS",
  "to": "YYYY-MM-DDTHH:MM:SS"
}}

**Output:**
- If conflicts exist, return a list of objects like:
[
  {{
    "roomName": "Room A",
    "fullName": "Nguyen Van A",
    "email": "abc@example.com",
    "startTime": "2025-08-05T14:00:00",
    "endTime": "2025-08-05T16:00:00"
  }},
  ...
]
- If no conflicts, return a message like:
✅ No conflicting bookings found within the given time range.
"""

department_conflict_users_prompt = """
Use this tool when the user wants to create a schedule for a department and you need to check if any members in that department have conflicting schedules within a given time range.
This tool will call an API using query parameters to retrieve the list of users in the specified department who are unavailable (i.e., have scheduling conflicts) during the requested time range.

**Input format (Query Parameters):**
- departmentName: <name of the department>
- startTime: YYYY-MM-DDTHH:MM:SS
- endTime: YYYY-MM-DDTHH:MM:SS

**Output:**
- If conflicting users exist, return a list of user objects like:
[
  {{
      "lastName": "Nguyen Van",
      "firstName": "A",
      "email": "a@example.com",
  }},
  ...
]

  Then inform the user that some members in the department already have schedules during the selected time range. Suggest that they:
  - Contact these users to negotiate a reschedule, **or**
  - Proceed to create the department schedule while being aware that those users may be unavailable.

- If no conflicts are found, return:
✅ No conflicting users found in the department within the given time range.
"""



create_department_schedule_prompt = """
Use this tool **only after** you have used the `GetDepartmentConflictUsers` tool to check for scheduling conflicts.
If there are any conflicting users in the department during the specified time, do not proceed with this tool and instead inform the user.

This tool will create a schedule for an entire department using the department name (as a path parameter) and the schedule details (as a JSON body).

**Important:** 
- Always call `GetDepartmentConflictUsers` first with the same `departmentName`, `startTime`, and `endTime` to ensure no one in the department has a conflicting schedule.
- Proceed with this tool only if `GetDepartmentConflictUsers` confirms ✅ no conflicting users.

**Input format:**
- Path:
  - departmentName (string): The name of the department for which the schedule is being created.

- Body (JSON):
{{
  "title": "<Title of the schedule>",
  "type": "<ONLINE | OFFLINE>",
  "startTime": "YYYY-MM-DDTHH:MM:SS",
  "endTime": "YYYY-MM-DDTHH:MM:SS",
  "roomName": "<Room name (required only if type is OFFLINE, leave empty for ONLINE)>"
}}

**Output:**
- If creation is successful, return a confirmation message along with the created schedule details.
- If the room is already booked (for OFFLINE type), return a message that the room is unavailable during that time.
- If the department does not exist or the user is unauthorized, return an appropriate error message.
"""

