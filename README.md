# NotifySend

A C# Windows command-line program for sending messages over TCP sockets.

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
- German localization
- Simple command-line interface

## Prerequisites

- .NET 8.0 or higher
- Windows operating system

## Installation

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
dotnet publish -c Release
```

## Usage

### Syntax

```
NotifySend.exe MESSAGE=<Text> IPV4=<Address> [Parameters...]
```

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `MESSAGE` | String | Yes | - | The message text to send |
| `IPV4` | String | Yes | - | Target IP address |
| `HEADER` | String | No | "INFORMATION" | Message header |
| `LEVEL` | String | No | "INFO" | Log level (INFO, WARN, ERROR) |
| `SUBJECT` | String | No | "" | Message subject |
| `REFERENZ` | Integer | No | 0 | Reference number |
| `PORT` | Integer | No | 1526 | Target port |

### Examples

**Simple message:**
```bash
NotifySend.exe MESSAGE="Test message" IPV4=127.0.0.1
```

**Message with all parameters:**
```bash
NotifySend.exe MESSAGE="Error occurred" IPV4=192.168.1.100 LEVEL=ERROR HEADER="SYSTEM" SUBJECT="Critical Error" REFERENZ=12345 PORT=8080
```

**Show help:**
```bash
NotifySend.exe --help
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
├── NotifySend.cs          # Main program
├── NotifySend.csproj      # Project file
├── NotifySend.sln         # Visual Studio Solution
└── README.md              # This file
```

### Compilation

```bash
# Debug version
dotnet build

# Release version
dotnet build -c Release

# Publishing
dotnet publish -c Release -r win-x64 --self-contained
```

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Contributing

Contributions are welcome! Please create a Pull Request or report bugs via the Issues function.

## Changelog

### Version 1.0.0
- Initial version
- Basic TCP communication
- JSON message format
- Command-line parameter support