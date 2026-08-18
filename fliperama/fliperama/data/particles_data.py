# -*- coding: utf-8 -*-
"""
Dados de física de partículas usados em todas as telas.
Portado do app original em React (Retro Game Physics App).
"""

# Cada cubo físico (com tag RFID) representa uma dessas partículas.
# A chave é o "id" usado em RFID_MAP (data/rfid_map.json).
PARTICLES = {
    "eletron": {
        "name": "Elétron",
        "type": "Lépton",
        "charge": "-1",
        "spin": "1/2",
        "mass": "0.511 MeV/c²",
        "description": (
            "O elétron é uma partícula fundamental que orbita o núcleo "
            "atômico. Possui carga elétrica negativa e é essencial para "
            "a química e a eletricidade."
        ),
        "color": (0, 255, 255),
    },
    "quark_up": {
        "name": "Quark Up",
        "type": "Quark",
        "charge": "+2/3",
        "spin": "1/2",
        "mass": "2.2 MeV/c²",
        "description": (
            "O quark up é um dos quarks mais leves e, junto com o quark "
            "down, forma prótons e nêutrons."
        ),
        "color": (255, 0, 255),
    },
    "quark_down": {
        "name": "Quark Down",
        "type": "Quark",
        "charge": "-1/3",
        "spin": "1/2",
        "mass": "4.7 MeV/c²",
        "description": (
            "O quark down é fundamental na composição dos núcleos "
            "atômicos, formando prótons e nêutrons junto com o quark up."
        ),
        "color": (255, 255, 0),
    },
    "foton": {
        "name": "Fóton",
        "type": "Bóson",
        "charge": "0",
        "spin": "1",
        "mass": "0",
        "description": (
            "O fóton é a partícula mediadora da força eletromagnética. "
            "Não tem massa e viaja à velocidade da luz."
        ),
        "color": (255, 215, 0),
    },
    "neutrino": {
        "name": "Neutrino",
        "type": "Lépton",
        "charge": "0",
        "spin": "1/2",
        "mass": "< 1 eV/c²",
        "description": (
            "Os neutrinos são partículas quase sem massa que interagem "
            "muito fracamente com a matéria, atravessando planetas "
            "inteiros sem serem detectados."
        ),
        "color": (180, 180, 255),
    },
    "gluon": {
        "name": "Glúon",
        "type": "Bóson",
        "charge": "0",
        "spin": "1",
        "mass": "0",
        "description": (
            "O glúon é o mediador da força nuclear forte, responsável "
            "por manter quarks unidos dentro de prótons e nêutrons."
        ),
        "color": (0, 255, 0),
    },
    "positron": {
        "name": "Pósitron",
        "type": "Antilépton",
        "charge": "+1",
        "spin": "1/2",
        "mass": "0.511 MeV/c²",
        "description": (
            "O pósitron é a antipartícula do elétron: mesma massa, "
            "carga oposta."
        ),
        "color": (255, 100, 100),
    },
    "higgs": {
        "name": "Bóson de Higgs",
        "type": "Bóson",
        "charge": "0",
        "spin": "0",
        "mass": "125.25 GeV/c²",
        "description": (
            "O bóson de Higgs está associado ao campo de Higgs, que dá "
            "massa às partículas fundamentais."
        ),
        "color": (255, 165, 0),
    },
}

LEPTONS = [
    {"name": "Elétron (e⁻)", "charge": "-1", "mass": "0.511 MeV", "generation": "1ª"},
    {"name": "Múon (μ⁻)", "charge": "-1", "mass": "105.7 MeV", "generation": "2ª"},
    {"name": "Tau (τ⁻)", "charge": "-1", "mass": "1777 MeV", "generation": "3ª"},
    {"name": "Neutrino do Elétron (νₑ)", "charge": "0", "mass": "< 1 eV", "generation": "1ª"},
    {"name": "Neutrino do Múon (νμ)", "charge": "0", "mass": "< 1 eV", "generation": "2ª"},
    {"name": "Neutrino do Tau (ντ)", "charge": "0", "mass": "< 1 eV", "generation": "3ª"},
]

QUARKS = [
    {"name": "Up (u)", "charge": "+2/3", "mass": "2.2 MeV", "generation": "1ª", "color": (255, 0, 0)},
    {"name": "Down (d)", "charge": "-1/3", "mass": "4.7 MeV", "generation": "1ª", "color": (0, 255, 0)},
    {"name": "Charm (c)", "charge": "+2/3", "mass": "1.28 GeV", "generation": "2ª", "color": (255, 0, 255)},
    {"name": "Strange (s)", "charge": "-1/3", "mass": "96 MeV", "generation": "2ª", "color": (255, 255, 0)},
    {"name": "Top (t)", "charge": "+2/3", "mass": "173 GeV", "generation": "3ª", "color": (0, 255, 255)},
    {"name": "Bottom (b)", "charge": "-1/3", "mass": "4.18 GeV", "generation": "3ª", "color": (255, 136, 0)},
]

ANTIMATTER_PAIRS = [
    {"particle": "Elétron (e⁻)", "antiparticle": "Pósitron (e⁺)", "charge": "-1 → +1"},
    {"particle": "Próton (p)", "antiparticle": "Antipróton (p̄)", "charge": "+1 → -1"},
    {"particle": "Nêutron (n)", "antiparticle": "Antinêutron (n̄)", "charge": "0 → 0"},
    {"particle": "Neutrino (ν)", "antiparticle": "Antineutrino (ν̄)", "charge": "0 → 0"},
]

FORCES = [
    {
        "name": "Força Nuclear Forte",
        "icon": "forte",
        "carrier": "Glúon",
        "description": "Mantém quarks unidos dentro de prótons e nêutrons. É a mais intensa das 4 forças, mas atua só a curtíssima distância.",
    },
    {
        "name": "Força Eletromagnética",
        "icon": "eletro",
        "carrier": "Fóton",
        "description": "Responsável pela luz, eletricidade e magnetismo. Atua entre partículas com carga elétrica, a qualquer distância.",
    },
    {
        "name": "Força Nuclear Fraca",
        "icon": "fraca",
        "carrier": "Bósons W e Z",
        "description": "Responsável pelo decaimento radioativo e pela fusão nuclear no Sol. Muda o \"sabor\" dos quarks e léptons.",
    },
    {
        "name": "Gravidade",
        "icon": "gravidade",
        "carrier": "Gráviton (hipotético)",
        "description": "A mais fraca das 4 forças em escala de partículas, mas domina em grandes escalas: planetas, estrelas e galáxias.",
    },
]

QUIZ_QUESTIONS = [
    {
        "question": "Qual é a partícula responsável pela força eletromagnética?",
        "options": ["Glúon", "Fóton", "Bóson W", "Gráviton"],
        "correct": 1,
        "explanation": "O fóton é a partícula mediadora da força eletromagnética, responsável pela luz e pelas interações elétricas e magnéticas.",
    },
    {
        "question": "Quantos tipos de quarks existem no Modelo Padrão?",
        "options": ["3", "4", "6", "8"],
        "correct": 2,
        "explanation": "Existem 6 tipos (sabores) de quarks: up, down, charm, strange, top e bottom.",
    },
    {
        "question": "Qual partícula tem carga elétrica negativa?",
        "options": ["Próton", "Nêutron", "Elétron", "Neutrino"],
        "correct": 2,
        "explanation": "O elétron possui carga elétrica negativa (-1), enquanto o próton é positivo e o nêutron/neutrino são neutros.",
    },
    {
        "question": "O que é antimatéria?",
        "options": ["Matéria negativa", "Matéria com carga oposta", "Matéria do futuro", "Matéria imaginária"],
        "correct": 1,
        "explanation": "Antimatéria é composta por antipartículas, que têm a mesma massa mas propriedades opostas (como carga) das partículas normais.",
    },
    {
        "question": "Qual força mantém os quarks unidos dentro do próton?",
        "options": ["Gravidade", "Força fraca", "Força forte", "Eletromagnetismo"],
        "correct": 2,
        "explanation": "A força nuclear forte, mediada pelos glúons, mantém os quarks unidos dentro de prótons e nêutrons.",
    },
]

# ---------------------------------------------------------------------------
# Quarks disponíveis no minigame "Jogo dos Hádrons" (inclui antiquarks,
# necessários para montar mésons como píon e káon).
# ---------------------------------------------------------------------------
AVAILABLE_QUARKS = [
    {"symbol": "u", "name": "Up", "charge": 2 / 3, "color": (255, 0, 0), "anti": False},
    {"symbol": "d", "name": "Down", "charge": -1 / 3, "color": (0, 255, 0), "anti": False},
    {"symbol": "c", "name": "Charm", "charge": 2 / 3, "color": (255, 0, 255), "anti": False},
    {"symbol": "s", "name": "Strange", "charge": -1 / 3, "color": (255, 255, 0), "anti": False},
    {"symbol": "ū", "name": "Anti-Up", "charge": -2 / 3, "color": (255, 120, 120), "anti": True},
    {"symbol": "d̄", "name": "Anti-Down", "charge": 1 / 3, "color": (120, 255, 120), "anti": True},
    {"symbol": "s̄", "name": "Anti-Strange", "charge": 1 / 3, "color": (255, 255, 150), "anti": True},
]

# Hádrons-alvo do minigame. "quarks" é a composição exata esperada
# (ordem não importa, mas a contagem de cada símbolo sim).
HADRONS = [
    {"name": "Próton", "quarks": ["u", "u", "d"], "charge": 1},
    {"name": "Nêutron", "quarks": ["u", "d", "d"], "charge": 0},
    {"name": "Píon+", "quarks": ["u", "d̄"], "charge": 1},
    {"name": "Píon-", "quarks": ["d", "ū"], "charge": -1},
    {"name": "Káon+", "quarks": ["u", "s̄"], "charge": 1},
    {"name": "Káon0", "quarks": ["d", "s̄"], "charge": 0},
]
