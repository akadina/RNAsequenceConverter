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
    
'''def single_insertion(tls, pos1, pos2, base, twoprime='r', thio):
    #just in case user swapped pos1 and pos2
    if pos2 < pos1: pos1, pos2 = pos2, pos1
    # because Python is zero-based and humans are one-based
    pos1, pos2 = pos1 - 1, pos2 - 1
    if pos2 - pos1 != 1:
        print('No insertion has been made.')
        print('Positions entered are not consecutive')
        return(tls)
    
    elif pos1 < -1 or pos1 > len(tls) / 4:
        print('No insertion has been made.')
        print('Cannot insert there')
        return(tls)
    
    elif base not in 'ACGUX':
        print('No insertion has been made.')
        print('Base not valid')
        return(tls)
    
    two_prime_abbs = {'OH': 'r', 'Methyl': 'm', 'Fluoro': 'f'}
    
    if pos1 == len(tls) / 4: mod = '-' + base + two_prime_abbs[twoprime]
    else: mod = '-' + base + two_prime_abbs[twoprime] + ('o' if thio == False else 's')
    modified_tls = tls[:((pos1 + 1) * 4)] + mod + tls[(pos1 + 1) * 4:]
    return modified_tls'''

def single_replacement(tls, pos, base, twoprime, thio):
    
    # because Python is zero-based and humans are one-based
    pos = int(pos) - 1
    true_or_false = {'true': True, 'false': False}
    if base == 'X': twoprime = 'x'
    
    if pos < 0 or pos > len(tls) // 4:
        return('Cannot make this replacement')
    
    elif base not in 'ACGUX':
        return('No replacement has been made. Base not valid')

    two_prime_abbs = {'vanilla': 'r', 'methyl': 'm', 'fluoro': 'f', 'x': 'x'}
    
    if pos == len(tls) // 4:
        return tls[:((pos) * 4)] + '-' + base + two_prime_abbs[twoprime]
        
    else:
        mod = '-' + base + two_prime_abbs[twoprime] + ('s' if true_or_false[thio] else 'o')
        return tls[:((pos) * 4)] + mod + tls[(pos + 1) * 4:]


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

@app.route('/get_repl_tls/<tls>/<replacement_pos>/<replacement_base>/<twoprime>/<thiophosphoryl>')
def get_repl_tls(tls, replacement_pos, replacement_base, twoprime, thiophosphoryl):
    replaced = single_replacement(tls, replacement_pos, replacement_base, twoprime, thiophosphoryl)
    return replaced
    
# Run the server
if __name__ == "__main__":
    app.run()