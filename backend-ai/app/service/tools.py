import json
from langchain.agents import Tool
from app.prompt import *
import requests
from config import *

def schedule_room_booking(data):
    print(data)
    return 'Book successfully'

def check_room_available(input_str):
    try:
        input_data = json.loads(input_str)
        print("Parsed JSON:")
        print(input_data)
        JWT_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJGeldUN3dja0U5dzVraWRmV180Q0ZLRnB4NlFEV2dkdS1uY0hvcUNRZTBVIn0.eyJleHAiOjE3NTMzNzA2NTcsImlhdCI6MTc1MzMzNDY1NywianRpIjoiODE0NzgwOTItM2U5NC00MWI3LTk5ODUtMTNkOGJjYzhiM2Y2IiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgxL3JlYWxtcy9Vc2VyU2NoZWR1bGUiLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiNDg4YTdlZmEtNTUwOC00MzEzLTg5NTMtZWM4M2E1NDZiNmRlIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoidXNlcl9zY2hlZHVsZSIsInNlc3Npb25fc3RhdGUiOiJmZjU1MmVkOS1iZWY0LTQ2OTYtOGMxMC0wMzJlOGZiOTBjMjkiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwiTUFOQUdFUiIsInVtYV9hdXRob3JpemF0aW9uIiwiQURNSU4iLCJVU0VSIiwiZGVmYXVsdC1yb2xlcy11c2Vyc2NoZWR1bGUiXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBlbWFpbCBwcm9maWxlIiwic2lkIjoiZmY1NTJlZDktYmVmNC00Njk2LThjMTAtMDMyZThmYjkwYzI5IiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJuYW1lIjoiMTIzMTIzIERvZSIsInByZWZlcnJlZF91c2VybmFtZSI6ImFkbWluIiwiZ2l2ZW5fbmFtZSI6IjEyMzEyMyIsImZhbWlseV9uYW1lIjoiRG9lIiwiZW1haWwiOiJzYXJhaEBleGFtcGxlLmNvbSJ9.eiBivQQQdkDUyG0PSzlTW3EplmkPQjnRS8WfRw9NvGmp7FpNY3luElHECcCqXtodcqudPjKvZRY6X74UEcWngrAGatDZ7Uv5wgL9eU8FVN8h724jm-2RXL3CtlVY-QUjKGEk6_tCwpic6O1Vy8lk8HITjVOT24x3ba4vqhTjCPwmHCqLxhWgjcjz3C0A-eontoYIbmx2DmEUoHIyFzKwylB4vx7MSazBgV9b-hIqfXEavlwdoD0YPT5hD_8jMqHqoKmD7wyQYbQJEYIfYGZOxfQsXsE4n5fomNiacf8-7vCG2j6xZbb2yCiD1U-NDVuvPR2VjLzzJWeMKJxyqtCh0g'
        headers = {
       "Authorization": f"Bearer {JWT_TOKEN}"
}
        URL = f"{SCHEDULE_API}/rooms/available?startDate={input_data['from']}&endDate={input_data['to']}"
        response = requests.get(URL,headers=headers)
        json_data = response.json()  # Parse response JSON

        rooms = json_data.get("data", [])  # Lấy danh sách phòng trong "data"
        return rooms
    except json.JSONDecodeError as e:
        print("Invalid JSON format:", e)

def check_free_time_range_room(input_str):
    try:
        input_data = json.loads(input_str)
        print("Parsed JSON:")
        print(input_data)

        room_name = input_data["roomName"]
        start_date = input_data["from"]
        end_date = input_data["to"]

        JWT_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJGeldUN3dja0U5dzVraWRmV180Q0ZLRnB4NlFEV2dkdS1uY0hvcUNRZTBVIn0.eyJleHAiOjE3NTMzNzA2NTcsImlhdCI6MTc1MzMzNDY1NywianRpIjoiODE0NzgwOTItM2U5NC00MWI3LTk5ODUtMTNkOGJjYzhiM2Y2IiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgxL3JlYWxtcy9Vc2VyU2NoZWR1bGUiLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiNDg4YTdlZmEtNTUwOC00MzEzLTg5NTMtZWM4M2E1NDZiNmRlIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoidXNlcl9zY2hlZHVsZSIsInNlc3Npb25fc3RhdGUiOiJmZjU1MmVkOS1iZWY0LTQ2OTYtOGMxMC0wMzJlOGZiOTBjMjkiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwiTUFOQUdFUiIsInVtYV9hdXRob3JpemF0aW9uIiwiQURNSU4iLCJVU0VSIiwiZGVmYXVsdC1yb2xlcy11c2Vyc2NoZWR1bGUiXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBlbWFpbCBwcm9maWxlIiwic2lkIjoiZmY1NTJlZDktYmVmNC00Njk2LThjMTAtMDMyZThmYjkwYzI5IiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJuYW1lIjoiMTIzMTIzIERvZSIsInByZWZlcnJlZF91c2VybmFtZSI6ImFkbWluIiwiZ2l2ZW5fbmFtZSI6IjEyMzEyMyIsImZhbWlseV9uYW1lIjoiRG9lIiwiZW1haWwiOiJzYXJhaEBleGFtcGxlLmNvbSJ9.eiBivQQQdkDUyG0PSzlTW3EplmkPQjnRS8WfRw9NvGmp7FpNY3luElHECcCqXtodcqudPjKvZRY6X74UEcWngrAGatDZ7Uv5wgL9eU8FVN8h724jm-2RXL3CtlVY-QUjKGEk6_tCwpic6O1Vy8lk8HITjVOT24x3ba4vqhTjCPwmHCqLxhWgjcjz3C0A-eontoYIbmx2DmEUoHIyFzKwylB4vx7MSazBgV9b-hIqfXEavlwdoD0YPT5hD_8jMqHqoKmD7wyQYbQJEYIfYGZOxfQsXsE4n5fomNiacf8-7vCG2j6xZbb2yCiD1U-NDVuvPR2VjLzzJWeMKJxyqtCh0g" 
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
        
tools = [
    Tool(
        name="ScheduleRoomBooking",
        func=schedule_room_booking,
        description= schedule_room_booking_prompt 
    ),
    Tool(
        name="CheckRoom",
        func= check_room_available,
        description= check_room_available_prompt
    ),
    Tool(
        name="CheckFreeTimeRangeRoom",
        func= check_free_time_range_room,
        description= check_room_available_range_prompt
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