# Imports
import scirisweb as sw

#####################
#%% Code part
#####################

def three_letter_seq(sequence, thio_end5, thio_end3):

    seq = sequence.upper()
    new_seq = ''
    for i in range(len(seq)):
        if seq[i] not in 'ACGTU':
            return('Sequence not valid')
        if seq[i] == 'T': new_seq += 'U'
        else: new_seq += seq[i]

    s = ''
    thio_end5 = int(thio_end5)
    thio_end3 = int(thio_end3)
    if thio_end3 < 0: return ''
    for i in range(len(new_seq)):
        if i == len(new_seq) - 1: s = s + '-' + new_seq[i] + ('r' if thio_end3 == 0 else 'm')
        elif i < thio_end5 or i > (len(new_seq) - thio_end3 - 1): s = s + '-' + new_seq[i] + 'ms'
        else: s = s + '-' + new_seq[i] + 'ro'
    return s

def sequence_length(sequence):
    if len(sequence) == 0: return ''
    
    for i in range(len(sequence)):
        if sequence[i] not in 'ACGTU':
            return('')

    return "Sequence length: " + str(len(sequence))

def isolate_sequence(tls):
    sequence = ''
    for i in range(len(tls)):
        if tls[i] in 'ACGUX':
            sequence += tls[i]
            
    return sequence

def sequence_x_length(seq):
    if len(seq) == 0: return ''
    
    for i in range(len(seq)):
        if seq[i] not in 'ACGUX':
            return('')

    return "Sequence length: " + str(len(seq))
    
def single_replacement(tls, pos, base, twoprime, thio):
    
    # because Python is zero-based and humans are one-based
    pos = int(pos) - 1
    
    if pos < 0 or pos > len(tls) // 4:
        return('Cannot make this replacement')
    
    elif base not in 'ACGUX':
        return('No replacement has been made. Base not valid')
    
    if base == 'X': twoprime = 'x'
    two_prime_abbs = {'r_vanilla': 'r', 'r_methyl': 'm', 'r_fluoro': 'f', 'x': 'x'}
    true_or_false = {'true': True, 'false': False}
    
    if pos == len(tls) // 4:
        return tls[:((pos) * 4)] + '-' + base + two_prime_abbs[twoprime]
        
    else:
        mod = '-' + base + two_prime_abbs[twoprime] + ('s' if true_or_false[thio] else 'o')
        return tls[:((pos) * 4)] + mod + tls[(pos + 1) * 4:]

def single_insertion(tls, pos1, pos2, base, twoprime, thio):
    
    pos1, pos2 = int(pos1), int(pos2)
    #just in case user swapped pos1 and pos2
    if pos2 < pos1: pos1, pos2 = pos2, pos1
    # because Python is zero-based and humans are one-based
    pos1, pos2 = pos1 - 1, pos2 - 1
    if pos2 - pos1 != 1:
        return('No insertion has been made. Positions entered are not consecutive.')
    
    elif pos1 < -1 or pos1 > len(tls) // 4:
        return('No insertion has been made. No valid position given')
    
    elif base not in 'ACGUX':
        return('No insertion has been made. Base not valid')
    
    if base == 'X': twoprime = 'x'
    two_prime_abbs = {'i_vanilla': 'r', 'i_methyl': 'm', 'i_fluoro': 'f', 'x': 'x'}
    true_or_false = {'true': True, 'false': False}
    
    if pos1 == len(tls) / 4: mod = '-' + base + two_prime_abbs[twoprime]
    else: mod = '-' + base + two_prime_abbs[twoprime] + ('s' if true_or_false[thio] else 'o')
    return tls[:((pos1 + 1) * 4)] + mod + tls[(pos1 + 1) * 4:]
    
#####################
#%% Webapp part
#####################

# Create the app
app = sw.ScirisApp(__name__, name="RNASequenceConverter", server_port=8181) # Set to a nonstandard port to avoid collisions

# Define the API
@app.route('/get_tls/<sequence>/<fiveend>/<threeend>')
def get_tls(sequence, fiveend, threeend):
    tls = three_letter_seq(sequence, fiveend, threeend)
    return tls
    
@app.route('/get_sequence_length/<sequence>')
def get_sequence_length(sequence):
    length = sequence_length(sequence)
    return length

@app.route('/get_repl_tls/<tls>/<replacement_pos>/<replacement_base>/<r_twoprime>/<r_thiophosphoryl>')
def get_repl_tls(tls, replacement_pos, replacement_base, r_twoprime, r_thiophosphoryl):
    replaced = single_replacement(tls, replacement_pos, replacement_base, r_twoprime, r_thiophosphoryl)
    return replaced

@app.route('/get_replacement_length/<tls_replacement>')
def get_replacement_length(tls_replacement):
    seq = isolate_sequence(tls_replacement)
    return sequence_x_length(seq)
    
@app.route('/get_insertion_tls/<tls>/<pos1>/<pos2>/<insertion_base>/<i_twoprime>/<i_thiophosphoryl>')
def get_insertion_tls(tls, pos1, pos2, insertion_base, i_twoprime, i_thiophosphoryl):
    inserted = single_insertion(tls, pos1, pos2, insertion_base, i_twoprime, i_thiophosphoryl)
    return inserted
    
@app.route('/get_insertion_length/<tls_insertion>')
def get_insertion_length(tls_insertion):
    seq = isolate_sequence(tls_insertion)
    return sequence_x_length(seq)
    
# Run the server
if __name__ == "__main__":
    app.run()