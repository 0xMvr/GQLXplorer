#!/usr/bin/env python3
"""
GraphQL Introspection Tool
A tool to check if GraphQL introspection is enabled and automatically send all queries/mutations
"""

import argparse
import json
import sys
import requests
import time
from urllib.parse import urljoin

# Introspection query to check if introspection is enabled
INTROSPECTION_CHECK_QUERY = """
{
  __schema {
    queryType {
      name
    }
  }
}
"""

# Full introspection query to get complete schema
FULL_INTROSPECTION_QUERY = """
query IntrospectionQuery {
  __schema {
    queryType { name }
    mutationType { name }
    subscriptionType { name }
    types {
      ...FullType
    }
    directives {
      name
      description
      locations
      args {
        ...InputValue
      }
    }
  }
}

fragment FullType on __Type {
  kind
  name
  description
  fields(includeDeprecated: true) {
    name
    description
    args {
      ...InputValue
    }
    type {
      ...TypeRef
    }
    isDeprecated
    deprecationReason
  }
  inputFields {
    ...InputValue
  }
  interfaces {
    ...TypeRef
  }
  enumValues(includeDeprecated: true) {
    name
    description
    isDeprecated
    deprecationReason
  }
  possibleTypes {
    ...TypeRef
  }
}

fragment InputValue on __InputValue {
  name
  description
  type { ...TypeRef }
  defaultValue
}

fragment TypeRef on __Type {
  kind
  name
  ofType {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
              }
            }
          }
        }
      }
    }
  }
}
"""

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():
    """Print tool banner"""
    banner = f"""
{Colors.OKCYAN}{'='*60}
   ██████╗  ██████╗ ██╗     ██╗  ██╗██████╗ ██╗      ██████╗ ██████╗ ███████╗██████╗ 
  ██╔════╝ ██╔═══██╗██║     ╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██╔══██╗██╔════╝██╔══██╗
  ██║  ███╗██║   ██║██║      ╚███╔╝ ██████╔╝██║     ██║   ██║██████╔╝█████╗  ██████╔╝
  ██║   ██║██║▄▄ ██║██║      ██╔██╗ ██╔═══╝ ██║     ██║   ██║██╔══██╗██╔══╝  ██╔══██╗
  ╚██████╔╝╚██████╔╝███████╗██╔╝ ██╗██║     ███████╗╚██████╔╝██║  ██║███████╗██║  ██║
   ╚═════╝  ╚══▀▀═╝ ╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                                                      
        GraphQL Introspection & Auto-Query Tool
        Check, Extract, and Execute GraphQL Operations
{'='*60}{Colors.ENDC}
    """
    print(banner)

def send_graphql_query(url, query, proxy=None):
    """
    Send a GraphQL query to the target endpoint
    
    Args:
        url: Target GraphQL endpoint URL
        query: GraphQL query string
        proxy: Proxy configuration (optional)
    
    Returns:
        Response object or None if failed
    """
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'GraphQL-Introspection-Tool/1.0'
    }
    
    payload = {
        'query': query
    }
    
    proxies = None
    verify_ssl = True
    
    if proxy:
        proxies = {
            'http': proxy,
            'https': proxy
        }
        # Disable SSL verification when using proxy
        verify_ssl = False
    
    try:
        # Suppress SSL warnings when verification is disabled
        if not verify_ssl:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            proxies=proxies,
            timeout=30,
            verify=verify_ssl
        )
        return response
    except requests.exceptions.RequestException as e:
        print(f"{Colors.FAIL}[!] Error sending request: {e}{Colors.ENDC}")
        return None

def check_introspection(url, proxy=None):
    """
    Check if GraphQL introspection is enabled
    
    Args:
        url: Target GraphQL endpoint URL
        proxy: Proxy configuration (optional)
    
    Returns:
        Boolean indicating if introspection is enabled
    """
    print(f"{Colors.OKBLUE}[*] Checking if introspection is enabled...{Colors.ENDC}")
    
    response = send_graphql_query(url, INTROSPECTION_CHECK_QUERY, proxy)
    
    if not response:
        return False
    
    try:
        data = response.json()
        
        # Check if we got valid introspection data
        if 'data' in data and '__schema' in data['data']:
            print(f"{Colors.OKGREEN}[+] Introspection is ENABLED!{Colors.ENDC}")
            return True
        elif 'errors' in data:
            error_msg = data['errors'][0].get('message', 'Unknown error')
            print(f"{Colors.FAIL}[!] Introspection is DISABLED{Colors.ENDC}")
            print(f"{Colors.WARNING}[!] Error: {error_msg}{Colors.ENDC}")
            return False
        else:
            print(f"{Colors.FAIL}[!] Introspection is likely DISABLED{Colors.ENDC}")
            return False
            
    except json.JSONDecodeError:
        print(f"{Colors.FAIL}[!] Failed to parse response as JSON{Colors.ENDC}")
        print(f"{Colors.WARNING}[!] Response: {response.text[:200]}{Colors.ENDC}")
        return False

def get_full_schema(url, proxy=None):
    """
    Get the full GraphQL schema via introspection
    
    Args:
        url: Target GraphQL endpoint URL
        proxy: Proxy configuration (optional)
    
    Returns:
        Schema data dictionary or None if failed
    """
    print(f"{Colors.OKBLUE}[*] Retrieving full schema...{Colors.ENDC}")
    
    response = send_graphql_query(url, FULL_INTROSPECTION_QUERY, proxy)
    
    if not response:
        return None
    
    try:
        data = response.json()
        
        if 'data' in data and '__schema' in data['data']:
            print(f"{Colors.OKGREEN}[+] Successfully retrieved schema!{Colors.ENDC}")
            return data['data']['__schema']
        else:
            print(f"{Colors.FAIL}[!] Failed to retrieve schema{Colors.ENDC}")
            return None
            
    except json.JSONDecodeError:
        print(f"{Colors.FAIL}[!] Failed to parse schema response{Colors.ENDC}")
        return None

def extract_queries_mutations(schema):
    """
    Extract all queries and mutations from the schema
    
    Args:
        schema: GraphQL schema dictionary
    
    Returns:
        Tuple of (queries, mutations) lists
    """
    queries = []
    mutations = []
    
    query_type_name = schema.get('queryType', {}).get('name')
    mutation_type_name = schema.get('mutationType', {}).get('name')
    
    for type_info in schema.get('types', []):
        type_name = type_info.get('name')
        
        if type_name == query_type_name and type_info.get('fields'):
            for field in type_info['fields']:
                queries.append({
                    'name': field['name'],
                    'description': field.get('description', ''),
                    'args': field.get('args', []),
                    'type': field.get('type', {})
                })
        
        if type_name == mutation_type_name and type_info.get('fields'):
            for field in type_info['fields']:
                mutations.append({
                    'name': field['name'],
                    'description': field.get('description', ''),
                    'args': field.get('args', []),
                    'type': field.get('type', {})
                })
    
    return queries, mutations

def get_type_name(type_obj):
    """
    Recursively get the type name from a type object
    
    Args:
        type_obj: GraphQL type object
    
    Returns:
        String representation of the type
    """
    if not type_obj:
        return "Unknown"
    
    kind = type_obj.get('kind')
    name = type_obj.get('name')
    of_type = type_obj.get('ofType')
    
    if kind == 'NON_NULL':
        return f"{get_type_name(of_type)}!"
    elif kind == 'LIST':
        return f"[{get_type_name(of_type)}]"
    elif name:
        return name
    elif of_type:
        return get_type_name(of_type)
    else:
        return "Unknown"

def generate_mock_value(type_obj, schema):
    """
    Generate a mock value based on the GraphQL type
    
    Args:
        type_obj: GraphQL type object
        schema: Full schema for reference
    
    Returns:
        Mock value appropriate for the type
    """
    type_name = get_type_name(type_obj).rstrip('!')
    
    # Handle list types
    if type_name.startswith('['):
        return []
    
    # Basic scalar types
    if type_name == 'String':
        return "test"
    elif type_name == 'Int':
        return 1
    elif type_name == 'Float':
        return 1.0
    elif type_name == 'Boolean':
        return True
    elif type_name == 'ID':
        return "1"
    else:
        # For custom types, return null or empty object
        return None

def build_graphql_operation(name, args, operation_type='query'):
    """
    Build a GraphQL operation string with arguments
    
    Args:
        name: Operation name
        args: List of argument definitions
        operation_type: 'query' or 'mutation'
    
    Returns:
        Tuple of (operation_string, variables_dict)
    """
    variables = {}
    arg_strings = []
    variable_defs = []
    
    for i, arg in enumerate(args):
        arg_name = arg['name']
        arg_type = get_type_name(arg['type'])
        var_name = f"var{i}"
        
        # Build variable definition
        variable_defs.append(f"${var_name}: {arg_type}")
        
        # Build argument usage
        arg_strings.append(f"{arg_name}: ${var_name}")
        
        # Generate mock value for variable
        variables[var_name] = generate_mock_value(arg['type'], None)
    
    # Build the operation
    if variable_defs:
        variables_part = f"({', '.join(variable_defs)})"
        args_part = f"({', '.join(arg_strings)})"
    else:
        variables_part = ""
        args_part = ""
    
    operation = f"""
{operation_type} Operation{variables_part} {{
  {name}{args_part}
}}
"""
    
    return operation.strip(), variables

def execute_operation(url, operation, variables, proxy=None, delay=0.5):
    """
    Execute a GraphQL operation
    
    Args:
        url: Target GraphQL endpoint URL
        operation: GraphQL operation string
        variables: Variables dictionary
        proxy: Proxy configuration
        delay: Delay between requests in seconds
    
    Returns:
        Response data or None
    """
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'GraphQL-Introspection-Tool/1.0'
    }
    
    payload = {
        'query': operation,
        'variables': variables
    }
    
    proxies = None
    verify_ssl = True
    
    if proxy:
        proxies = {
            'http': proxy,
            'https': proxy
        }
        # Disable SSL verification when using proxy
        verify_ssl = False
    
    try:
        time.sleep(delay)  # Rate limiting
        
        # Suppress SSL warnings when verification is disabled
        if not verify_ssl:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            proxies=proxies,
            timeout=30,
            verify=verify_ssl
        )
        return response
    except requests.exceptions.RequestException as e:
        print(f"{Colors.FAIL}[!] Error: {e}{Colors.ENDC}")
        return None

def send_all_operations(url, queries, mutations, proxy=None, delay=0.5, pause=False):
    """
    Send all queries and mutations to the endpoint
    
    Args:
        url: Target GraphQL endpoint URL
        queries: List of query definitions
        mutations: List of mutation definitions
        proxy: Proxy configuration
        delay: Delay between requests
        pause: Pause and wait for Enter before each request
    """
    results = {
        'queries': [],
        'mutations': []
    }
    
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== SENDING QUERIES ==={Colors.ENDC}")
    print(f"{Colors.OKCYAN}Sending {len(queries)} queries...{Colors.ENDC}\n")
    
    for i, query in enumerate(queries, 1):
        print(f"{Colors.OKBLUE}[{i}/{len(queries)}] Executing query: {query['name']}{Colors.ENDC}")
        
        if pause:
            input(f"{Colors.WARNING}Press Enter to continue...{Colors.ENDC}")
        
        operation, variables = build_graphql_operation(query['name'], query['args'], 'query')
        
        response = execute_operation(url, operation, variables, proxy, delay)
        
        if response:
            try:
                result_data = response.json()
                status = f"{Colors.OKGREEN}✓ Success{Colors.ENDC}" if response.status_code == 200 else f"{Colors.WARNING}⚠ Status {response.status_code}{Colors.ENDC}"
                print(f"    Status: {status}")
                
                if 'errors' in result_data:
                    print(f"    {Colors.WARNING}Errors: {result_data['errors'][0].get('message', 'Unknown error')}{Colors.ENDC}")
                elif 'data' in result_data:
                    print(f"    {Colors.OKGREEN}Data received{Colors.ENDC}")
                
                results['queries'].append({
                    'name': query['name'],
                    'status_code': response.status_code,
                    'response': result_data
                })
            except json.JSONDecodeError:
                print(f"    {Colors.FAIL}Failed to parse response{Colors.ENDC}")
        else:
            print(f"    {Colors.FAIL}✗ Failed{Colors.ENDC}")
        print()
    
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== SENDING MUTATIONS ==={Colors.ENDC}")
    print(f"{Colors.OKCYAN}Sending {len(mutations)} mutations...{Colors.ENDC}\n")
    
    for i, mutation in enumerate(mutations, 1):
        print(f"{Colors.OKBLUE}[{i}/{len(mutations)}] Executing mutation: {mutation['name']}{Colors.ENDC}")
        
        if pause:
            input(f"{Colors.WARNING}Press Enter to continue...{Colors.ENDC}")
        
        operation, variables = build_graphql_operation(mutation['name'], mutation['args'], 'mutation')
        
        response = execute_operation(url, operation, variables, proxy, delay)
        
        if response:
            try:
                result_data = response.json()
                status = f"{Colors.OKGREEN}✓ Success{Colors.ENDC}" if response.status_code == 200 else f"{Colors.WARNING}⚠ Status {response.status_code}{Colors.ENDC}"
                print(f"    Status: {status}")
                
                if 'errors' in result_data:
                    print(f"    {Colors.WARNING}Errors: {result_data['errors'][0].get('message', 'Unknown error')}{Colors.ENDC}")
                elif 'data' in result_data:
                    print(f"    {Colors.OKGREEN}Data received{Colors.ENDC}")
                
                results['mutations'].append({
                    'name': mutation['name'],
                    'status_code': response.status_code,
                    'response': result_data
                })
            except json.JSONDecodeError:
                print(f"    {Colors.FAIL}Failed to parse response{Colors.ENDC}")
        else:
            print(f"    {Colors.FAIL}✗ Failed{Colors.ENDC}")
        print()
    
    return results

def load_schema_from_file(filename):
    """
    Load schema from a JSON file
    
    Args:
        filename: Path to schema JSON file
    
    Returns:
        Schema dictionary or None if failed
    """
    try:
        with open(filename, 'r') as f:
            schema = json.load(f)
        print(f"{Colors.OKGREEN}[+] Schema loaded from {filename}{Colors.ENDC}")
        return schema
    except FileNotFoundError:
        print(f"{Colors.FAIL}[!] File not found: {filename}{Colors.ENDC}")
        return None
    except json.JSONDecodeError:
        print(f"{Colors.FAIL}[!] Invalid JSON in file: {filename}{Colors.ENDC}")
        return None
    except Exception as e:
        print(f"{Colors.FAIL}[!] Failed to load schema: {e}{Colors.ENDC}")
        return None

def save_schema_to_file(schema, filename='graphql_schema.json'):
    """
    Save schema to a JSON file
    
    Args:
        schema: Schema dictionary
        filename: Output filename
    """
    try:
        with open(filename, 'w') as f:
            json.dump(schema, f, indent=2)
        print(f"{Colors.OKGREEN}[+] Schema saved to {filename}{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}[!] Failed to save schema: {e}{Colors.ENDC}")

def save_results_to_file(results, filename='graphql_results.json'):
    """
    Save execution results to a JSON file
    
    Args:
        results: Results dictionary
        filename: Output filename
    """
    try:
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"{Colors.OKGREEN}[+] Results saved to {filename}{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}[!] Failed to save results: {e}{Colors.ENDC}")

def main():
    parser = argparse.ArgumentParser(
        description='GraphQL Introspection & Auto-Query Tool - Automatically execute all queries and mutations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
#        epilog="""
# Examples:
#   # Just show banner and help
#   %(prog)s
  
#   # Check introspection and save schema
#   %(prog)s -u https://example.com/graphql -s schema.json
  
#   # Use default proxy (127.0.0.1:8080)
#   %(prog)s -u https://example.com/graphql -p -q
  
#   # Use custom proxy
#   %(prog)s -u https://example.com/graphql -p http://127.0.0.1:9090 -q
  
#   # Retrieve schema from URL and execute operations
#   %(prog)s -u https://example.com/graphql -q
  
#   # Execute operations from a schema file
#   %(prog)s -u https://example.com/graphql -q schema.json
  
#   # Pause before each request (useful for manual inspection)
#   %(prog)s -u https://example.com/graphql -q --pause
  
#   # Use with proxy and pause mode
#   %(prog)s -u https://example.com/graphql -p -q --pause
#        """
    )
    
    parser.add_argument('-u', '--url', help='Target GraphQL endpoint URL')
    parser.add_argument('-p', '--proxy', nargs='?', const='http://127.0.0.1:8080', metavar='PROXY',
                       help='Use proxy (default: http://127.0.0.1:8080). Optionally specify custom proxy URL')
    parser.add_argument('-s', '--schema', help='Save schema to JSON file (e.g., schema.json)')
    parser.add_argument('-q', '--query', nargs='?', const=True, metavar='SCHEMA_FILE',
                       help='Execute all queries and mutations. Optionally provide schema file (e.g., -q schema.json), otherwise retrieve from URL')
    parser.add_argument('-o', '--output', help='Save query/mutation results to JSON file')
    parser.add_argument('-d', '--delay', type=float, default=0.5,
                       help='Delay between requests in seconds (default: 0.5)')
    parser.add_argument('--pause', action='store_true',
                       help='Pause and wait for Enter key press before each request')
    
    args = parser.parse_args()
    
    print_banner()
    
    # If no arguments provided, show help and banner only
    if not args.url:
        parser.print_help()
        sys.exit(0)
    
    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        print(f"{Colors.FAIL}[!] Invalid URL. Must start with http:// or https://{Colors.ENDC}")
        sys.exit(1)
    
    # Set proxy
    proxy = args.proxy if args.proxy else None
    
    print(f"{Colors.OKBLUE}[*] Target: {args.url}{Colors.ENDC}")
    if proxy:
        print(f"{Colors.OKBLUE}[*] Proxy: {proxy}{Colors.ENDC}")
    print(f"{Colors.OKBLUE}[*] Delay: {args.delay}s between requests{Colors.ENDC}")
    print()
    
    # Determine workflow based on flags
    schema = None
    need_to_query = args.query is not False and args.query is not None
    
    # If -q is provided with a file path, load schema from file
    if need_to_query and isinstance(args.query, str):
        print(f"{Colors.OKBLUE}[*] Loading schema from file: {args.query}{Colors.ENDC}")
        schema = load_schema_from_file(args.query)
        
        if not schema:
            print(f"{Colors.FAIL}[!] Failed to load schema from file. Cannot proceed.{Colors.ENDC}")
            sys.exit(1)
    else:
        # Otherwise, check introspection and retrieve schema from URL
        is_enabled = check_introspection(args.url, proxy)
        
        if not is_enabled:
            print(f"\n{Colors.FAIL}[!] Introspection is disabled. Cannot proceed.{Colors.ENDC}")
            sys.exit(1)
        
        schema = get_full_schema(args.url, proxy)
        
        if not schema:
            print(f"{Colors.FAIL}[!] Failed to retrieve schema. Cannot proceed.{Colors.ENDC}")
            sys.exit(1)
        
        # Save schema if -s flag is provided
        if args.schema:
            print(f"\n{Colors.OKBLUE}[*] Saving schema to file...{Colors.ENDC}")
            save_schema_to_file(schema, args.schema)
    
    # Execute queries and mutations if -q flag is used
    if need_to_query:
        # Extract queries and mutations
        print(f"\n{Colors.OKBLUE}[*] Extracting queries and mutations...{Colors.ENDC}")
        queries, mutations = extract_queries_mutations(schema)
        
        print(f"{Colors.OKGREEN}[+] Found {len(queries)} queries and {len(mutations)} mutations{Colors.ENDC}")
        
        if len(queries) == 0 and len(mutations) == 0:
            print(f"{Colors.WARNING}[!] No queries or mutations found in schema{Colors.ENDC}")
            sys.exit(0)
        
        # Send all queries and mutations
        results = send_all_operations(args.url, queries, mutations, proxy, args.delay, args.pause)
        
        # Summary
        print(f"\n{Colors.HEADER}{Colors.BOLD}=== SUMMARY ==={Colors.ENDC}")
        print(f"{Colors.OKGREEN}Queries executed: {len(results['queries'])}/{len(queries)}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}Mutations executed: {len(results['mutations'])}/{len(mutations)}{Colors.ENDC}")
        
        # Save results if requested
        if args.output:
            save_results_to_file(results, args.output)
    elif not args.schema:
        print(f"\n{Colors.WARNING}[!] Use -s to save schema and/or -q [schema_file] to execute queries/mutations{Colors.ENDC}")

if __name__ == '__main__':
    main()