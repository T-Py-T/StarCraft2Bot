# Fix Python dependencies for StarCraft2Bot
Write-Host "Fixing Python dependencies..." -ForegroundColor Cyan

# Uninstall wrong sc2 package
Write-Host "Removing incorrect sc2 package..." -ForegroundColor Yellow
python -m pip uninstall sc2 -y

# Install correct burnysc2 package
Write-Host "Installing correct burnysc2 package..." -ForegroundColor Yellow
python -m pip install burnysc2

# Install other dependencies
Write-Host "Installing additional dependencies..." -ForegroundColor Yellow
python -m pip install stable-baselines3 wandb tensorboard numpy torch gymnasium

# Test the installation
Write-Host "Testing sc2 library..." -ForegroundColor Yellow
python -c "from sc2 import run_game, maps, Race, Difficulty; print('✅ Correct sc2 library installed!')"

# Test the bot
Write-Host "Testing the bot..." -ForegroundColor Yellow
python src/test_bot.py

Write-Host "Setup complete!" -ForegroundColor Green
