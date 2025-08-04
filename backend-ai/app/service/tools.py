import json
from langchain.agents import Tool
from app.prompt import *
import requests
from config import *
import redis
r = redis.Redis(host='localhost', port=6379, db=0)


def schedule_room_booking(data):
    print(data)
    return 'Book successfully'

def check_room_available(input_str):
    try:
        input_data = json.loads(clean_json_input(input_str))
        keycloak_id =input_data['keycloak_id']
        JWT_TOKEN = r.get(keycloak_id)
        if JWT_TOKEN is not None:
            JWT_TOKEN = JWT_TOKEN.decode('utf-8')
        headers = {
            "Authorization": f"Bearer {JWT_TOKEN}"
        }
        URL = f"{SCHEDULE_API}/rooms/available?startDate={input_data['from']}&endDate={input_data['to']}"
        response = requests.get(URL,headers=headers)
        json_data = response.json()  # Parse response JSON

        return str(json_data)
    except json.JSONDecodeError as e:
        print("Invalid JSON format:", e)

def check_free_time_range_room(input_str):
    try:
        input_data = json.loads(clean_json_input(input_str))
        keycloak_id =input_data['keycloak_id']
        JWT_TOKEN = r.get(keycloak_id)
        if JWT_TOKEN is not None:
            JWT_TOKEN = JWT_TOKEN.decode('utf-8')
        room_name = input_data["roomName"]
        start_date = input_data["from"]
        end_date = input_data["to"]

        headers = {
            "Authorization": f"Bearer {JWT_TOKEN}"
        }

        URL = f"{SCHEDULE_API}/schedules/free/{room_name}?startDate={start_date}&endDate={end_date}"
        response = requests.get(URL, headers=headers)
        
        if response.status_code != 200:
            print("Failed request:", response.status_code, response.text)
            return []

        json_data = response.json()
        available_times = json_data.get("data", [])

        return available_times

    except json.JSONDecodeError as e:
        print("Invalid JSON format:", e)
        return []
    except KeyError as e:
        print("Missing required field in input:", e)
        return []
def get_all_rooms(input_str):
    try:
        
        input_data = json.loads(clean_json_input(input_str))
        keycloak_id =input_data['keycloak_id']
        JWT_TOKEN = r.get(keycloak_id)
        if JWT_TOKEN is not None:
            JWT_TOKEN = JWT_TOKEN.decode('utf-8')

        URL = f"{SCHEDULE_API}/rooms/all"

        headers = {
            "Authorization": f"Bearer {JWT_TOKEN}",
        }
        response = requests.get(URL, headers=headers)
        json_data = response.json()  # Parse response JSON

        rooms = str(json_data)  # Lấy danh sách phòng trong "data"
        return rooms
    except json.JSONDecodeError as e:
        print("Invalid JSON format:", e)

def schedule_room_booking(input_str: str): 
    try:
        input_data = json.loads(clean_json_input(input_str))
        print("Parsed schedule request:", input_data)
        keycloak_id =input_data['keycloak_id']
        JWT_TOKEN = r.get(keycloak_id)
        if JWT_TOKEN is not None:
            JWT_TOKEN = JWT_TOKEN.decode('utf-8')
        payload = {
            "title": input_data["title"],
            "type": input_data["type"].upper(),
            "startTime": input_data["startTime"],
            "endTime": input_data["endTime"]
        }

        if payload["type"] == "OFFLINE":
            payload["roomName"] = input_data["roomName"]
        headers = {
            "Authorization": f"Bearer {JWT_TOKEN}",
            "Content-Type": "application/json"
        }

        url = f"{SCHEDULE_API}/schedules/simple"
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            return "✅ Schedule created successfully."
        else:
            return f"❌ Failed to create schedule: {response.status_code} - {response.text}"

    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_conflict_schedule_info(input_str):
    try:
        input_data = json.loads(clean_json_input(input_str))
        keycloak_id = input_data['keycloak_id']
        start_time = input_data['from']
        end_time = input_data['to']

        JWT_TOKEN = r.get(keycloak_id)
        if JWT_TOKEN is not None:
            JWT_TOKEN = JWT_TOKEN.decode('utf-8')

        headers = {
            "Authorization": f"Bearer {JWT_TOKEN}"
        }

        url = f"{SCHEDULE_API}/schedules/conflicts?startTime={start_time}&endTime={end_time}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json().get("data", [])
            if not data:
                return "✅ Không có lịch nào bị trùng trong khoảng thời gian này."
            return json.dumps(data, indent=2, ensure_ascii=False)
        else:
            return f"❌ API call failed: {response.status_code} - {response.text}"

    except Exception as e:
        return f"❌ Lỗi khi gọi get_conflict_schedule_info: {str(e)}"

def get_department_conflict_users(input_str: str):
    try:
        input_data = json.loads(clean_json_input(input_str))
        keycloak_id = input_data['keycloak_id']
        department_name = input_data['departmentName']
        start_time = input_data['startTime']
        end_time = input_data['endTime']

        JWT_TOKEN = r.get(keycloak_id)
        if JWT_TOKEN:
            JWT_TOKEN = JWT_TOKEN.decode('utf-8')

        headers = {
            "Authorization": f"Bearer {JWT_TOKEN}"
        }

        url = f"{SCHEDULE_API}/schedules/conflicts?departmentName={department_name}&startTime={start_time}&endTime={end_time}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json().get("data", [])
            if not data:
                return "✅ Không có người nào bị trùng lịch trong phòng ban."
            return f"⚠️ Các user bị conflict: \n{json.dumps(data, indent=2, ensure_ascii=False)}"
        else:
            return f"❌ API lỗi: {response.status_code} - {response.text}"

    except Exception as e:
        return f"❌ Lỗi trong get_department_conflict_users: {str(e)}"
    
def create_schedule_for_department(input_str: str):
    try:
        input_data = json.loads(clean_json_input(input_str))
        keycloak_id = input_data['keycloak_id']
        department_name = input_data['departmentName']

        JWT_TOKEN = r.get(keycloak_id)
        if JWT_TOKEN:
            JWT_TOKEN = JWT_TOKEN.decode('utf-8')

        payload = {
            "title": input_data["title"],
            "type": input_data["type"].upper(),
            "startTime": input_data["startTime"],
            "endTime": input_data["endTime"]
        }

        if payload["type"] == "OFFLINE":
            payload["roomName"] = input_data["roomName"]

        headers = {
            "Authorization": f"Bearer {JWT_TOKEN}",
            "Content-Type": "application/json"
        }

        url = f"{SCHEDULE_API}/schedules/departments/{department_name}"
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            return "✅ Lịch họp đã được tạo thành công cho phòng ban."
        else:
            return f"❌ Không thể tạo lịch: {response.status_code} - {response.text}"

    except Exception as e:
        return f"❌ Lỗi trong create_schedule_for_department: {str(e)}"


def clean_json_input(raw: str) -> str:
    lines = raw.strip().splitlines()
    
    # Nếu dòng đầu tiên là ``` hoặc ```json → bỏ
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    
    # Nếu dòng cuối là ```
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    
    return "\n".join(lines).strip()
from datetime import datetime
def get_current_time(input_str=None):
    return datetime.now().strftime("%A, %d %B %Y, %H:%M:%S")

tools = [
    Tool(
        name="ScheduleRoomBooking",
        func=schedule_room_booking,
        description= schedule_room_booking_prompt 
    ),
    Tool(
        name="CheckRoomAvailable",
        func= check_room_available,
        description= check_room_available_prompt
    ),
    Tool(
        name="CheckFreeTimeRangeRoom",
        func= check_free_time_range_room,
        description= check_room_available_range_prompt
    ),
    Tool(
        name="GetAllRooms",
        func= get_all_rooms,
        description= get_all_rooms_prompt
    ),
    Tool(
        name="GetCurrentTime",
        func=get_current_time,
        description= '''
        this function help to get current time with output format is %Y-%m-%dT%H:%M:%S'''
    ),
    Tool(
        name="ScheduleRoomBooking",
        func=schedule_room_booking,
        description=create_simple_schedule_prompt
    ),
    Tool(
        name="GetConflictScheduleInfo",
        func=get_conflict_schedule_info,
        description=conflict_schedule_info_prompt
    ),
    Tool(
        name="GetDepartmentConflictUsers",
        func=get_department_conflict_users,
        description=department_conflict_users_prompt
    ),
    Tool(
        name="CreateScheduleForDepartment",
        func=create_schedule_for_department,
        description=create_department_schedule_prompt
    )
]



# Phòng A chiều nay còn trống không. -> agent trả về kết quả 
# Phòng A này hiện tại trống không. -> agent trả lại kết quả
# Tôi đang cần 1 phòng trống vào chiều thứ 5 để họp -> hỏi lại thứ 5 tuần nào
# tôi cần 1 phòng trống thứ 5 tuần này thì có không -> check rồi trả về
# đặt cho tôi 1 phòng vào thứ 5 tuần này đi -> hỏi lại phòng a trống vào thứ 5 bạn có muốn đặt không. có -> đặt ko tìm phòng khác
# Dời lịch phòng A chiều thứ 5 tuần này sang thứ 6 được ko. -> check
# Tìm phòng nào đủ lớn để họp nhiều người. -> trả phòng + số người hỏi có đồng ý không.
# Phòng A này trống vào thứ mấy. 