import pandas as pd
from math import ceil
import numpy as np


def check_type(flags):
    try:
        if 'BASEANGBAND' in flags:
            return 'Base'
        elif 'ZANGBAND' in flags:
            return 'Zangband'
        elif 'CTHANGBAND' in flags:
            return 'Cthulhu'
        elif 'PERNANGBAND' in flags:
            return 'Pern'
        elif 'BLUEBAND' in flags:
            return 'Blue'
        elif 'JOKEANGBAND' in flags:
            return 'Joke'
        else:
            return 'None'
    except TypeError:
        return ''


def check_unique(flags):
    try:
        if 'UNIQUE' in flags:
            return 'YES'
        else:
            return 'No'
    except TypeError:
        return ''


def calc_hp(monster):
    try:
        hd = monster.hp
        h1, h2 = hd.split('d')
        t3 = f'~{int(h1) * (1 + int(h2) // 2)}' if 'FORCE_MAXHP' not in monster[
            'flags'] else (int(h1) * int(h2))
        return f'{t3} ({h1}d{h2})'
    except AttributeError:
        return


def make_description(monster):
    descr = monster.description
    try:
        if descr[0].isalpha() and descr[1].isalpha():
            t2 = f'\lettrine{{{descr[0]}}}{{{descr[1:descr.find(" ")]}}}{descr[descr.find(" "):]}\n'
            t2 += f'\settoheight{{\heightofhw}}{{\\vbox{{{descr}}}}}\n'
            t2 += '\equalitytest{\heightofhw}'
        else:
            t2 = descr
        t2 += '\n'
    except TypeError:
        t2 = ''
    return t2


def make_main(monster):
    t3 = f'\\textbf{{Type:}} {check_type(monster["flags"])} '
    t3 += f'\\textbf{{Unique:}} {check_unique(monster["flags"])} '
    t3 += f'\\textbf{{Id:}} {monster.name}\n'
    return t3


def make_atacks(monster):
    at = '\\textbf{Attack methods:}\n\n'
    for attack in monster.attack:
        at1, *at2 = attack
        at += f'{at1}: {" ".join(at2)}\n\n'
    at += '\n'
    return at


def make_spells(monster):
    _, w = monster.chance.split('_IN_')
    t = f'\\textbf{{Spell chance:}} 1 spell every {w} turns (1_IN_{w})\n'
    t += f'\\begin{{longtable}}{{lll}}\n\caption*{{Spells (and breaths, arrows or missiles): ({len(monster.spells)})}}\\\\\n'
    lines = ceil(len(monster.spells) / 3)
    for i in range(lines):
        line = monster.spells[i * 3 : i * 3 + 3]
        t += (' & '.join(line))
        t += '\\\\\n'
    t += '\end{longtable}'
    return t


def make_flags(monster):
    t = f'\\begin{{longtable}}{{lll}}\n\caption*{{Flags: ({len(monster["flags"])})}}\\\\\n'
    lines = ceil(len(monster['flags']) / 3)
    for i in range(lines):
        line = monster['flags'][i * 3 : i * 3 + 3]
        t += ('& '.join(line))
        t += '\\\\\n'
    t += '\end{longtable}'
    return t


def to_tex(monster, name='MONSTER.tex'):
    nan = float('nan')
    symbol = monster.symbol.replace('{', '\{')
    t1 = f'\subsection{{{monster.Name}, (Symbol {symbol}, Color {monster.color})}}\n'
    t2 = make_description(monster) + '\n'
    t3 = make_main(monster) + '\n'

    t4 = f'\\textbf{{HP:}} {calc_hp(monster)} \\textbf{{AC:}} {monster.AC} \\textbf{{Experience:}} {monster.exp} \\textbf{{Speed}}: {monster.speed}\n\n'
    t5 = f'\\textbf{{Depth:}} {monster.lvl} ({50*monster.lvl}ft) \\textbf{{Rarity:}} {monster.rarity} \\textbf{{Vision:}} {monster.vision} \\textbf{{Alertness:}} {monster.alertness}\n\n'
    t6 = '\n'
    t7 = f'\\textbf{{Weight:}} {monster.weight} \\textbf{{Weapons:}} {monster.weapons} \\textbf{{Torso:}} {monster.torso} \\textbf{{Arm:}} {monster.arms} \\textbf{{Finger:}} {monster.finger} \\textbf{{Head:}} {monster["head"]} \\textbf{{Leg:}} {monster.leg}\n\n'
    t8 = f'\\textbf{{Treasure:}} {monster.treasure} \\textbf{{Combat:}} {monster.combat} \\textbf{{Magic:}} {monster.magic} \\textbf{{Tool:}} {monster.tool}\n\n'
    if not isinstance(monster.attack, float):
        t9 = make_atacks(monster)
    if not isinstance(monster.chance, float):
        t10 = make_spells(monster)
    if not isinstance(monster['flags'], float):
        t11 = make_flags(monster)
    with open(name, 'a') as file:
        file.write(
            t1.replace('~', r'\textasciitilde'
                       ).replace('#', r'\#').replace('$',
                                                     '\$').replace('^', '\^')
        )
        if t2:
            file.write(t2)
        try:
            file.write(t3)
        except TypeError:
            pass
        file.write(t4)
        file.write(t5)
        file.write(t6)
        file.write(t7)
        file.write(t8)
        try:
            file.write(t9.replace('_', '\_'))
        except UnboundLocalError:
            pass
        try:
            file.write(t10.replace('_', '\_'))
        except UnboundLocalError:
            pass
        try:
            file.write(t11.replace('_', '\_'))
        except UnboundLocalError:
            pass
        file.write('\n')
        file.write('\\newpage\n')


with open('r_info.txt', 'r') as file:
    f = file.read()

info = f[f.find('The Player'):]
info = info.split('\nN:')

new_pd = pd.DataFrame(
    columns=(
        'Name',
        'symbol',
        'color',
        'speed',
        'hp',
        'vision',
        'AC',
        'alertness',
        'lvl',
        'rarity',
        'weight',
        'exp',
        'weapons',
        'torso',
        'arms',
        'finger',
        'head',
        'leg',
        'treasure',
        'combat',
        'magic',
        'tool',
        'attack',
        'flags',
        'chance',
        'spells',
        'description'
    ),
    index=range(2 * len(info) - 1)
)

# new_pd = new_pd.astype({'description': 'string', 'chance': 'string'})
for monster in info[1 :]:
    lines = monster.split('\n')
    ind, name = lines[0].split(':')
    ind = int(ind)
    new_pd.loc[ind, 'Name'] = name

    try:
        g_string = [line for line in lines if 'G:' == line[: 2]][0]
    except:
        pass
    else:
        g, symbol, color = g_string.split(':')
        new_pd.loc[ind, 'symbol'] = symbol
        new_pd.loc[ind, 'color'] = color

    try:
        i_string = [line for line in lines if 'I:' == line[: 2]][0]
    except:
        pass
    else:
        i, speed, hp, vision, ac, alertness = i_string.split(':')
        new_pd.loc[ind, 'speed'] = int(speed)
        new_pd.loc[ind, 'hp'] = hp
        new_pd.loc[ind, 'vision'] = int(vision)
        new_pd.loc[ind, 'AC'] = int(ac)
        new_pd.loc[ind, 'alertness'] = int(alertness)

    try:
        w_string = [line for line in lines if 'W:' == line[: 2]][0]
    except:
        pass
    else:
        w, lvl, rarity, weight, exp = w_string.split(':')
        new_pd.loc[ind, 'lvl'] = int(lvl)
        new_pd.loc[ind, 'rarity'] = int(rarity)
        new_pd.loc[ind, 'weight'] = int(weight)
        new_pd.loc[ind, 'exp'] = int(exp)

    try:
        e_string = [line for line in lines if 'E:' == line[: 2]][0]
    except:
        pass
    else:
        e, weapons, torso, arms, finger, head, leg = e_string.split(':')
        new_pd.loc[ind, 'weapons'] = int(weapons)
        new_pd.loc[ind, 'torso'] = int(torso)
        new_pd.loc[ind, 'arms'] = int(arms)
        new_pd.loc[ind, 'finger'] = int(finger)
        new_pd.loc[ind, 'head'] = int(head)
        new_pd.loc[ind, 'leg'] = int(leg)

    try:
        o_string = [line for line in lines if 'O:' == line[: 2]][0]
    except:
        pass
    else:
        o, treasure, combat, magic, tool = o_string.split(':')
        new_pd.loc[ind, 'treasure'] = int(treasure)
        new_pd.loc[ind, 'combat'] = int(combat)
        new_pd.loc[ind, 'magic'] = int(magic)
        new_pd.loc[ind, 'tool'] = int(tool)

    try:
        b_strings = [line for line in lines if 'B:' == line[: 2]]
        b_strings[-1]
    except:
        pass
    else:
        b = [line[2 :] for line in b_strings]
        b = [attack.split(':') for attack in b]
        new_pd.loc[ind, 'attack'] = b

    try:
        f_strings = [line for line in lines if 'F:' == line[: 2]]
        f_strings[-1]
    except:
        pass
    else:
        f = '|'.join(f_strings)
        f = f.replace('F:', '')
        flags = [flag.replace(' ', '') for flag in f.split('|')]
        flags = [flag for flag in flags if flag]
        new_pd.loc[ind, 'flags'] = flags

    try:
        s_strings = [line for line in lines if 'S:' == line[: 2]]
        s_strings[-1]
    except:
        pass
    else:
        chance, *spells = s_strings
        _, chance = chance.split('S:')
        spells = [
            spell for line in spells for spell in line.split('S:') if spell
        ]
        spells = ''.join(spells)
        spells = spells.replace(' ', '').split('|')
        if spells == ['']:
            # something not nice
            chance, *spells = chance.replace(' ', '').split('|')
            spells = [spell for spell in spells if spell]
            print(f'Problematic id: {ind}')
        else:
            chance = chance.replace('|', '').replace(' ', '')
        new_pd.iloc[ind]['chance'] = chance
        # new_pd[ind,'chance'] = chance
        new_pd.iloc[ind]['spells'] = spells

    try:
        d_strings = [line for line in lines if 'D:' == line[: 2]]
        d_strings[-1]
    except:
        pass
    else:
        d = ' '.join(d_strings).replace(' D:', ' ')[2 :]
        new_pd.iloc[ind]['description'] = d

new_pd = new_pd.dropna(axis=0, how='all')
sorted_pd = new_pd.sort_values(by=['symbol', 'lvl'], kind='mergesort')

t = [
    'UNIQUE' in x if isinstance(x, list) else False for x in sorted_pd['flags']
]

new_groups = [
    "ANIMAL",
    "SPIDER",
    "ORC",
    "TROLL",
    "GIANT",
    "DRAGON",
    "DEMON",
    "UNDEAD",
    "EVIL",
    "DRAGONRIDER",
    "GOOD",
    "NONLIVING",
    "UNIQUE",
    "PSEUDO_UNIQUE"
]

trueth = np.zeros(len(sorted_pd), bool)

i = 0
with open('MONSTER.tex', 'w') as file:
    file.write('\documentclass[t3.tex]{subfiles}\n\n\\begin{document}\n')
for index, monster in sorted_pd.iterrows():
    to_tex(monster)
with open('MONSTER.tex', 'a') as file:
    file.write('\n\end{document}')

for flag in new_groups:
    filetmp = flag.replace('_', '')
    with open(f'{filetmp}.tex', 'w') as file:
        file.write('\documentclass[t3.tex]{subfiles}\n\n\\begin{document}\n')
    index = [
        flag in x if isinstance(x, list) else False for x in sorted_pd['flags']
    ]
    trueth = np.logical_or(index, trueth)
    tmp = sorted_pd[index]
    for index, monster in tmp.iterrows():
        to_tex(monster, f'{flag}.tex')
    with open(f'{flag}.tex', 'a') as file:
        file.write('\n\end{document}')

trueth = np.logical_not(trueth)

rest = sorted_pd[trueth]

with open('REST.tex', 'w') as file:
    file.write('\documentclass[t3.tex]{subfiles}\n\n\\begin{document}\n')
for index, monster in rest.iterrows():
    to_tex(monster, 'REST.tex')
with open('REST.tex', 'a') as file:
    file.write('\n\end{document}')
