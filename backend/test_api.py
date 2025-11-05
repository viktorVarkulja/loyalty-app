#!/usr/bin/env python3
"""
Quick API Test Script
Run this to test the loyalty app APIs
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def print_response(title, response):
    """Pretty print response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def main():
    print("🚀 Testing Loyalty App API")
    print(f"Base URL: {BASE_URL}")

    # Test 1: Register
    print("\n📝 Test 1: Register User")
    response = requests.post(f"{BASE_URL}/api/auth/register/", json={
        "email": "testuser@example.com",
        "name": "Test User",
        "password": "testpass123",
        "password_confirm": "testpass123"
    })
    print_response("Register User", response)

    if response.status_code == 201:
        data = response.json()
        access_token = data['tokens']['access']
        user_id = data['user']['id']
        print(f"\n✅ User registered successfully!")
        print(f"User ID: {user_id}")
        print(f"Access Token: {access_token[:50]}...")
    else:
        print("\n❌ Registration failed! User might already exist.")
        print("Trying to login instead...")

        # Try login
        response = requests.post(f"{BASE_URL}/api/auth/login/", json={
            "email": "testuser@example.com",
            "password": "testpass123"
        })
        print_response("Login User", response)

        if response.status_code == 200:
            data = response.json()
            access_token = data['access']
            user_id = data['user']['id']
            print(f"\n✅ Login successful!")
        else:
            print("\n❌ Login failed! Exiting...")
            return

    # Headers for authenticated requests
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Test 2: Get Profile
    print("\n👤 Test 2: Get User Profile")
    response = requests.get(f"{BASE_URL}/api/auth/profile/", headers=headers)
    print_response("Get Profile", response)

    # Test 3: List Products
    print("\n📦 Test 3: List Products")
    response = requests.get(f"{BASE_URL}/api/products/", headers=headers)
    print_response("List Products", response)

    # Test 4: Get Points Balance
    print("\n💰 Test 4: Get Points Balance")
    response = requests.get(f"{BASE_URL}/api/points/balance/", headers=headers)
    print_response("Points Balance", response)

    # Test 5: List Stores
    print("\n🏪 Test 5: List Stores")
    response = requests.get(f"{BASE_URL}/api/stores/", headers=headers)
    print_response("List Stores", response)

    # Test 6: Submit Review Request
    print("\n🔍 Test 6: Submit Product for Review")
    response = requests.post(f"{BASE_URL}/api/reviews/",
        headers=headers,
        json={
            "product_name": "Unknown Product Test",
            "receipt_data": {"quantity": 1, "price": 150.0}
        }
    )
    print_response("Submit Review", response)

    # Test 7: Get My Reviews
    print("\n📋 Test 7: Get My Review Requests")
    response = requests.get(f"{BASE_URL}/api/reviews/my/", headers=headers)
    print_response("My Reviews", response)

    # Test 8: List Transactions
    print("\n📝 Test 8: List Transactions")
    response = requests.get(f"{BASE_URL}/api/transactions/", headers=headers)
    print_response("List Transactions", response)

    print("\n" + "="*60)
    print("✅ All tests completed!")
    print("="*60)
    print("\n💡 Next steps:")
    print("1. Open Swagger UI: http://localhost:8000/api/schema/swagger-ui/")
    print("2. Open Django Admin: http://localhost:8000/admin/")
    print("3. Create admin user: python manage.py createsuperuser")
    print("4. Test more endpoints in Swagger UI")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to server!")
        print("Make sure the server is running:")
        print("  cd backend")
        print("  source venv/bin/activate")
        print("  python manage.py runserver")
    except Exception as e:
        print(f"\n❌ Error: {e}")
