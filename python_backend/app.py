from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

def matches_input(production, input_symbol, grammar, visited=None):
    """
    Recursively check if a production rule (or sequence of symbols) can lead to the input symbol.
    """
    if not production:
        return False # Empty production cannot match input symbol
    
    if visited is None:
        visited = set()
    
    first_symbol = production[0]

    # If the first symbol is a terminal, check for a match with the input symbol
    if first_symbol == input_symbol:
        return True
    # If it's a non-terminal and not yet visited, recursively check each of its productions
    elif first_symbol in grammar and first_symbol not in visited:
        visited.add(first_symbol) # Mark this non-terminal as visited
        for sub_production in grammar[first_symbol]:
            if matches_input(sub_production, input_symbol, grammar, visited):
                return True
        visited.remove(first_symbol) # Remove from visited after processing

    # Continue with the next symbol in the production sequence
    return matches_input(production[1:], input_symbol, grammar, visited)

def predictive_parser(grammar, input_string):
    log = []  
    input_symbols = list(input_string)
    starting_symbol = next(iter(grammar)) 
    stack = [starting_symbol]

    while stack:
        top = stack.pop() # Get the top of the stack
        log.append({
            'input_buffer': ''.join(input_symbols),
            'stack': ''.join(stack + [top]),
            'action': f'Processing {top}'
        })

        # If the top of the stack is a non-terminal
        if top in grammar:
            matched = False 
            for production in grammar[top]:
                # Use the recursive function to check if this production can lead to the input symbol
                if matches_input(production, input_symbols[0], grammar):
                    log.append({
                        'input_buffer': ''.join(input_symbols),
                        'stack': ''.join(stack + [top]),
                        'action': f'Expand {top} -> {"".join(production)}'
                    })
                    stack.extend(reversed(production)) # Push the production onto the stack
                    matched = True
                    break 

            if not matched:
                log.append({
                    'input_buffer': ''.join(input_symbols),
                    'stack': ''.join(stack + [top]),
                    'action': 'No matching production found, rejecting input'
                })
                return jsonify({'grammar': grammar, 'log': log})

        elif top == input_symbols[0]: # If the top is a terminal
            log.append({
                'input_buffer': ''.join(input_symbols),
                'stack': ''.join(stack),
                'action': f'Match {top}'
            })
            input_symbols.pop(0) # Consume the input symbol            

        else:
            # Mismatch case
            log.append({
                'input_buffer': ''.join(input_symbols),
                'stack': ''.join(stack),
                'action': 'Mismatch, rejecting input'
            })
            return jsonify({'grammar': grammar, 'log': log})

    # If the stack is empty and all input is consumed, parsing is successful
    return jsonify({'grammar': grammar, 'log': log})


@app.route('/parse', methods=['POST'])
def parse_input():
    data = request.get_json()
    grammar = data.get('grammar')
    input_string = data.get('inputString')

    # Parse the grammar string into a usable format
    grammar_dict = {}
    for rule in grammar.splitlines():
        if '->' in rule:
            lhs, rhs = rule.split('->')
            lhs = lhs.strip()
            rhs_options = [option.strip().split() for option in rhs.split('|')]
            grammar_dict[lhs] = rhs_options

    # Pass grammar_dict and input_string to predictive_parser
    return predictive_parser(grammar_dict, input_string)

if __name__ == '__main__':
    app.run(debug=True)
