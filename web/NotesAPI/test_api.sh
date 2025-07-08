#!/bin/bash

BASE_URL="http://localhost:5000"

echo "==> Creating a note (POST)"
curl -s -X POST -H "Content-Type: application/json" \
    -d '{"title": "Learn Flask", "content": "Write clean APIs"}' \
    $BASE_URL/notes
echo -e "\n"

echo "==> Listing all notes (GET)"
curl -s $BASE_URL/notes
echo -e "\n"

echo "==> Getting note with ID 1 (GET)"
curl -s $BASE_URL/notes/1
echo -e "\n"

echo "==> Replacing note 1 (PUT)"
curl -s -X PUT -H "Content-Type: application/json" \
    -d '{"title": "Updated Title", "content": "Full content replaced"}' \
    $BASE_URL/notes/1
echo -e "\n"

echo "==> Partially updating note 1 (PATCH)"
curl -s -X PATCH -H "Content-Type: application/json" \
    -d '{"content": "This is the patched content"}' \
    $BASE_URL/notes/1
echo -e "\n"

echo "==> Getting updated note 1"
curl -s $BASE_URL/notes/1
echo -e "\n"

echo "==> Deleting note 1 (DELETE)"
curl -s -X DELETE $BASE_URL/notes/1
echo -e "\n"

echo "==> Confirm deletion of note 1 (GET)"
curl -s $BASE_URL/notes/1
echo -e "\n"

