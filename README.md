# GQLXplorer

<div align="center">
```
   ██████╗  ██████╗ ██╗     ██╗  ██╗██████╗ ██╗      ██████╗ ██████╗ ███████╗██████╗ 
  ██╔════╝ ██╔═══██╗██║     ╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██╔══██╗██╔════╝██╔══██╗
  ██║  ███╗██║   ██║██║      ╚███╔╝ ██████╔╝██║     ██║   ██║██████╔╝█████╗  ██████╔╝
  ██║   ██║██║▄▄ ██║██║      ██╔██╗ ██╔═══╝ ██║     ██║   ██║██╔══██╗██╔══╝  ██╔══██╗
  ╚██████╔╝╚██████╔╝███████╗██╔╝ ██╗██║     ███████╗╚██████╔╝██║  ██║███████╗██║  ██║
   ╚═════╝  ╚══▀▀═╝ ╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
```

**A powerful GraphQL introspection and automated query/mutation execution tool for security testing**

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

</div>

---

## 🚀 Features

- **🔍 Introspection Detection**: Automatically checks if GraphQL introspection is enabled
- **📦 Schema Extraction**: Retrieves and saves complete GraphQL schemas to JSON files
- **⚡ Auto-Query Execution**: Automatically sends all queries and mutations from the schema
- **🔄 Schema Reusability**: Load previously saved schemas and execute them against any GraphQL endpoint
- **🕵️ Proxy Support**: Built-in proxy support with automatic SSL verification bypass (perfect for Burp Suite)
- **⏸️ Manual Mode**: Pause before each request for manual inspection
- **💾 Export Results**: Save all query/mutation responses to JSON for further analysis
- **🎨 Beautiful Output**: Color-coded terminal output for easy reading
- **⚙️ Flexible Configuration**: Customizable delays, proxy settings, and execution modes

---

## 📋 Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Features Breakdown](#features-breakdown)
- [Use Cases](#use-cases)
- [Contributing](#contributing)
- [Disclaimer](#disclaimer)
- [License](#license)

---

## 🛠️ Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Install Dependencies
```bash
git clone https://github.com/yourusername/gqlxplorer.git
cd gqlxplorer
pip install -r requirements.txt
```

### requirements.txt
```
requests>=2.28.0
urllib3>=1.26.0
```

---

## 📖 Usage

### Basic Syntax
```bash
python gqlxplorer.py [options]
```

### Command-Line Options

| Option | Description |
|--------|-------------|
| `-u, --url URL` | Target GraphQL endpoint URL |
| `-p, --proxy [PROXY]` | Use proxy (default: `http://127.0.0.1:8080`). Optionally specify custom proxy |
| `-s, --schema FILE` | Save retrieved schema to JSON file |
| `-q, --query [FILE]` | Execute queries/mutations. Optionally provide schema file, otherwise retrieve from URL |
| `-o, --output FILE` | Save query/mutation results to JSON file |
| `-d, --delay SECONDS` | Delay between requests in seconds (default: 0.5) |
| `--pause` | Pause and wait for Enter key before each request |
| `-h, --help` | Show help message and exit |

---

## 💡 Examples

### 1. Display Help and Banner
```bash
python gqlxplorer.py
```

### 2. Check Introspection and Save Schema
```bash
python gqlxplorer.py -u https://api.example.com/graphql -s schema.json
```

### 3. Auto-Execute All Queries (Retrieve Schema from URL)
```bash
python gqlxplorer.py -u https://api.example.com/graphql -q
```

### 4. Execute Queries from Saved Schema File
```bash
python gqlxplorer.py -u https://api.example.com/graphql -q schema.json
```

### 5. Use with Burp Suite (Default Proxy)
```bash
python gqlxplorer.py -u https://api.example.com/graphql -p -q
```

### 6. Use with Custom Proxy
```bash
python gqlxplorer.py -u https://api.example.com/graphql -p http://192.168.1.100:8080 -q
```

### 7. Manual Inspection Mode (Pause Before Each Request)
```bash
python gqlxplorer.py -u https://api.example.com/graphql -p -q --pause
```

### 8. Save All Results to File
```bash
python gqlxplorer.py -u https://api.example.com/graphql -q -o results.json
```

### 9. Complete Workflow
```bash
# Step 1: Extract schema and save it
python gqlxplorer.py -u https://api.example.com/graphql -s schema.json

# Step 2: Execute all queries with proxy and pause mode
python gqlxplorer.py -u https://api.example.com/graphql -p -q schema.json --pause -o results.json
```

### 10. Test Multiple Endpoints with Same Schema
```bash
# Extract schema from one endpoint
python gqlxplorer.py -u https://api1.example.com/graphql -s schema.json

# Test the same schema against different endpoints
python gqlxplorer.py -u https://api2.example.com/graphql -q schema.json
python gqlxplorer.py -u https://api3.example.com/graphql -q schema.json
```

---

## 🎯 Features Breakdown

### Introspection Detection
GQLXplorer automatically checks if GraphQL introspection is enabled on the target endpoint. If disabled, the tool will notify you and exit gracefully.

### Schema Extraction
Retrieves the complete GraphQL schema including:
- All available queries
- All available mutations
- Field arguments and types
- Descriptions and deprecation information

### Automated Execution
- Automatically generates valid GraphQL operations for all queries and mutations
- Creates mock values for required arguments based on type definitions
- Executes operations sequentially with configurable delays
- Displays real-time status for each operation

### Proxy Integration
- Seamless integration with tools like Burp Suite, OWASP ZAP, or Fiddler
- Automatic SSL certificate verification bypass when using proxies
- Suppresses SSL warnings for cleaner output
- Default proxy: `127.0.0.1:8080` (Burp Suite default)

### Manual Inspection Mode
The `--pause` flag allows you to:
- Review each request before it's sent
- Inspect requests/responses in your proxy tool
- Manually test or modify requests in real-time
- Take notes or screenshots between operations

---

## 🔧 Use Cases

### Security Testing
- **Penetration Testing**: Discover all available GraphQL operations during security assessments
- **Authorization Testing**: Test access controls across all queries and mutations
- **Input Validation**: Identify injection points and test input validation
- **Rate Limiting**: Test rate limiting and DoS protections

### API Discovery
- **Documentation Generation**: Extract complete API schemas when documentation is missing
- **API Inventory**: Catalog all available operations across multiple GraphQL endpoints
- **Schema Comparison**: Compare schemas between different environments (dev, staging, prod)

### Development & Testing
- **API Testing**: Quickly test all GraphQL operations during development
- **Integration Testing**: Verify all queries and mutations are working correctly
- **Schema Validation**: Ensure schema consistency across deployments

---

## 🔐 Security Considerations

### Responsible Disclosure
- Only test GraphQL endpoints you have explicit permission to test
- This tool is intended for authorized security testing and educational purposes only
- Always follow responsible disclosure practices when finding vulnerabilities

### Safe Usage
- Use appropriate delays (`-d`) to avoid overwhelming target servers
- Monitor rate limiting and respect API usage policies
- Be cautious when testing mutations as they may modify data
- Use `--pause` mode when testing production environments

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### How to Contribute
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## ⚠️ Disclaimer

This tool is provided for educational and authorized testing purposes only. Users are responsible for ensuring they have proper authorization before testing any GraphQL endpoints. The authors assume no liability for misuse or damage caused by this tool.

**Use responsibly and ethically.**

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

Created with ❤️ for the security community

---

## 🙏 Acknowledgments

- Thanks to all contributors and users
- Inspired by the need for efficient GraphQL security testing tools
- Built for penetration testers, security researchers, and developers

---

<div align="center">

**If you find this tool useful, please consider giving it a ⭐ on GitHub!**

</div>
