import os
import platform

# OS detection
IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"
IS_MACOS = platform.system() == "Darwin"

# StarCraft II executable paths
# Update these paths to match your StarCraft II installation
STARCRAFT_II_PATH_WINDOWS = r"C:\Program Files (x86)\StarCraft II\StarCraft II.exe"
STARCRAFT_II_PATH_LINUX = "/mnt/e/XboxGames/StarCraft II/StarCraft II.exe"

# Default Linux path (for users who installed StarCraft II natively on Linux)
# This is the default path that the sc2 library looks for on Linux
STARCRAFT_II_PATH_LINUX_DEFAULT = "/home/taylor/StarCraftII/Versions"

# macOS paths - StarCraft II is not natively available on macOS
# Users typically run it through Wine, CrossOver, or virtualization
STARCRAFT_II_PATH_MACOS_WINE = "/Users/taylor/Library/Application Support/CrossOver/Bottles/StarCraft II/drive_c/Program Files (x86)/StarCraft II/StarCraft II.exe"
STARCRAFT_II_PATH_MACOS_CROSSOVER = "/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/StarCraft II/StarCraft II.exe"
STARCRAFT_II_PATH_MACOS_DEFAULT = (
    "/Applications/StarCraft II/StarCraft II.app/Contents/MacOS/StarCraft II"
)

# Set the SC2PATH environment variable for the sc2 library based on OS
# The sc2 library uses this environment variable to find the StarCraft II installation
if IS_WINDOWS:
    if os.path.exists(STARCRAFT_II_PATH_WINDOWS):
        os.environ["SC2PATH"] = os.path.dirname(STARCRAFT_II_PATH_WINDOWS)
        print(f"Windows: Set SC2PATH to: {os.environ['SC2PATH']}")

        # Also set project Maps directory as fallback
        try:
            project_root = os.path.dirname(os.path.dirname(__file__))
        except NameError:
            project_root = os.path.dirname(os.getcwd())
        project_maps_dir = os.path.join(project_root, "Maps")
        os.environ["SC2_MAPS_FALLBACK"] = project_maps_dir
    else:
        print(
            f"Warning: StarCraft II executable not found at {STARCRAFT_II_PATH_WINDOWS}"
        )
        print(
            "Please update STARCRAFT_II_PATH_WINDOWS in config.py to match your installation"
        )

elif IS_LINUX:
    # Try WSL path first, then default Linux path
    if os.path.exists(STARCRAFT_II_PATH_LINUX):
        os.environ["SC2PATH"] = os.path.dirname(STARCRAFT_II_PATH_LINUX)
        print(f"Linux/WSL: Set SC2PATH to: {os.environ['SC2PATH']}")

        # Check if Maps directory exists, if not, create a symlink or download maps
        maps_dir = os.path.join(os.environ["SC2PATH"], "Maps")
        if not os.path.exists(maps_dir):
            print(f"Warning: Maps directory not found at {maps_dir}")
            print(
                "This is common with Xbox Game Pass or incomplete StarCraft II installations."
            )
            print("You may need to:")
            print("1. Download StarCraft II maps manually")
            print("2. Or use a different StarCraft II installation")
            print("3. Or run the bot with built-in maps only")

        # Also set project Maps directory as fallback
        try:
            project_root = os.path.dirname(os.path.dirname(__file__))
        except NameError:
            project_root = os.path.dirname(os.getcwd())
        project_maps_dir = os.path.join(project_root, "Maps")
        os.environ["SC2_MAPS_FALLBACK"] = project_maps_dir

    elif os.path.exists(STARCRAFT_II_PATH_LINUX_DEFAULT):
        os.environ["SC2PATH"] = STARCRAFT_II_PATH_LINUX_DEFAULT
        print(f"Linux: Set SC2PATH to: {os.environ['SC2PATH']}")
    else:
        print(
            f"Warning: StarCraft II executable not found at {STARCRAFT_II_PATH_LINUX}"
        )
        print(
            f"Warning: StarCraft II executable not found at {STARCRAFT_II_PATH_LINUX_DEFAULT}"
        )
        print(
            "Please update STARCRAFT_II_PATH_LINUX in config.py to match your installation"
        )

elif IS_MACOS:
    # Try different macOS installation methods
    sc2_found = False

    # Try Wine installation
    if os.path.exists(STARCRAFT_II_PATH_MACOS_WINE):
        os.environ["SC2PATH"] = os.path.dirname(STARCRAFT_II_PATH_MACOS_WINE)
        print(f"macOS (Wine): Set SC2PATH to: {os.environ['SC2PATH']}")
        sc2_found = True

    # Try CrossOver installation
    elif os.path.exists(STARCRAFT_II_PATH_MACOS_CROSSOVER):
        os.environ["SC2PATH"] = os.path.dirname(STARCRAFT_II_PATH_MACOS_CROSSOVER)
        print(f"macOS (CrossOver): Set SC2PATH to: {os.environ['SC2PATH']}")
        sc2_found = True

    # Try default macOS path (if someone managed to get it working)
    elif os.path.exists(STARCRAFT_II_PATH_MACOS_DEFAULT):
        os.environ["SC2PATH"] = os.path.dirname(STARCRAFT_II_PATH_MACOS_DEFAULT)
        print(f"macOS (Native): Set SC2PATH to: {os.environ['SC2PATH']}")
        sc2_found = True

    if sc2_found:
        # Set project Maps directory as fallback
        try:
            project_root = os.path.dirname(os.path.dirname(__file__))
        except NameError:
            project_root = os.path.dirname(os.getcwd())
        project_maps_dir = os.path.join(project_root, "Maps")
        os.environ["SC2_MAPS_FALLBACK"] = project_maps_dir
    else:
        print("Warning: StarCraft II not found on macOS")
        print("StarCraft II is not natively available on macOS. You need to:")
        print("1. Install StarCraft II through Wine, CrossOver, or virtualization")
        print("2. Update the paths in config.py to match your installation")
        print("3. Or run the bot on Windows/Linux instead")
        print("Please manually set the SC2PATH environment variable")

else:
    print(f"Warning: Unsupported operating system: {platform.system()}")
    print("Please manually set the SC2PATH environment variable")

# Game settings
SAVE_REPLAY = True
REALTIME = False

# Disable wandb visuals by default
WANDB_MODE = "offline"

# Disable wandb prompts and set to offline mode
os.environ["WANDB_MODE"] = "offline"
os.environ["WANDB_SILENT"] = "true"
