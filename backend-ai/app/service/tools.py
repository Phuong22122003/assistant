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
        JWT_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJGeldUN3dja0U5dzVraWRmV180Q0ZLRnB4NlFEV2dkdS1uY0hvcUNRZTBVIn0.eyJleHAiOjE3NTMzMjczMTMsImlhdCI6MTc1MzI5MTMxMywianRpIjoib25ydHJvOmIzNTk2Y2MxLTIxY2MtMzMxMS1iMWNhLTQ2NDhiYjE0N2ZhNyIsImlzcyI6Imh0dHA6Ly9sb2NhbGhvc3Q6ODA4MS9yZWFsbXMvVXNlclNjaGVkdWxlIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6IjNjM2FlMWM2LTdjOTItNDFmMi1hMjY5LTM4YmY4ZThlMmZkZiIsInR5cCI6IkJlYXJlciIsImF6cCI6InVzZXJfc2NoZWR1bGUiLCJzaWQiOiJmYjRkYWNkNi05MmY2LTQ1NGUtYTk3OC1hMTA0MGI5YWViN2YiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwiTUFOQUdFUiIsInVtYV9hdXRob3JpemF0aW9uIiwiQURNSU4iLCJVU0VSIiwiZGVmYXVsdC1yb2xlcy11c2Vyc2NoZWR1bGUiXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBlbWFpbCBwcm9maWxlIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJuYW1lIjoiYWRtaW4gYWRtaW4iLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJhZG1pbjEiLCJnaXZlbl9uYW1lIjoiYWRtaW4iLCJmYW1pbHlfbmFtZSI6ImFkbWluIiwiZW1haWwiOiJhYmNAZ21haWwuY29tIn0.sh9RUC-dUUlfEOPF2qUC0M0y9VNOwUZnqEQauYyFM8QaCdgy1Y8-WdowbQFSPd1V6ZuMsEa3Jm44V6xSlDydqn7gCMJDVpfOWYqv-XMPs-EW3c6rOyjTxdWex-7yk337aQ5m1A61gXyX3lm3UpA_YL58vqSJ_Q_-Es5s23hSpNlW-BQJ9B1ueAIkMOUo9rXOLAJTfxoyVpe0HumoUvgKE52qEFRO5CPHkxFWN6yKjp4Lr0Pz7hc_QMIFh2hGZqomoo1Bj3TtmilS4G03uLMPJBWFaKFo0c1GNfKvle_OEKoeiuIzW1-gJHJzaQ6uJIr_rHO1BtoMobiMSWFhmQzbvg'
        headers = {
       "Authorization": f"Bearer {JWT_TOKEN}"
}
        URL = f'{SCHEDULE_API}/rooms/available?startDate={input_data['from']}&endDate={input_data['to']}' 
        response = requests.get(URL,headers=headers)
        json_data = response.json()  # Parse response JSON

        rooms = json_data.get("data", [])  # Lấy danh sách phòng trong "data"
        return rooms
    except json.JSONDecodeError as e:
        print("Invalid JSON format:", e)
        
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

]


# Phòng A chiều nay còn trống không. -> agent trả về kết quả 
# Phòng A này hiện tại trống không. -> agent trả lại kết quả
# Tôi đang cần 1 phòng trống vào chiều thứ 5 để họp -> hỏi lại thứ 5 tuần nào
# tôi cần 1 phòng trống thứ 5 tuần này thì có không -> check rồi trả về
# đặt cho tôi 1 phòng vào thứ 5 tuần này đi -> hỏi lại phòng a trống vào thứ 5 bạn có muốn đặt không. có -> đặt ko tìm phòng khác
# Dời lịch phòng A chiều thứ 5 tuần này sang thứ 6 được ko. -> check
# Tìm phòng nào đủ lớn để họp nhiều người. -> trả phòng + số người hỏi có đồng ý không.
# Phòng A này trống vào thứ mấy. 