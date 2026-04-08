#!/usr/bin/env bash

PING_URL="$1"

echo "========================================"
echo " OpenEnv Submission Validator"
echo "========================================"

echo "Step 1/3: Pinging HF Space ($PING_URL/reset)..."

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$PING_URL/reset")

if [ "$HTTP_CODE" = "200" ]; then
  echo "PASSED -- HF Space is live and responds to /reset"
else
  echo "FAILED -- HF Space not responding (HTTP $HTTP_CODE)"
  exit 1
fi

echo "Step 2/3: Docker build..."

docker build -t test-env .

if [ $? -eq 0 ]; then
  echo "PASSED -- Docker build succeeded"
else
  echo "FAILED -- Docker build failed"
  exit 1
fi

echo "Step 3/3: openenv validate..."

openenv validate

if [ $? -eq 0 ]; then
  echo "PASSED -- openenv validate passed"
else
  echo "FAILED -- openenv validate failed"
  exit 1
fi

echo "========================================"
echo " All checks passed! 🚀"
echo "========================================"