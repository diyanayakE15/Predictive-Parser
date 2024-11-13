# Initialize global variables
diction = {}
firsts = {}
follows = {}
rules= []
nonterm_userdef = [] 
ntlist=[]
term_userdef = []
log = []  
start_symbol = None


def removeLeftRecursion(rulesDiction):
	store = {}
	for lhs in rulesDiction:
		alphaRules = []
		betaRules = []
		allrhs = rulesDiction[lhs]
		for subrhs in allrhs:
			if subrhs[0] == lhs:
				alphaRules.append(subrhs[1:])
			else:
				betaRules.append(subrhs)
		if len(alphaRules) != 0:
			lhs_ = lhs + "'"
			while (lhs_ in rulesDiction.keys()) \
					or (lhs_ in store.keys()):
				lhs_ += "'"
			for b in range(0, len(betaRules)):
				betaRules[b].append(lhs_)
			rulesDiction[lhs] = betaRules
			for a in range(0, len(alphaRules)):
				alphaRules[a].append(lhs_)
			alphaRules.append(['ε'])
			store[lhs_] = alphaRules
	for left in store:
		rulesDiction[left] = store[left]
	return rulesDiction


def LeftFactoring(rulesDiction):
	newDict = {}
	for lhs in rulesDiction:
		allrhs = rulesDiction[lhs]
		temp = dict()
		for subrhs in allrhs:
			if subrhs[0] not in list(temp.keys()):
				temp[subrhs[0]] = [subrhs]
			else:
				temp[subrhs[0]].append(subrhs)
		new_rule = []
		tempo_dict = {}
		for term_key in temp:
			allStartingWithTermKey = temp[term_key]
			if len(allStartingWithTermKey) > 1:
				lhs_ = lhs + "'"
				while (lhs_ in rulesDiction.keys()) \
						or (lhs_ in tempo_dict.keys()):
					lhs_ += "'"
				new_rule.append([term_key, lhs_])
				ex_rules = []
				for g in temp[term_key]:
					ex_rules.append(g[1:])
				tempo_dict[lhs_] = ex_rules
			else:
				new_rule.append(allStartingWithTermKey[0])
		newDict[lhs] = new_rule
		for key in tempo_dict:
			newDict[key] = tempo_dict[key]
	return newDict

def first(rule):
	global rules, nonterm_userdef, \
		term_userdef, diction, firsts
	if len(rule) != 0 and (rule is not None):
		if rule[0] in term_userdef:
			return rule[0]
		elif rule[0] == 'ε':
			return 'ε'

	if len(rule) != 0:
		if rule[0] in list(diction.keys()):
			fres = []
			rhs_rules = diction[rule[0]]
			
			for itr in rhs_rules:
				indivRes = first(itr)
				if type(indivRes) is list:
					for i in indivRes:
						fres.append(i)
				else:
					fres.append(indivRes)
			if 'ε' not in fres:
				return fres
			else:
				newList = []
				fres.remove('ε')
				if len(rule) > 1:
					ansNew = first(rule[1:])
					if ansNew != None:
						if type(ansNew) is list:
							newList = fres + ansNew
						else:
							newList = fres + [ansNew]
					else:
						newList = fres
					return newList
				return fres

def follow(nt):
	global start_symbol, rules, nonterm_userdef, \
		term_userdef, diction, firsts, follows
	solset = set()
	if nt == start_symbol:
		solset.add('$')
	for curNT in diction:
		rhs = diction[curNT]
		for subrule in rhs:
			if nt in subrule:
				while nt in subrule:
					index_nt = subrule.index(nt)
					subrule = subrule[index_nt + 1:]
					if len(subrule) != 0:
						res = first(subrule)
						if 'ε' in res:
							newList = []
							res.remove('ε')
							ansNew = follow(curNT)
							if ansNew != None:
								if type(ansNew) is list:
									newList = res + ansNew
								else:
									newList = res + [ansNew]
							else:
								newList = res
							res = newList
					else:
						if nt != curNT:
							res = follow(curNT)
					if res is not None:
						if type(res) is list:
							for g in res:
								solset.add(g)
						else:
							solset.add(res)
	return list(solset)


def computeAllFirsts():
    global rules, nonterm_userdef, term_userdef, diction, firsts
    for rule in rules:
        k = rule.split("->")
        k[0] = k[0].strip()
        k[1] = k[1].strip()
        rhs = k[1]
        multirhs = rhs.split('|')
        for i in range(len(multirhs)):
            multirhs[i] = multirhs[i].strip()
            multirhs[i] = multirhs[i].split()
        diction[k[0]] = multirhs

    print(f"\nRules: \n")
    for y in diction:
        print(f"{y}->{diction[y]}")
    print(f"\nAfter elimination of left recursion:\n")

    diction = removeLeftRecursion(diction)
    for y in diction:
        print(f"{y}->{diction[y]}")
    print("\nAfter left factoring:\n")

    diction = LeftFactoring(diction)
    for y in diction:
        print(f"{y}->{diction[y]}")
    for y in list(diction.keys()):
        t = set()
        for sub in diction.get(y):
            res = first(sub)
            if res != None:
                if type(res) is list:
                    for u in res:
                        t.add(u)
                else:
                    t.add(res)
        firsts[y] = t

    print("\nCalculated firsts: ")
    key_list = list(firsts.keys())
    index = 0
    for gg in firsts:
        print(f"first({key_list[index]}) "
              f"=> {firsts.get(gg)}")
        index += 1

    # Convert sets to lists for jsonify
    return {k: list(v) for k, v in firsts.items()}


def computeAllFollows():
    global start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows
    for NT in diction:
        solset = set()
        sol = follow(NT)
        if sol is not None:
            for g in sol:
                solset.add(g)
        follows[NT] = solset

    print("\nCalculated follows: ")
    key_list = list(follows.keys())
    index = 0
    for gg in follows:
        print(f"follow({key_list[index]})"
              f" => {follows[gg]}")
        index += 1

    # Convert sets to lists for jsonify
    return {k: list(v) for k, v in follows.items()}


def createParseTable():
	global ntlist
	import copy
	global diction, firsts, follows, term_userdef
	print("\nFirsts and Follow Result table\n")

	mx_len_first = 0
	mx_len_fol = 0
	for u in diction:
		k1 = len(str(firsts[u]))
		k2 = len(str(follows[u]))
		if k1 > mx_len_first:
			mx_len_first = k1
		if k2 > mx_len_fol:
			mx_len_fol = k2

	print(f"{{:<{10}}} "
		f"{{:<{mx_len_first + 5}}} "
		f"{{:<{mx_len_fol + 5}}}"
		.format("Non-T", "FIRST", "FOLLOW"))
	for u in diction:
		print(f"{{:<{10}}} "
			f"{{:<{mx_len_first + 5}}} "
			f"{{:<{mx_len_fol + 5}}}"
			.format(u, str(firsts[u]), str(follows[u])))
	ntlist = list(diction.keys())
	terminals = copy.deepcopy(term_userdef)
	terminals.append('$')

	mat = []
	for x in diction:
		row = []
		for y in terminals:
			row.append('')
		mat.append(row)
	rules_is_LL = True
	for lhs in diction:
		rhs = diction[lhs]
		for y in rhs:
			res = first(y)
			if 'ε' in res:
				if type(res) == str:
					firstFollow = []
					fol_op = follows[lhs]
					if fol_op is str:
						firstFollow.append(fol_op)
					else:
						for u in fol_op:
							firstFollow.append(u)
					res = firstFollow
				else:
					res.remove('ε')
					res = list(res) +\
						list(follows[lhs])
			ttemp = []
			if type(res) is str:
				ttemp.append(res)
				res = copy.deepcopy(ttemp)
			for c in res:
				xnt = ntlist.index(lhs)
				yt = terminals.index(c)
				if mat[xnt][yt] == '':
					mat[xnt][yt] = mat[xnt][yt] \
								+ f"{lhs}->{' '.join(y)}"
				else:
					if f"{lhs}->{y}" in mat[xnt][yt]:
						continue
					else:
						rules_is_LL = False
						mat[xnt][yt] = mat[xnt][yt] \
									+ f",{lhs}->{' '.join(y)}"
	print("\nGenerated parsing table:\n")
	frmt = "{:>12}" * len(terminals)
	print(frmt.format(*terminals))

	j = 0
	for y in mat:
		frmt1 = "{:>12}" * len(y)
		print(f"{ntlist[j]} {frmt1.format(*y)}")
		j += 1


	return (mat, rules_is_LL, terminals)


def validateStringUsingStackBuffer(parsing_table, rulesll1, table_term_list, input_string, term_userdef, start_symbol):
	global log
	print(f"\nValidate String => {input_string}\n")
	if rulesll1 == False:
		return f"\nInput String = " \
			f"\"{input_string}\"\n" \
			f"rules is not LL(1)"

	stack = [start_symbol, '$']
	buffer = []

	input_string = input_string.split()
	input_string.reverse()
	buffer = ['$'] + input_string

	print("{:>20} {:>20} {:>20}".
		format("Buffer", "Stack","Action"))

	while True:
		if stack == ['$'] and buffer == ['$']:
			log.append({
				'input_buffer': ''.join(stack),
				'stack': ''.join(buffer),
				'action': "Valid"
        })
			print("{:>20} {:>20} {:>20}"
				.format(' '.join(buffer),
						' '.join(stack),
						"Valid"))
			return jsonify(log)
		elif stack[0] not in term_userdef:
			x = list(diction.keys()).index(stack[0])
			y = table_term_list.index(buffer[-1])
			if parsing_table[x][y] != '':
				entry = parsing_table[x][y]
				log.append({
				'input_buffer': ''.join(stack),
				'stack': ''.join(buffer),
				'action': f"T[{stack[0]}][{buffer[-1]}] = {entry}"
        })
				print("{:>20} {:>20} {:>25}".
					format(' '.join(buffer),
							' '.join(stack),
							f"T[{stack[0]}][{buffer[-1]}] = {entry}"))
				lhs_rhs = entry.split("->")
				lhs_rhs[1] = lhs_rhs[1].replace('ε', '').strip()
				entryrhs = lhs_rhs[1].split()
				stack = entryrhs + stack[1:]
			else:
				return jsonify(log)
		else:
			if stack[0] == buffer[-1]:
				log.append({
				'input_buffer': ''.join(stack),
				'stack': ''.join(buffer),
				'action': f"Matched:{stack[0]}"
        })
				print("{:>20} {:>20} {:>20}"
					.format(' '.join(buffer),
							' '.join(stack),
							f"Matched:{stack[0]}"))
				buffer = buffer[:-1]
				stack = stack[1:]
			else:
				return jsonify(log)
			
def segregate_symbols(lhs,rhs):
	global nonterm_userdef, term_userdef
	# Add LHS as a non-terminal if not already present
	if lhs not in nonterm_userdef:
			nonterm_userdef.append(lhs)

	# Process each production rule in RHS
	for production in rhs:
			# Add symbols to their respective lists
			for symbol in production:
					# Non-terminal symbols (assumed to be uppercase)
					if symbol.isupper() and symbol not in nonterm_userdef:
							nonterm_userdef.append(symbol)
					# Terminal symbols (typically lowercase or other characters)
					elif (symbol.islower() or symbol not in nonterm_userdef + term_userdef) and symbol != 'ε':
							term_userdef.append(symbol)

	# Remove duplicates by converting to a set and back to a list
	nonterm_userdef = list(set(nonterm_userdef))
	term_userdef = list(set(term_userdef))

	return jsonify(nonterm_userdef, term_userdef)


def compute_parsing(input_string):
	global rules, diction, firsts, follows, start_symbol, nonterm_userdef, term_userdef
	rules = rules.splitlines()

	# Process rules rules
	for rule in rules:
			if '->' in rule:
					k = rule.split("->")
					lhs = k[0].strip()
					rhs = k[1].strip()
					# Split only if "|" is present in rhs
					if '|' in rhs:
							rhs = [r.strip().split() for r in rhs.split('|')]
					else:
							rhs = [rhs.split()]
					diction[lhs] = rhs
					segregate_symbols(lhs, rhs)
			else:
					print(f"Skipping invalid rule: {rule}")

	print(f"term_userdef: {term_userdef},nonterm_userdef:{nonterm_userdef}")
	computeAllFirsts()
	start_symbol = list(diction.keys())[0]
	computeAllFollows()
	parsing_table, result, tabTerm = createParseTable()

	validateStringUsingStackBuffer(parsing_table, result, tabTerm, input_string, term_userdef, start_symbol)

	return parsing_table,


from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

@app.route('/recursion', methods=['POST'])
def parse_input():
	global rules,term_userdef
	data = request.get_json()
	rules = data.get('rules')
	inputString = data.get('inputString')
	print(inputString)
	
	if not rules or not inputString:
		return jsonify({'error': 'rules and Input String are required.'}), 400
	
	parsing_table, = compute_parsing(inputString)
	print(parsing_table)
	term_userdef.append('$')
	return jsonify({'parsing_table': parsing_table, 
        'firsts': {k: list(v) for k, v in firsts.items()},
        'follows': {k: list(v) for k, v in follows.items()},
				'log':log,
				'nonterm_userdef': ntlist, 'term_userdef': term_userdef})

if __name__ == '__main__':
  app.run(debug=True)
