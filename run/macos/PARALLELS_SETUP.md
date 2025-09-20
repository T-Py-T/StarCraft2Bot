# Parallels Desktop Setup Guide

## Prerequisites
- Parallels Desktop for Mac
- Windows 10/11 license
- At least 8GB RAM
- 50GB free disk space

## Setup Steps

### 1. Install Parallels Desktop
- Download from [Parallels](https://www.parallels.com/)
- Install and activate

### 2. Create Windows VM
- Open Parallels Desktop
- Click "Create New"
- Select "Install Windows"
- Choose Windows 10/11
- Allocate at least 4GB RAM
- Allocate at least 50GB disk space

### 3. Install StarCraft II
- Start the Windows VM
- Open a web browser
- Go to [Battle.net](https://battle.net)
- Download and install Battle.net
- Install StarCraft II through Battle.net

### 4. Configure the Bot
- Copy the StarCraft2Bot project to the VM
- Install Python and dependencies in the VM
- Update `src/config.py` with the Windows StarCraft II path
- Run the bot from within the VM

### 5. Network Configuration
- Enable network sharing between Mac and VM
- The bot will run in the VM but you can develop on Mac
- Use shared folders to sync code changes

## Advantages of Parallels
- Native Windows performance
- Full StarCraft II compatibility
- Easy to set up and maintain
- Can run multiple VMs for testing

## Disadvantages
- Requires Windows license
- Uses more system resources
- Slightly more complex setup
