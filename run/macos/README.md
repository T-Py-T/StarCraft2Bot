# macOS Setup for StarCraft2Bot

This directory contains macOS-specific setup scripts and instructions for running StarCraft2Bot on macOS.

## Important Note

**StarCraft II is not natively available on macOS.** You will need to use one of the following methods to run StarCraft II. This guide provides step-by-step instructions for the most common approaches.

## Prerequisites

- macOS with Homebrew installed
- At least 8GB of free disk space
- Battle.net account (free)

## Setup Options

### Option 1: Parallels Desktop (Recommended - Most Reliable)

**Parallels Desktop** is the most reliable way to run StarCraft II on macOS. It provides native Windows performance and full compatibility.

#### Prerequisites
- Parallels Desktop for Mac
- Windows 10/11 license
- At least 8GB RAM
- 50GB free disk space

#### Step 1: Install Parallels Desktop

1. **Download Parallels:**
   - Go to [Parallels Desktop](https://www.parallels.com/)
   - Download the latest version for macOS
   - Install Parallels Desktop

2. **Create Windows VM:**
   - Open Parallels Desktop
   - Click "Create New"
   - Select "Install Windows"
   - Choose Windows 10/11
   - Allocate at least 4GB RAM
   - Allocate at least 50GB disk space

#### Step 2: Install StarCraft II

1. **Start the Windows VM**
2. **Open a web browser**
3. **Go to [Battle.net](https://battle.net)**
4. **Download and install Battle.net**
5. **Install StarCraft II through Battle.net**

#### Step 3: Configure the Bot

1. **Copy the StarCraft2Bot project to the VM**
2. **Install Python and dependencies in the VM**
3. **Update `src/config.py` with the Windows StarCraft II path**
4. **Run the bot from within the VM**

**See:** [PARALLELS_SETUP.md](PARALLELS_SETUP.md) for detailed instructions.

### Option 2: CrossOver (Limited Compatibility)

**CrossOver** is a commercial compatibility layer, but has limited compatibility with StarCraft II on macOS.

#### Step 1: Install CrossOver

1. **Download CrossOver:**
   - Go to [CodeWeavers CrossOver](https://www.codeweavers.com/crossover)
   - Download the latest version for macOS
   - Install CrossOver following the installer instructions

2. **Start Free Trial:**
   - CrossOver offers a 14-day free trial
   - No payment required initially

#### Step 2: Install StarCraft II

1. **Open CrossOver**
2. **Click "Install a Windows Application"**
3. **Search for "Battle.net"** and select it from the list
4. **Follow the installation wizard** - CrossOver will handle the setup
5. **Install StarCraft II** through the Battle.net launcher

**Note:** CrossOver has limited compatibility with StarCraft II. If you encounter issues, use Parallels Desktop instead.

### Option 3: Wine (Deprecated - Not Recommended)

**Note:** Wine Stable is deprecated and will be disabled on 2026-09-01. Parallels Desktop is strongly recommended instead.

If you must use Wine directly:

Open Terminal and run:
```bash
# Install Wine using Homebrew (deprecated)
brew install --cask wine-stable
```

**Note:** This may require sudo permissions. If prompted, enter your macOS password.

#### Step 2: Download StarCraft II

1. Go to [Battle.net](https://battle.net)
2. Download the Battle.net installer
3. Save it to your Downloads folder

#### Step 3: Configure the Bot

After installing StarCraft II through CrossOver, you need to set up the bot to work with CrossOver:

1. **Run the CrossOver setup script:**
   ```bash
   cd /path/to/StarCraft2Bot
   python3 src/sc2_crossover_launcher_v2.py
   ```

2. **Test the setup:**
   ```bash
   make test-macos
   ```

3. **If successful, start training:**
   ```bash
   make train
   ```

#### Step 4: Troubleshooting

If you encounter issues:

1. **StarCraft II not found:**
   - Make sure StarCraft II is installed in CrossOver
   - Check that the bottle name is "StarCraft II"

2. **Websocket connection errors:**
   - This is normal - StarCraft II is launching but may need configuration
   - Try running the test script multiple times
   - Check that port 5000 is not in use by other applications

3. **Performance issues:**
   - Close other applications
   - Run StarCraft II in headless mode (no graphics)
   - Consider allocating more resources to CrossOver

### Option 3: CrossOver (Paid, More Reliable)

CrossOver is a commercial version of Wine that's more polished and reliable.

#### Step 1: Install CrossOver

1. Download from [CodeWeavers](https://www.codeweavers.com/crossover)
2. Install CrossOver following the installer instructions

#### Step 2: Install StarCraft II

1. Open CrossOver
2. Click "Install a Windows Application"
3. Search for "StarCraft II" or "Battle.net"
4. Follow the installation wizard
5. Note the installation path

#### Step 3: Update Configuration

Edit `src/config.py` and update the CrossOver path:
```python
STARCRAFT_II_PATH_MACOS_CROSSOVER = "/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/StarCraft II/StarCraft II.exe"
```

### Option 4: Virtualization (Most Reliable)

For the best compatibility and performance, run Windows in a virtual machine.

#### Step 1: Choose a Virtualization Platform

- **Parallels Desktop** (paid, best performance)
- **VMware Fusion** (paid)
- **VirtualBox** (free)

#### Step 2: Install Windows

1. Create a new Windows VM
2. Install Windows 10/11
3. Allocate at least 4GB RAM and 50GB disk space

#### Step 3: Install StarCraft II

1. Install StarCraft II normally in the Windows VM
2. Note the installation path (usually `C:\Program Files (x86)\StarCraft II\`)

#### Step 4: Run the Bot

Run the bot from within the Windows VM, or use shared folders to access your code.

### Option 5: Remote Development

Develop on macOS but run the bot on a Windows/Linux machine.

1. Set up a Windows/Linux machine (local or cloud)
2. Install StarCraft II on that machine
3. Use VS Code Remote Development or similar
4. Run the bot remotely via SSH

## Quick Setup (After Installing StarCraft II)

1. **Run the setup script:**
   ```bash
   cd run/macos
   python3 setup_maps.py
   ```

2. **Install dependencies:**
   ```bash
   cd ../..
   uv sync
   ```

3. **Test the setup:**
   ```bash
   make check-env
   ```

4. **Start training:**
   ```bash
   make train
   ```

## Troubleshooting

### Common Issues

1. **"Unsupported operating system: Darwin"**
   - This is expected if StarCraft II is not found
   - Follow the setup instructions above

2. **"Maps directory not found"**
   - Run the setup script: `python3 run/macos/setup_maps.py`
   - Or manually create a `Maps` directory in the project root

3. **Whisky installation fails**
   - Make sure you're downloading from the official GitHub releases
   - Check if your macOS version is supported
   - Try running Whisky with administrator privileges

4. **Wine installation fails (if using deprecated Wine)**
   - Make sure you have Homebrew installed
   - Try: `brew update && brew upgrade`
   - Check if you have Xcode Command Line Tools: `xcode-select --install`

5. **StarCraft II won't start in Whisky/Wine**
   - Try running it manually first through Whisky's interface
   - Check Whisky/Wine logs for errors
   - Try installing additional Wine dependencies
   - Make sure you have the correct path in config.py

6. **Performance issues**
   - Run StarCraft II in headless mode (no graphics)
   - Close other applications
   - Consider using CrossOver instead of Wine

### Performance Tips

- **Whisky:** Modern, optimized for gaming, generally performs well
- **Wine:** May have performance issues, but it's free (deprecated)
- **CrossOver:** Generally performs better than Wine
- **Virtualization:** Provides the best compatibility but uses more resources
- **Headless mode:** Set `HEADLESS = True` in your training scripts for better performance

### Getting Help

If you encounter issues:

1. **For Whisky:** Check the [Whisky GitHub issues](https://github.com/WhiskyApp/Whisky/issues) and [Discord community](https://discord.gg/whisky)
2. **For Wine:** Check the [Wine AppDB](https://appdb.winehq.org/) for StarCraft II compatibility
3. Search for "StarCraft II Whisky macOS" or "StarCraft II Wine macOS" on Google
4. Check the [CrossOver compatibility database](https://www.codeweavers.com/compatibility)
5. Consider using a Windows/Linux machine for production training

## Files in this Directory

- `setup_maps.py` - Sets up basic maps and provides setup instructions
- `README.md` - This full setup guide

## Next Steps

Once you have StarCraft II installed and configured:

1. Run `make check-env` to verify your setup
2. Run `make train` to start training
3. Check the main README.md for more detailed usage instructions
