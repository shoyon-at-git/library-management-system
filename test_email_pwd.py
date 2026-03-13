#!/usr/bin/env python3
"""Test email and password generation for students."""

from db import init_db
from models.students import register_student, get_student_by_id

init_db()

# Test register_student with auto email and password
print("Testing register_student with auto-generated email and password...")
# Use numeric ID for compatibility with old schema
ok, result = register_student("12345", "John Doe", "CSE", "2023-2024", 2005)

if ok:
    student_id, email, password = result
    print(f"✓ Student registered successfully")
    print(f"  Student ID: {student_id}")
    print(f"  Email: {email}")
    print(f"  Password: {password} (length={len(password)})")
    
    # Verify password length
    if len(password) == 4:
        print(f"✓ Password length is 4")
    else:
        print(f"✗ Password length is {len(password)}, expected 4")
    
    # Retrieve and display student info
    info = get_student_by_id(student_id)
    if info:
        print(f"\n✓ Student info retrieved from DB:")
        print(f"  Student ID: {info[0]}")
        print(f"  Name: {info[1]}")
        print(f"  Department: {info[2]}")
        if len(info) > 3:
            print(f"  Email: {info[3]}")
        if len(info) > 4:
            print(f"  Session: {info[4]}")
        if len(info) > 5:
            print(f"  Birth Year: {info[5]}")
    else:
        print(f"✗ Unable to retrieve student info from DB")
else:
    print(f"✗ Failed to register student: {result}")

print("\n✓ All tests completed!")
