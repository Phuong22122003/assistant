def create_prompt(conversation, keycloak_id):
    return f"""
If the user input is a greeting or small talk, respond naturally without taking action.
Make sure to always include 'Action:' and 'Action Input:' when taking action, otherwise respond normally.
Important rules:
- If required info is missing, ask user or use tools to get info.
- To clarify info, respond with a question as final answer.
- If booking conflicts with an existing booking, ask for confirmation to book another room.
- Always confirm with user before booking or canceling.
- The user is authenticated; always include this user's keycloak_id in any booking or cancellation action.

Keycloak is provide by user "{keycloak_id}" so add it to input like below:
Action Input: {{
    ...,
    "keycloak_id": "{keycloak_id}"
}}

---
Begin the conversation below:
{conversation}
"""
