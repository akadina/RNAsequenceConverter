# Imports
import sciris as sc
import scirisweb as sw

#####################
#%% Code part
#####################

__version__ = '0.1.4' # Specify a version

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
    
'''def single_insertion(tls, pos1, pos2, base, twoprime='r', thio=False):
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
    
    if pos < 0 or pos > len(tls) / 4:
        return('Cannot make this replacement')
    
    elif base not in 'ACGUX':
        return('No replacement has been made. Base not valid')

    two_prime_abbs = {'vanilla': 'r', 'methyl': 'm', 'fluoro': 'f', 'x': 'x'}
    
    if pos == len(tls) / 4: mod = '-' + base + two_prime_abbs[twoprime]
        
    else: mod = '-' + base + two_prime_abbs[twoprime] + ('s' if true_or_false[thio] else 'o')
    modified_tls = tls[:((pos) * 4)] + mod + tls[(pos + 1) * 4:]
    
    return modified_tls


#####################
#%% Webapp part
#####################

# Create the app
app = sw.ScirisApp(__name__, name="RNASequenceConverter", server_port=8181) # Set to a nonstandard port to avoid collisions

# Define the API for the tool
@app.route('/get_tls/<sequence>/<fiveend>/<threeend>')
def get_tls(sequence, fiveend, threeend):
    print('get_tls() called')
    tls = three_letter_seq(sequence, fiveend, threeend)
    return tls

@app.route('/get_repl_tls/<tls>/<replacement_pos>/<replacement_base>/<twoprime>/<thiophosphoryl>')
def get_repl_tls(tls, replacement_pos, replacement_base, twoprime, thiophosphoryl):
    print('get_repl_tls() called')
    replaced = single_replacement(tls, replacement_pos, replacement_base, twoprime, thiophosphoryl)
    return replaced

# Get the version
@app.route('/get_version')
def get_version():
    print('get_version() called')
    return __version__

# Allow for automatic updates from GitHub
@app.route('/gitupdate') # The URL will be e.g. rna.ocds.co/gitupdate
def git_update():
    print('git_update() called')
    from flask import request
    json = request.get_json() # Get the actual data from GitHub
    if json is not None and json.get('ref') == 'refs/heads/master': # Check that it's right
        sc.runcommand('echo "Push received at %s, server going DOWN!" >> tmp.log' % sc.getdate(), printinput=True)
        sc.runcommand('git pull', printinput=True, printoutput=True) # Get new files from GitHub
        sc.runcommand('./restart_server') # Nothing after this will run because this kills the server, lol
    return 'OK' # Will only be displayed if the command above is NOT run

# Run the server
if __name__ == "__main__":
    app.run()
