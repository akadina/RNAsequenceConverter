# Imports
import scirisweb as sw

#####################
#%% Code part
#####################

def three_letter_seq(sequence, thio_end5, thio_end3):
    s = ''
    thio_end5 = int(thio_end5)
    thio_end3 = int(thio_end3)
    if thio_end3 < 0: return ''
    for i in range(len(sequence)):
        if i == len(sequence) - 1: s = s + '-' + sequence[i] + ('r' if thio_end3 == 0 else 'm')
        elif i < thio_end5: s = s + '-' + sequence[i] + 'ms'
        elif i > (len(sequence) - thio_end3 - 1): s = s + '-' + sequence[i] + 'ms'
        else: s = s + '-' + sequence[i] + 'ro'
    return s

def single_insertion(tls, pos1, pos2, base, twoprime='r', thio=False):
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
    return modified_tls

def single_replacement(tls, pos, base, twoprime='r', thio=False):

    # because Python is zero-based and humans are one-based
    pos -= 1
    
    if pos < 0 or pos > len(tls) / 4:
        print('No replacement has been made.')
        print('Cannot replace base that does not exist.')
        return(tls)
    
    elif base not in 'ACGUX':
        print('No replacement has been made.')
        print('Base not valid')
        return(tls)
    
    two_prime_abbs = {'OH': 'r', 'Methyl': 'm', 'Fluoro': 'f'}
    
    if pos == len(tls) / 4: mod = '-' + base + two_prime_abbs[twoprime]
        
    else: mod = '-' + base + two_prime_abbs[twoprime] + ('o' if thio == False else 's')
    modified_tls = tls[:((pos) * 4)] + mod + tls[(pos + 1) * 4:]
    return modified_tls


def read_sequence(s):
    #read sequence. Ensure no errors (AGCU) If any T's - convert to U's
    sequence = s.upper()
    seq = ''
    flag = 1
    for i in range(len(sequence)):
        if sequence[i] not in 'ACGTU':
            flag = 0
            break
        if sequence[i] == 'T': seq += 'U'
        else: seq += sequence[i]
    
    if flag != 0:
        print(seq)
        print("Sequence length: " + str(len(seq)))
    else: print('Sequence not valid')
    return sequence


def make_sequence(seq, thio_end5, thio_end3):
    tls = three_letter_seq(seq, thio_end5, thio_end3)
    print('Standard three letter sequence is: ')
    print(tls)
    return tls


#####################
#%% Webapp part
#####################

# Create the app
app = sw.ScirisApp(__name__, name="RNASequenceConverter", server_port=8181) # Set to a nonstandard port to avoid collisions

# Define the API
@app.route('/get_tls/<sequence>/<fiveend>/<threeend>') # Define the route -- requires 3 inputs
def get_tls(sequence, fiveend, threeend):
    tls = three_letter_seq(sequence, fiveend, threeend) # Actually make the thing
    return tls

# Allow for automatic updates
@app.route('/gitupdate', methods=['POST']) # The URL will be e.g. rna.ocds.co/gitupdate
def git_update():
    from flask import request
    json = request.get_json() # Get the actual data from GitHub
    if json.get('ref') == 'refs/heads/master': # CHck that it's right
        print('Push received, server going DOWN!')
        sc.runcommand('git pull') # Get new files from GitHub
        sc.runcommand('./restart_server') # Nothing after this will run because this kills the server, lol
    return 'OK' # Will only be displayed if the command above is NOT run

# Run the server
if __name__ == "__main__":
    app.run()