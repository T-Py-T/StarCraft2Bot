#!/bin/bash
# Sync changes and run bot in Windows VM

VM_HOST="taylor@10.211.55.3"

echo "📤 Pushing changes to Git..."
git add .
git commit -m "Auto sync: $(date)"
git push origin bot-updates

echo "📥 Pulling changes in Windows VM and running bot..."
ssh $VM_HOST "cd StarCraft2Bot && git pull origin bot-updates && uv run src/test_bot.py"
