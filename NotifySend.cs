using System;
using System.Net.Sockets;
using System.Text;
using System.Text.Json;

class SendMessageClient
{
    static void Main(string[] args)
    {
        // Defaults
        string header = "INFORMATION";
        string level = "INFO";
        string subject = "";
        int referenz = 0;
        string message = null;
        string ipv4 = null;
        int port = 1526;

        bool showHelp = false;

        // Check paramters 
        foreach (var arg in args)
        {
            if (arg.Equals("-h", StringComparison.OrdinalIgnoreCase) ||
                arg.Equals("--help", StringComparison.OrdinalIgnoreCase) ||
                arg.Equals("/?", StringComparison.OrdinalIgnoreCase))
            {
                showHelp = true;
                break;
            }

            var parts = arg.Split('=', 2);
            if (parts.Length != 2) continue;
            var key = parts[0].Trim().ToUpperInvariant();
            var value = parts[1].Trim();

            switch (key)
            {
                case "HEADER": header = value; break;
                case "LEVEL":
                    var lvl = value.ToUpperInvariant();
                    if (lvl == "INFO" || lvl == "WARN" || lvl == "ERROR")
                        level = lvl;
                    else
                        showHelp = true;
                    break;
                case "SUBJECT": subject = value; break;
                case "REFERENZ":
                    if (int.TryParse(value, out int refVal)) referenz = refVal;
                    else showHelp = true;
                    break;
                case "MESSAGE": message = value; break;
                case "IPV4": ipv4 = value; break;
                case "PORT":
                    if (int.TryParse(value, out int portVal)) port = portVal;
                    else showHelp = true;
                    break;
            }
        }

        // Check required parameters
        if (showHelp || string.IsNullOrWhiteSpace(message) || string.IsNullOrWhiteSpace(ipv4))
        {
            var executableName = OperatingSystem.IsWindows() ? "NotifySend.exe" : "NotifySend";
            
            Console.WriteLine("Usage:");
            Console.WriteLine($"  {executableName} MESSAGE=<Text> IPV4=<Address> [HEADER=<Text>] [LEVEL=INFO|WARN|ERROR] [SUBJECT=<Text>] [REFERENZ=<Number>] [PORT=<Number>]");
            Console.WriteLine();
            Console.WriteLine("Parameters:");
            Console.WriteLine("  MESSAGE   (Required)  - Message text");
            Console.WriteLine("  IPV4      (Required)  - Target IP address");
            Console.WriteLine("  HEADER    (Optional)  - Header (default: INFORMATION)");
            Console.WriteLine("  LEVEL     (Optional)  - INFO, WARN or ERROR (default: INFO)");
            Console.WriteLine("  SUBJECT   (Optional)  - Subject");
            Console.WriteLine("  REFERENZ  (Optional)  - Reference number (integer, default: 0)");
            Console.WriteLine("  PORT      (Optional)  - Target port (default: 1526)");
            Console.WriteLine();
            Console.WriteLine("Example:");
            Console.WriteLine($"  {executableName} MESSAGE=\"Test\" IPV4=127.0.0.1 LEVEL=ERROR PORT=15266");
            return;
        }

        var msg = new
        {
            HEADER = header,
            LEVEL = level,
            SUBJECT = subject,
            REFERENZ = referenz,
            MESSAGE = message
        };

        var json = JsonSerializer.Serialize(msg);
        try
        {
            using (var client = new TcpClient(ipv4, port))
            using (var stream = client.GetStream())
            {
                var data = Encoding.UTF8.GetBytes(json);
                stream.Write(data, 0, data.Length);
            }
            Console.WriteLine("Message sent.");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error sending message: {ex.Message}");
        }
    }
}