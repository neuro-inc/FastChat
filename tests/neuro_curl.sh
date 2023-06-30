curl -s https://api--yevheniisemendiak.jobs.cato-gpu-poc.org.neu.ro/v1/completions \
  -H "Content-Type: application/json" -H "Authorization: Bearer `neuro config show-token`" \
  -d '{
    "model": "vicuna-13b-v1.3",
    "prompt": "Once upon a time",
    "max_tokens": 41,
    "temperature": 0.5
  }' | jq


curl -s https://api--yevheniisemendiak.jobs.cato-gpu-poc.org.neu.ro/v1/chat/completions \
  -H "Content-Type: application/json" -H "Authorization: Bearer `neuro config show-token`" \
  -d '{
    "model": "vicuna-13b-v1.3",
    "messages": [{"role": "user", "content": "Hello! What is your name?"}]
  }' | jq
