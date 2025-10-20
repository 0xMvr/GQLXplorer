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
