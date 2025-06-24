mock_reservation = {
    "reservation_id": "ABC123",
    "email": "host@example.com"
}

def send_guest_data_via_email(email: str, guest_data: list):
    print(f"\n[MOCK EMAIL SENT TO: {email}]")
    for i, guest in enumerate(guest_data, start=1):
        print(f"Guest {i}:")
        for k, v in guest.items():
            print(f"  {k}: {v}")