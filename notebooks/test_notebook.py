from nltk import CFG
from nltk.parse.generate import generate

#%%
# First note of Song of sorrows 
rules = """

    A12 -> 'AAAAAAAAAAAA'

"""

grammar = CFG.fromstring(rules)

#%%
grammar

#%%
# Create a generator which uses lazy evaluation
generate(grammar)

#%%
# Use next to get the next 'phrase' or element in the gramamr,
#    which is the 12 Ays in this case
phrase = next(generate(grammar))
phrase

#%% 
# :Globals:
AllRules = dict(
    banjo_rules_old1 = """
        "A12 -> 'AdAdAdAdAdAd'"
    """,
    # This says 12 maps to 2 2 2 2 2 2 (6 beats of 2, I guess)
    # 2 is melody string1 so it becomes 
    #   melody string1 2 2 2 2 2
    #   melody is A and string1 is d so this becomes
    # 12 -> Ad Ad Ad Ad Ad Ad
    # So this is equivalent to the above, banjo_rules_old1
    banjo_rules_old2 = """
     12 -> 2 2 2 2 2 2
      2 -> melody string1
     string1 -> 'd'
     melody -> 'A'
    """,
    
    banjo_rules = """
      16 -> 3 3 3 3 4
      12 -> 3 3 3 3
      8 -> 3 3 2
      4 -> melody string1 string5 string1
      3 -> melody string1 string5
      2 -> melody string1
      string1 -> 'd'
      string5 -> 'g'
      melody -> '{pitch}' 
    """
)

HEADER = """
    X: 1
    %%titleleft 1
    T: {title}
    L: 1/16
    Q: {tempo}
    K: {key}
    %%printtempo false
    %%MIDI program 105"""

TEMPO = 130
KEY = 'D'

#%%
def banjoify(rules):
    grammar = CFG.fromstring(rules)
    phrase = next(generate(grammar))
    return ''.join(phrase)

def runsh(*strings):
    return subprocess.run(*strings)


def make_abc_files(abc, title='', lyrics='', tempo=TEMPO, key=KEY,
            soundfont_path='./GeneralUser GS v1.471.sf2'):

    if not os.path.exists(soundfont_path):
        raise FileNotFoundError(f'Could not find {soundfont_path}')

    print(abc)
    header = HEADER.format(title=title, tempo=str(tempo), key=key)
    uuid = str(uuid4())
    abc_filename = uuid + '.abc'

    # Write the song information to file
    with open(abc_filename, 'w') as f:
        f.write('\n'.join([header, abc, lyrics]))

    # Create an svg of the song using abcm2ps
    #  PS meaning postcript
    #  -g Produce svg output
    svg_filename = 'Out001.svg'
    subprocess.run(['abc2ps', ])
    # display(SVG(svg_filename))

    midi_filename = uuid + '.mid'
    runsh('abc2midi', abc_filename, '-o', midi_filename)
    
    wav_filename = random_string + '.wav'
    subprocess.run(['fluidsynth', '-i', '-F', wav_filename, soundfont_path, midi_filename])        
    # for use in ipython notebook
    # display(Audio(wav_filename))

    # os.remove(abc_filename)
    # etc.
    
    return dict(
        abc_filename=abc_filename,
        midi_filename=midi_filename,
        svg_filename=svg_filename,
        wav_filename=wav_filename
    )


    


def play(abc, title='', lyrics='', tempo=TEMPO, key=KEY, 
         soundfont_path = './GeneralUser GS v1.471.sf2'):
    
    if not os.path.exists(soundfont_path):
        raise FileNotFoundError(f'Could not find {soundfont_path}')
    
    print(abc)
    header = HEADER.format(title=title, tempo=str(tempo), key=key)
    random_string = str(uuid4())
    abc_filename = random_string + '.abc'
    with open(abc_filename, 'w') as f:
        f.write('\n'.join([header, abc, lyrics]))

    svg_filename = 'Out001.svg'
    subprocess.run(['abcm2ps', '-g', abc_filename])
    display(SVG(svg_filename))
    
    midi_filename = random_string + '.mid'
    subprocess.run(['abc2midi', abc_filename, '-o', midi_filename])
    
    wav_filename = random_string + '.wav'
    subprocess.run(['fluidsynth', '-i', '-F', wav_filename, soundfont_path, midi_filename])        
    display(Audio(wav_filename))
           
    os.remove(abc_filename)     
    os.remove(svg_filename)
    os.remove(midi_filename)
    os.remove(wav_filename)



banjoify(rules)
#%%
play(banjoify(phrase))

#%%
