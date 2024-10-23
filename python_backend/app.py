from flask import Flask, request, jsonify

app = Flask(__name__)

def predictive_parser(grammar, input_string):
    log = []  
    input_symbols = list(input_string) 
    stack = ['S'] 
    while stack:
        top = stack.pop()  # Get the top of the stack
        log.append({
            'input_buffer': ''.join(input_symbols),
            'stack': ''.join(stack + [top]),
            'action': f'Processing {top}'
        })

        # If the top of the stack is a non-terminal
        if top in grammar:
            matched = False  # To check if we find a matching production
            for production in grammar[top]:
                if production[0] == input_symbols[0]:  # Check if the first input symbol matches
                    log.append({
                        'input_buffer': ''.join(input_symbols),
                        'stack': ''.join(stack + [top]),
                        'action': f'Expand {top} -> {"".join(production)}'
                    })
                    stack.extend(reversed(production))  # Push the production onto the stack
                    input_symbols.pop(0)  # Consume the input symbol
                    matched = True
                    break
            
            if not matched:
                # No production matched, log the error and return
                log.append({
                    'input_buffer': ''.join(input_symbols),
                    'stack': ''.join(stack + [top]),
                    'action': 'No matching production found, rejecting input'
                })
                return jsonify({'log': log})
        elif top == input_symbols[0]:  # If the top is a terminal
            log.append({
                'input_buffer': ''.join(input_symbols),
                'stack': ''.join(stack),
                'action': f'Match {top}'
            })
            input_symbols.pop(0)  # Consume the input symbol
        else:
            # Mismatch case
            log.append({
                'input_buffer': ''.join(input_symbols),
                'stack': ''.join(stack),
                'action': 'Mismatch, rejecting input'
            })
            return jsonify({'log': log})

    # If the stack is empty and all input is consumed, parsing is successful
    return jsonify({'log': log})

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

    return predictive_parser(grammar_dict, input_string)

if __name__ == '__main__':
    app.run(debug=True)
