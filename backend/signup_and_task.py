#!/usr/bin/env python3
"""
Script to sign up a user with you@gmail.com and add a cricket task.
This script will:
1. Sign up a user with you@gmail.com and password 12345678
2. Create a task named "cricket"
"""

import asyncio
import os
import sys
import json

# Add the current directory to the path so we can import the API client
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'frontend', 'src'))

# Import the API client functions
import httpx


async def signup_and_add_task():
    """Sign up user and add cricket task"""

    # Define the API base URL
    api_base_url = os.getenv("NEXT_PUBLIC_API_URL", "http://localhost:8000/api")
    if not api_base_url.endswith('/api'):
        api_base_url += '/api'

    print(f"Using API base URL: {api_base_url}")

    async with httpx.AsyncClient(timeout=30.0) as client:
        # Step 1: Sign up the user
        print("Signing up user with you@gmail.com...")
        signup_data = {
            "email": "you@gmail.com",
            "password": "12345678"
        }

        try:
            response = await client.post(
                f"{api_base_url}/auth/signup",
                json=signup_data,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code in [200, 201]:
                user_data = response.json()
                print(f"OK User signed up successfully!")
                print(f"  - User ID: {user_data.get('id')}")
                print(f"  - Email: {user_data.get('email')}")

                # Get the token for authentication
                token = user_data.get('token')
                user_id = user_data.get('id')

                # Step 2: Add a cricket task
                print(f"\nAdding cricket task for user {user_id}...")
                task_data = {
                    "title": "cricket",
                    "description": "Cricket task added via script"
                }

                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}"
                }

                task_response = await client.post(
                    f"{api_base_url}/{user_id}/tasks",
                    json=task_data,
                    headers=headers
                )

                if task_response.status_code in [200, 201]:
                    task_result = task_response.json()
                    print(f"OK Task added successfully!")
                    print(f"  - Task ID: {task_result.get('id')}")
                    print(f"  - Task Title: {task_result.get('title')}")
                    print(f"  - Task Description: {task_result.get('description')}")
                    print(f"  - Completed: {task_result.get('completed')}")
                    return True
                else:
                    print(f"✗ Failed to add task. Status: {task_response.status_code}")
                    print(f"  Response: {task_response.text}")
                    return False

            elif response.status_code == 409:  # Conflict - email already exists
                print("OK User already exists with you@gmail.com")

                # Try to sign in instead
                print("Signing in with existing user...")
                signin_data = {
                    "email": "you@gmail.com",
                    "password": "12345678"
                }

                signin_response = await client.post(
                    f"{api_base_url}/auth/signin",
                    json=signin_data,
                    headers={"Content-Type": "application/json"}
                )

                if signin_response.status_code == 200:
                    user_data = signin_response.json()
                    print(f"OK User signed in successfully!")
                    print(f"  - User ID: {user_data.get('id')}")
                    print(f"  - Email: {user_data.get('email')}")

                    # Get the token for authentication
                    token = user_data.get('token')
                    user_id = user_data.get('id')

                    # Step 2: Add a cricket task
                    print(f"\nAdding cricket task for user {user_id}...")
                    task_data = {
                        "title": "cricket",
                        "description": "Cricket task added via script"
                    }

                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {token}"
                    }

                    task_response = await client.post(
                        f"{api_base_url}/{user_id}/tasks",
                        json=task_data,
                        headers=headers
                    )

                    if task_response.status_code in [200, 201]:
                        task_result = task_response.json()
                        print(f"OK Task added successfully!")
                        print(f"  - Task ID: {task_result.get('id')}")
                        print(f"  - Task Title: {task_result.get('title')}")
                        print(f"  - Task Description: {task_result.get('description')}")
                        print(f"  - Completed: {task_result.get('completed')}")
                        return True
                    else:
                        print(f"X Failed to add task. Status: {task_response.status_code}")
                        print(f"  Response: {task_response.text}")
                        return False
                else:
                    print(f"X Failed to sign in. Status: {signin_response.status_code}")
                    print(f"  Response: {signin_response.text}")
                    return False
            else:
                print(f"X Signup failed. Status: {response.status_code}")
                print(f"  Response: {response.text}")
                return False

        except Exception as e:
            print(f"X Error during signup or task creation: {e}")
            return False


if __name__ == "__main__":
    success = asyncio.run(signup_and_add_task())
    if success:
        print("\nSUCCESS: User signed up (or already existed) and cricket task added successfully!")
    else:
        print("\nFAILED: Operation failed!")
        exit(1)