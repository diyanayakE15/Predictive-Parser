# Predictive Parser

## Overview
This project implements a predictive parser based on a given context-free grammar (CFG). The parser takes an input string and the grammar definition and attempts to parse the string, generating a log of each parsing step. The log includes the input buffer, stack content, and the action taken at each step.

## Features
- **Grammar Definition**: Supports grammars defined in Backus-Naur Form (BNF).
- **Input Parsing**: Processes input strings according to the specified grammar.
- **Detailed Logging**: Provides step-by-step logging of the parsing process.
- **Web Interface**: A simple frontend built with Next.js to interact with the parser.

## Technologies Used
- **Backend**: Python with Flask for handling API requests.
- **Frontend**: Next.js (React framework) for creating a user-friendly interface.
- **Data Exchange**: JSON format for communication between the frontend and backend.

## Installation

### Prerequisites
- Python 3.x
- Node.js (for Next.js)
- Flask
- Requests library (for testing with Postman or CURL)

### Backend Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd python_backend

Install required Python packages:
  pip install Flask

Start the Flask server:
  python app.py

### Usage
On the frontend web interface, enter the grammar in BNF format. For example:

S -> a A
A -> b B | ε
B -> c
Input the string you want to parse (e.g., abc).

Click the Parse button to initiate parsing.

View the results in a table format showing the input buffer, stack, and action for each parsing step.

Example Input
Grammar:
css
Copy code
S -> a A
A -> b B | ε
B -> c
Input String:
Expected Output:
The parsing log will display the sequence of actions taken by the parser as it processes the input string.

### Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have suggestions or improvements.

### License
This project is licensed under the MIT License. See the LICENSE file for more details.

### Acknowledgments
Thank you to the open-source community for the libraries and tools that made this project possible.
Special thanks to anyone who contributed to the development of the parser algorithms.

