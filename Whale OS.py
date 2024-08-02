import os
import time
import msvcrt  # Module for Windows-specific keyboard input handling
import requests  # Module for making HTTP requests

class Kernel:
    def __init__(self):
        self.running = False
        self.current_directory = "/"
        self.clock_running = False
        self.system_folder = "/whale_os_system_files"  # Define the system files directory
        self.network_config_file = os.path.join(self.system_folder, "network_config.txt")
        self.history_file = os.path.join(self.system_folder, "history.txt")
        self.network_connected = False
        self.ip_address = ""
        self.dns_server = ""
        self.gateway = ""

        # Initialize system files directory and contents
        self.setup_system()
        self.setup_network()

    def setup_system(self):
        # Create the system files directory if it doesn't exist
        if not os.path.exists(self.system_folder):
            os.makedirs(self.system_folder)

        # Create default system files or directories
        self.create_default_config()

    def setup_network(self):
        # Create network configuration file if it doesn't exist
        if not os.path.exists(self.network_config_file):
            with open(self.network_config_file, 'w') as f:
                f.write("Network Configuration:\n")
                f.write(" - IP Address: \n")
                f.write(" - DNS Server: \n")
                f.write(" - Gateway: \n")
                # Add more network settings as needed
        else:
            # Read network configuration if it exists
            self.read_network_config()

    def read_network_config(self):
        # Read network configuration from file
        with open(self.network_config_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith(" - IP Address:"):
                    self.ip_address = line.split(":")[1].strip()
                elif line.startswith(" - DNS Server:"):
                    self.dns_server = line.split(":")[1].strip()
                elif line.startswith(" - Gateway:"):
                    self.gateway = line.split(":")[1].strip()

    def save_network_config(self):
        # Save network configuration to file
        with open(self.network_config_file, 'w') as f:
            f.write("Network Configuration:\n")
            f.write(f" - IP Address: {self.ip_address}\n")
            f.write(f" - DNS Server: {self.dns_server}\n")
            f.write(f" - Gateway: {self.gateway}\n")

    def create_default_config(self):
        # Example: Create a default system configuration file
        system_config_file = os.path.join(self.system_folder, "config.txt")
        if not os.path.exists(system_config_file):
            with open(system_config_file, 'w') as f:
                f.write("Welcome to Whale OS!\n")
                f.write("System configuration:\n")
                f.write(" - Language: English\n")
                f.write(" - Version: 1.0\n")
                f.write(" - Author: Your Name\n")
                # Add more default configuration settings as needed

    def start(self):
        print("Starting Whale OS...")
        self.running = True
        start_time = time.time()
        while True:
            if time.time() - start_time > 6:
                break
            if msvcrt.kbhit() and msvcrt.getch() == b'\x7f':
                self.display_system_specs()
                break

        print("Whale OS started.")
        self.run_shell()

    def run_shell(self):
        while self.running:
            command = input(f"WhaleOS [{self.current_directory}]> ")
            self.execute_command(command)

    def execute_command(self, command):
        parts = command.split()
        if not parts:
            return

        main_command = parts[0].lower()
        if main_command == "exit":
            self.running = False
        elif main_command == "mkdir":
            if len(parts) < 2:
                print("Usage: mkdir <directory_name>")
            else:
                directory_name = parts[1]
                new_directory = os.path.join(self.current_directory, directory_name)
                os.makedirs(new_directory, exist_ok=True)
                print(f"Created directory: {new_directory}")
        elif main_command == "create":
            if len(parts) < 2:
                print("Usage: create <file_name>")
            else:
                file_name = parts[1]
                file_path = os.path.join(self.current_directory, file_name)
                with open(file_path, 'w') as f:
                    print(f"Created file: {file_path}")
        elif main_command == "run":
            if len(parts) < 2:
                print("Usage: run <file_name>")
            else:
                file_name = parts[1]
                file_path = os.path.join(self.current_directory, file_name)
                if os.path.isfile(file_path):
                    print(f"Running file: {file_path}")
                    # Here you could implement logic to 'run' the file (simulation)
                else:
                    print(f"File not found: {file_path}")
        elif main_command == "clock":
            if len(parts) > 1 and parts[1].lower() == "stop":
                self.clock_running = False
                print("Clock stopped.")
            else:
                self.clock_running = True
                self.display_clock()
        elif main_command == "cd":
            if len(parts) < 2:
                print("Usage: cd <directory>")
            else:
                new_directory = parts[1]
                if new_directory == "..":
                    self.current_directory = os.path.dirname(self.current_directory)
                else:
                    new_path = os.path.join(self.current_directory, new_directory)
                    if os.path.isdir(new_path):
                        self.current_directory = new_path
                    else:
                        print(f"Directory '{new_directory}' not found")
        elif main_command == "ls":
            files = os.listdir(self.current_directory)
            for file in files:
                print(file)
        elif main_command == "hello":
            print("Hello in Whale language: こんにちは")
        elif main_command == "edit":
            if len(parts) < 2:
                print("Usage: edit <file_path>")
            else:
                file_path = os.path.join(self.current_directory, parts[1])
                if os.path.isfile(file_path):
                    print(f"Editing file: {file_path}")
                    print("Enter your code below. Press Ctrl+D (Ctrl+Z on Windows) to save and exit.")
                    edited_code = []
                    try:
                        while True:
                            line = input()
                            edited_code.append(line)
                    except EOFError:
                        with open(file_path, 'w') as f:
                            f.write("\n".join(edited_code))
                            print(f"Changes saved to {file_path}")
                else:
                    print(f"File not found: {file_path}")
        elif main_command == "runscript":
            if len(parts) < 2:
                print("Usage: runscript <file_path>")
            else:
                script_name = parts[1]
                script_path = os.path.join(self.current_directory, script_name)
                if os.path.isfile(script_path):
                    print(f"Executing script: {script_path}")
                    with open(script_path, 'r') as f:
                        script_code = f.read()
                        # Simulate running the script
                        print("Script output:")
                        print("-" * 20)
                        exec(script_code)  # Execute the script
                        print("-" * 20)
                else:
                    print(f"Script file not found: {script_path}")
        elif main_command == "game":
            # Command to start the game
            from whale_os_system_files.Game import play_game
            play_game()
        elif main_command == "help":
            self.display_help()
        elif main_command == "network":
            self.manage_network(parts)
        elif main_command == "surf":
            if self.network_connected:
                self.internet_surfing()
            else:
                print("Not connected to a network.")
        elif main_command == "cls":
            self.clear_screen()
        else:
            print(f"Command '{command}' not recognized")

    def display_clock(self):
        while self.clock_running:
            current_time = time.strftime("%H:%M:%S")
            print(f"Current time: {current_time}")
            time.sleep(1)

    def display_system_specs(self):
        # Display system specs here
        print("System Specs:")
        print("-" * 20)
        print(f"OS Version: Whale OS 1.0")
        print(f"Processor: Whale CPU 1.0")
        print(f"Memory: 8GB RAM")
        print(f"Storage: 256GB SSD")
        print("-" * 20)

    def display_help(self):
        # Display available commands and their usage
        print("Available commands:")
        print("-" * 20)
        print("exit          - Exit Whale OS")
        print("mkdir <dir>   - Create a new directory")
        print("create <file> - Create a new file")
        print("run <file>    - Run a file")
        print("clock [stop]  - Start or stop the clock")
        print("cd <dir>      - Change current directory")
        print("ls            - List files in current directory")
        print("hello         - Display greeting in Whale language")
        print("edit <file>   - Edit a file")
        print("runscript <file> - Execute a script file")
        print("game          - Start a game")
        print("help          - Display this help message")
        print("network status   - Display network status")
        print("network connect  - Connect to a network")
        print("network disconnect - Disconnect from the network")
        print("network config   - Configure network settings")
        print("surf          - Start internet surfing (requires network connection)")
        print("cls           - Clear the screen log")
        print("-" * 20)

    def manage_network(self, parts):
        if len(parts) < 2:
            print("Usage: network <command>")
            return

        network_command = parts[1].lower()
        if network_command == "status":
            self.display_network_status()
        elif network_command == "connect":
            self.connect_to_network()
        elif network_command == "disconnect":
            self.disconnect_from_network()
        elif network_command == "config":
            self.configure_network()
        else:
            print("Network command not recognized.")

    def display_network_status(self):
        print("Network Status:")
        print("-" * 20)
        if self.network_connected:
            print("Status: Connected")
            print(f"IP Address: {self.ip_address}")
            print(f"DNS Server: {self.dns_server}")
            print(f"Gateway: {self.gateway}")
        else:
            print("Status: Disconnected")
        print("-" * 20)

    def connect_to_network(self):
        if not self.network_connected:
            print("Connecting to network...")
            # Simulate connection process
            time.sleep(2)
            self.ip_address = "192.168.1.100"  # Example IP address
            self.dns_server = "8.8.8.8"  # Example DNS server
            self.gateway = "192.168.1.1"  # Example gateway
            self.network_connected = True
            print("Connected to network.")
            self.save_network_config()
        else:
            print("Already connected to a network.")

    def disconnect_from_network(self):
        if self.network_connected:
            print("Disconnecting from network...")
            # Simulate disconnection process
            time.sleep(1)
            self.network_connected = False
            self.ip_address = ""
            self.dns_server = ""
            self.gateway = ""
            print("Disconnected from network.")
            self.save_network_config()
        else:
            print("Not currently connected to a network.")

    def configure_network(self):
        print("Network Configuration:")
        print("-" * 20)
        print(f"Current IP Address: {self.ip_address}")
        print(f"Current DNS Server: {self.dns_server}")
        print(f"Current Gateway: {self.gateway}")
        print("-" * 20)
        new_ip = input("Enter new IP Address (or press Enter to keep current): ").strip()
        if new_ip:
            self.ip_address = new_ip
        new_dns = input("Enter new DNS Server (or press Enter to keep current): ").strip()
        if new_dns:
            self.dns_server = new_dns
        new_gateway = input("Enter new Gateway (or press Enter to keep current): ").strip()
        if new_gateway:
            self.gateway = new_gateway
        print("Network configuration updated.")
        self.save_network_config()

    def internet_surfing(self):
        url = input("Enter the URL you want to visit: ").strip()
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Successfully fetched content from {url}")
                print("-" * 20)
                print(response.text)  # Print fetched HTML content (for demonstration)
                print("-" * 20)
            else:
                print(f"Failed to fetch content from {url}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching content from {url}: {str(e)}")

    def clear_screen(self):
        # Function to clear the screen log (command history)
        print("\n" * 50)  # Print 50 new lines to clear the screen log

if __name__ == "__main__":
    kernel = Kernel()
    kernel.start()
