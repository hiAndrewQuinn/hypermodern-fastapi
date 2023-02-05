PAYLOAD='{
  "cart_value": 790,
  "delivery_distance": 100,
  "number_of_items": 4,
  "time": "2021-10-12T13:00:00Z"
}'

curl -s -X POST 127.0.0.1:8000 \
     -H "Content-Type: application/json" \
     -d "$PAYLOAD" | jq '.'
