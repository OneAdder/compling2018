"""Тут код, результаты в result.json"""

import json
import pandas as pd

from yargy import Parser, rule, or_
from yargy.pipelines import morph_pipeline, caseless_pipeline
from yargy.interpretation import fact
from yargy.predicates import in_

data = pd.read_csv('pristavki.csv', header=None, names=['text'])

Game = fact(
    'game',
    ['series', 'name', 'release'],
)

zelda = rule(
    morph_pipeline([
        'The Legend of Zelda',
        'Зельда',
        'Zelda',
    ]).interpretation(Game.series.const('The Legend of Zelda')),
    morph_pipeline([
        'Ocarina of Time',
        'Breath of the Wild',
        'Majors mask',
        'A Link Between Worlds',
        'Skyward Sword',
        'Wind Waker',
    ]).interpretation(Game.name).optional(),
    morph_pipeline(['3D', 'HD']).interpretation(Game.release).optional(),
)

gta = rule(
    morph_pipeline([
        'Grand Theft Auto',
        'GTA',
        'ГТА',
    ]).interpretation(Game.series.const('Grand Theft Auto')),
    morph_pipeline([
        '3', '4', '5',
        'San Andreas',
        'Vice City',
        'Chinatown Wars',
        'Liberty City Stories',
        'Vice City Stories',
    ]).interpretation(Game.name),
    morph_pipeline([]).interpretation(Game.release).optional()
)

megaten = rule(
    morph_pipeline([
        'Shin Megami Tensei',
        'Megami Tensei',
    ]).interpretation(Game.series),
    morph_pipeline([
        'Persona',
        'Devil Summoner',
        'Digital Devil Saga',
        'Devil Children Shiro',
    ]).interpretation(Game.name),
    in_('234').interpretation(Game.release).optional(),
)

assassin = rule(
    morph_pipeline([
        "Assassin's Creed",
        'Ассассин',
        'Ассассин Крид',
        'Ассассинс Крид',
    ]).interpretation(Game.series.const("Assassin's Creed")),
    morph_pipeline([
        '2', '3', '4',
        'II', 'III', 'IV',
        'Unity', 'Единство',
        'Syndicate', 'Синдикат',
        'Rogue', 'Изгой',
    ]).interpretation(Game.name),
    morph_pipeline([
        'Bloodlines',
        'Liberation',
        'Black Flag',
        'Чёрный флаг',
    ]).interpretation(Game.release).optional(),
)

colda = rule(
    morph_pipeline([
        'Call Of Duty',
        'Gall Of Duty',
        'кол оф дьюти',
        'колда',
    ]).interpretation(Game.series.const('Call Of Duty')),
    morph_pipeline([
        'MW',
        'Modern Warfare',
        'Advanced Warfare',
        'Black Ops',
    ]).interpretation(Game.name),
    morph_pipeline([
        '1', '2', '3',
        'I', 'II', 'III',
        'Declassified',
    ]).interpretation(Game.release).optional(),
)

#можно нанять эксперта и продолжать, но в идеале тут нужна языковая модель: слишком много вариантов

gm = or_(zelda, gta, megaten, assassin, colda).interpretation(Game)

parser = Parser(gm)
matches = []

for sent in data.text:
    for match in parser.findall(sent):
        matches.append(match.fact.as_json)

print(len(matches))#622
with open('result.json', 'w') as f:
    json.dump(matches, f, ensure_ascii=False, indent=4)
