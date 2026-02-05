# NotifySend

A cross-platform command-line tool for sending messages over TCP sockets, available in both C# (.NET) and Python implementations.

#### Check NotifyPanel for receiving notifications from NotifySend

A Windows Forms application that receives and displays notification messages from a Firebird SQL Server.

https://github.com/huh66/NotifyPanel


#### Check NotifyClient for sending notifications to NotifyPanel from Firebird SQL

Firebird 3.0 User Defined Routine (UDR) for sending messages over TCP to the calling SQL client or any other IP client.

https://github.com/huh66/NotifyClient


## Description

NotifySend is a simple console application that sends structured messages in JSON format over TCP to a target server. It is particularly suitable for notifications and logging systems.

## Features

- Sending messages over TCP sockets
- JSON message formatting
- Configurable parameters (Header, Level, Subject, etc.)
- Cross-platform support (Windows and Linux)
- Simple command-line interface
- **Python client with desktop notification support for Linux**

## Implementations

### C# Client (Windows/Linux)
- .NET 8.0 based implementation
- Native cross-platform support
- Optimized for Windows environments

### Python Client (Linux)
- Pure Python implementation with **unique generator-coroutine architecture**
- Desktop notification support using `plyer`
- Unconventional pipeline design with marinated coroutines
- Generator-based byte streaming for TCP communication
- Lightweight and easy to install
- Ideal for Linux environments

## Prerequisites

### C# Client
- .NET 8.0 or higher
- Windows or Linux operating system

### Python Client
- Python 3.6 or higher
- Linux operating system (for desktop notifications)
- Optional: `plyer` library for desktop notifications

## Installation

### Python Client Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make executable:
```bash
chmod +x notify_send.py
```

3. Run directly:
```bash
./notify_send.py MESSAGE="Test" IPV4=127.0.0.1
```

4. Or install as package:
```bash
pip install -e .
notify_send MESSAGE="Test" IPV4=127.0.0.1
```

### C# Client Installation

#### Install .NET 8.0 (if not already installed)

**Windows:**
Download and install from: https://dotnet.microsoft.com/download/dotnet/8.0

**Linux (Ubuntu/Debian):**
```bash
wget https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb
sudo apt-get update
sudo apt-get install -y dotnet-sdk-8.0
```

### C# Client Build and Run

1. Clone repository:
```bash
git clone <repository-url>
cd NotifySend
```

2. Build project:
```bash
dotnet build
```

3. Create executable:
```bash
# For Windows
dotnet publish -c Release -r win-x64 --self-contained

# For Linux
dotnet publish -c Release -r linux-x64 --self-contained
```

4. Run the application:
```bash
# Windows
NotifySend.exe MESSAGE="Test" IPV4=127.0.0.1

# Linux
./NotifySend MESSAGE="Test" IPV4=127.0.0.1
```

## Usage

### Python Client

**Remote Mode (TCP):**
```bash
./notify_send.py MESSAGE="Test message" IPV4=127.0.0.1
./notify_send.py MESSAGE="Error!" IPV4=192.168.1.5 LEVEL=ERROR PORT=8080
```

**Local Desktop Notification Mode:**
```bash
./notify_send.py --notify MESSAGE="Task complete" TITLE="Success"
```

**Show help:**
```bash
./notify_send.py --help
```

### C# Client Syntax

**Windows:**
```
NotifySend.exe MESSAGE=<Text> IPV4=<Address> [Parameters...]
```

**Linux:**
```
./NotifySend MESSAGE=<Text> IPV4=<Address> [Parameters...]
```

## Parameters

Both Python and C# clients use the same parameter format:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `MESSAGE` | String | Yes | - | The message text to send |
| `IPV4` | String | Yes | - | Target IP address |
| `HEADER` | String | No | "INFORMATION" | Message header |
| `LEVEL` | String | No | "INFO" | Log level (INFO, WARN, ERROR) |
| `SUBJECT` | String | No | "" | Message subject |
| `REFERENZ` | Integer | No | 0 | Reference number |
|  | `TITLE` | String | Yes (--notify) | - | Notification title (Python client only) |

**Python Client Specific:**
- Supports `--notify` flag for local desktop notifications
- Requires both `TITLE` and `MESSAGE` when using `--notify`

### Examples

**Python Client - TCP Mode:**
```bash
# Simple message
./notify_send.py MESSAGE="Test message" IPV4=127.0.0.1

# With parameters
./notify_send.py MESSAGE="Error occurred" IPV4=192.168.1.100 LEVEL=ERROR HEADER="SYSTEM" SUBJECT="Critical Error" REFERENZ=12345 PORT=8080
```

**Python Client - Desktop Notification Mode:**
```bash
# Local notification
./notify_send.py --notify TITLE="Build Complete" MESSAGE="All tests passed"

# Help
./notify_send.py --help
```

**C# Client:**
```bash
# Windows
NotifySend.exe MESSAGE="Test message" IPV4=127.0.0.1

# Linux
./NotifySend MESSAGE="Test message" IPV4=127.0.0.1

# Message with all parameters
NotifySend.exe MESSAGE="Error occurred" IPV4=192.168.1.100 LEVEL=ERROR HEADER="SYSTEM" SUBJECT="Critical Error" REFERENZ=12345 PORT=8080
```

## JSON Message Format

The program sends messages in the following JSON format:

```json
{
    "HEADER": "INFORMATION",
    "LEVEL": "INFO",
    "SUBJECT": "Subject",
    "REFERENZ": 0,
    "MESSAGE": "Message text"
}
```

## Error Handling

- Connection errors display appropriate error messages
- Invalid parameters lead to help display
- Missing required parameters are detected and reported

## Development

### Project Structure

```
NotifySend/
├── NotifySend.cs          # C# implementation
├── NotifySend.csproj      # Project file
├── NotifySend.sln         # Visual Studio Solution
├── notify_send.py         # Python implementation
├── requirements.txt       # Python dependencies
├── setup.py               # Python package setup
└── README.md              # This file
```

### Python Architecture

The Python client uses a unique **generator-coroutine pipeline architecture**:

- **Coroutine Sandwich System**: Validators use primed coroutines for state transformations
- **Generator-Based Streaming**: Byte transmission via generators for chunked socket operations
- **Culinary Naming Convention**: Unconventional variable naming for code uniqueness
- **Pipeline Processing**: Data flows through validation coroutines before transmission

Key Components:
- `marinate_coroutine`: Decorator that primes coroutines for immediate use
- `tuna_sandwich_validator`: Coroutine for LEVEL validation
- `pretzel_number_cruncher`: Coroutine for integer parsing
- `catapult_bytes_generator`: Generator-based TCP transmission
- `toast_local_bagel`: Desktop notification handler

### Compilation

```bash
# Debug version
dotnet build

# Release version
dotnet build -c Release

# Publishing for Windows
dotnet publish -c Release -r win-x64 --self-contained

# Publishing for Linux
dotnet publish -c Release -r linux-x64 --self-contained

# Publishing for multiple platforms
dotnet publish -c Release -r win-x64 --self-contained
dotnet publish -c Release -r linux-x64 --self-contained
```

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Contributing

Contributions are welcome! Please create a Pull Request or report bugs via the Issues function.

## Changelog

### Version 1.2.0
- Added Python client implementation for Linux
- Desktop notification support via plyer
- Generator-coroutine pipeline architecture
- Dual-mode operation (TCP remote + local notification)
- Setup script for easy Python installation

### Version 1.1.0
- Added Linux support for C# client
- Cross-platform compatibility
- Updated help text for both platforms
- English localization

### Version 1.0.0
- Initial version
- Basic TCP communication
- JSON message format
- Command-line parameter support