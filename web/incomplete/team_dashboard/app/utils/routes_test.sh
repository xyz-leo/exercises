#!/bin/bash

# testing_script.sh
# Complete testing script for all API routes
# Expecting the API to be running locally at localhost:8000, empty database

BASE_URL="http://127.0.0.1:8000"
ADMIN_EMAIL="admin@admin.com"
ADMIN_PASSWORD="admin"

echo "STARTING API TESTS"
echo "=================="

# Function to make requests and display results
make_request() {
    local description=$1
    local method=$2
    local url=$3
    local data=$4
    local token=$5
    
    echo ""
    echo "TEST: $description"
    echo "URL: $method $url"
    
    if [ -n "$token" ]; then
        response=$(curl -s -w "|HTTP_STATUS:%{http_code}" -X $method "$url" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $token" \
            -d "$data")
    else
        response=$(curl -s -w "|HTTP_STATUS:%{http_code}" -X $method "$url" \
            -H "Content-Type: application/json" \
            -d "$data")
    fi
    
    # Extract HTTP status
    http_status=$(echo "$response" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d: -f2)
    # Extract response body (remove the status part)
    response_body=$(echo "$response" | sed 's/|HTTP_STATUS:[0-9]*//')
    
    echo "Status: $http_status"
    echo "Response: $response_body"
    echo "----------------------------------------"
}

echo "Creating admin user..."
make_request "Create admin user" "POST" "$BASE_URL/users/" \
    "{\"username\": \"admin\", \"email\": \"$ADMIN_EMAIL\", \"password\": \"$ADMIN_PASSWORD\"}"


# Get auth token first
echo "Getting authentication token..."
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
    -H "Content-Type: application/json" \
    -d "{\"email\": \"$ADMIN_EMAIL\", \"password\": \"$ADMIN_PASSWORD\"}")

TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo "ERROR: Failed to get authentication token"
    exit 1
fi

echo "Token obtained successfully"
echo "==========================="

# USERS ENDPOINTS
echo "USERS ENDPOINTS TESTS"

# Create user
make_request "Create user" "POST" "$BASE_URL/users/" \
    '{"username": "testuser", "email": "test@example.com", "password": "test123"}'

# Create user id 3
make_request "Create user" "POST" "$BASE_URL/users/" \
    '{"username": "team_user", "email": "teamuser@example.com", "password": "test123"}'

# Create user id 4 with same email, must fail
make_request "Create user" "POST" "$BASE_URL/users/" \
    '{"username": "team_users", "email": "teamuser@example.com", "password": "test123"}'

# Get all users
make_request "Get all users" "GET" "$BASE_URL/users/" "" "$TOKEN"

# Get user by ID
make_request "Get user by ID" "GET" "$BASE_URL/users/1" "" "$TOKEN"

# Update user
make_request "Update user" "PUT" "$BASE_URL/users/1" \
    '{"username": "UpdatedUser", "email": "updated@example.com"}' "$TOKEN"

# Get current user info
make_request "Get current user info" "GET" "$BASE_URL/users/me" "" "$TOKEN"

# Change password
make_request "Change password" "PUT" "$BASE_URL/users/password" \
    '{"current_password": "admin", "new_password": "newpassword"}' "$TOKEN"

# TASKS ENDPOINTS
echo "TASKS ENDPOINTS TESTS"

# Create task for user
make_request "Create task for user" "POST" "$BASE_URL/tasks/" \
    '{"title": "Learn FastAPI", "description": "Study FastAPI documentation", "status": "in_progress", "owner_id": 1}' "$TOKEN"

# Get all tasks
make_request "Get all tasks" "GET" "$BASE_URL/tasks/" "" "$TOKEN"

# Get task by ID
make_request "Get task by ID" "GET" "$BASE_URL/tasks/1" "" "$TOKEN"

# Update task
make_request "Update task" "PUT" "$BASE_URL/tasks/1" \
    '{"title": "Updated Task", "description": "Updated description", "status": "completed"}' "$TOKEN"

# Get tasks by user
make_request "Get tasks by user" "GET" "$BASE_URL/tasks/user/1" "" "$TOKEN"

# Get tasks by status
make_request "Get tasks by status" "GET" "$BASE_URL/tasks/status/completed" "" "$TOKEN"

# Delete task
make_request "Delete task" "DELETE" "$BASE_URL/tasks/1" "" "$TOKEN"

# TEAMS ENDPOINTS
echo "TEAMS ENDPOINTS TESTS"

# Create team
make_request "Create team" "POST" "$BASE_URL/teams/" \
    '{"name": "Development Team"}' "$TOKEN"

# Create task for team
make_request "Create task for team" "POST" "$BASE_URL/tasks/" \
    '{"title": "API Development", "description": "Study documentation", "status": "in_progress", "owner_id": 1, "team_id": 1}' "$TOKEN"


# Get all teams
make_request "Get all teams" "GET" "$BASE_URL/teams/" "" "$TOKEN"

# Get team by ID
make_request "Get team by ID" "GET" "$BASE_URL/teams/1" "" "$TOKEN"

# Update team
make_request "Update team" "PUT" "$BASE_URL/teams/1" \
    '{"name": "Advanced Development Team"}' "$TOKEN"

# Get team members
make_request "Get team members" "GET" "$BASE_URL/teams/1/members" "" "$TOKEN"

# Get user teams
make_request "Get user teams" "GET" "$BASE_URL/teams/user/1" "" "$TOKEN"

# Get team tasks
make_request "Get team tasks" "GET" "$BASE_URL/tasks/team/1" "" "$TOKEN"

# TEAM-MEMBERS ENDPOINTS
echo "TEAM-MEMBERS ENDPOINTS TESTS"

# Get all team members
make_request "Get all team members" "GET" "$BASE_URL/team-members/" "" "$TOKEN"

# Get team members by team ID
make_request "Get team members by team ID" "GET" "$BASE_URL/team-members/teams/1/members" "" "$TOKEN"

# Get team member by ID
make_request "Get team member by ID" "GET" "$BASE_URL/team-members/1" "" "$TOKEN"

# Add member to team
make_request "Add member to team" "POST" "$BASE_URL/team-members/teams/1/members" \
    '{"user_id": 3, "team_id": 1, "is_moderator": false}' "$TOKEN"

# Update member role
make_request "Update member role" "PUT" "$BASE_URL/team-members/teams/1/members/3/role" \
    '{"is_moderator": true}' "$TOKEN"

# Delete team member
make_request "Delete team member" "DELETE" "$BASE_URL/team-members/teams/1/members/3" "" "$TOKEN"

# CLEANUP - Delete test resources
echo "CLEANUP TESTS"

# Delete team
make_request "Delete team" "DELETE" "$BASE_URL/teams/1" "" "$TOKEN"

# Delete user
make_request "Delete user" "DELETE" "$BASE_URL/users/2" "" "$TOKEN"
make_request "Delete user" "DELETE" "$BASE_URL/users/3" "" "$TOKEN"
make_request "Delete user" "DELETE" "$BASE_URL/users/1" "" "$TOKEN"

echo ""
echo "ALL TESTS COMPLETED"
echo "==================="
