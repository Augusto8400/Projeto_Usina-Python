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
        "mass": "0,511 MeV/c²",
        "description": (
            "O elétron foi a primeira partícula subatômica descoberta, em "
            "experimentos realizados por Joseph John Thomson em 1897. É um "
            "dos constituintes básicos dos átomos e é responsável por "
            "transportar a eletricidade nos fios e cabos elétricos. Pertence "
            "à família dos léptons e interage pelas forças eletromagnética, "
            "nuclear fraca e gravitacional. Possui spin 1/2, carga elétrica "
            "-1 e massa de 0,511 MeV/c². Por ser o lépton de menor massa, "
            "é uma partícula estável."
        ),
        "color": (0, 255, 255),
    },

    "muon": {
        "name": "Múon",
        "type": "Lépton",
        "charge": "-1",
        "spin": "1/2",
        "mass": "105,65 MeV/c²",
        "description": (
            "O múon é uma partícula pertencente à família dos léptons e, "
            "por isso, interage pelas forças eletromagnética, nuclear fraca "
            "e gravitacional. Foi descoberto por Carl D. Anderson e Seth "
            "Neddermeyer em 1936, em experimentos de raios cósmicos. Possui "
            "spin 1/2, carga elétrica -1 e massa de 105,65 MeV/c². O múon "
            "decai pela força fraca, convertendo-se em um elétron, um "
            "neutrino do múon e um antineutrino eletrônico, com vida média "
            "de aproximadamente 2,2 × 10^-6 s."
        ),
        "color": (100, 180, 255),
    },

    "tau": {
        "name": "Tau",
        "type": "Lépton",
        "charge": "-1",
        "spin": "1/2",
        "mass": "1776,9 MeV/c²",
        "description": (
            "O tau é uma partícula pertencente à família dos léptons e "
            "interage pelas forças eletromagnética, nuclear fraca e "
            "gravitacional. Foi descoberto por Martin Lewis Perl e "
            "colaboradores em 1974, no acelerador SPEAR. Possui spin 1/2, "
            "carga elétrica -1 e massa de 1776,9 MeV/c², sendo o lépton "
            "de maior massa conhecido. Os taus decaem pela força fraca, "
            "podendo se transformar em píons e neutrinos ou em elétrons, "
            "múons e neutrinos."
        ),
        "color": (255, 120, 180),
    },

    "neutrino_electron": {
        "name": "Neutrino do Elétron",
        "type": "Lépton",
        "charge": "0",
        "spin": "1/2",
        "mass": "< 1 eV/c²",
        "description": (
            "O neutrino do elétron foi proposto por Wolfgang Pauli em 1930 "
            "para resolver a aparente falha na conservação de energia no "
            "decaimento beta do nêutron e foi descoberto em 1956 por Clyde "
            "Cowan e Frederick Reines. Possui spin 1/2, carga elétrica zero "
            "e massa desconhecida, mas muito menor que 1 eV/c². Interage "
            "apenas através das forças nuclear fraca e gravitacional, sendo "
            "por isso muito difícil de detectar. Os neutrinos do elétron, "
            "múon e tau podem se converter uns nos outros durante sua "
            "propagação, fenômeno chamado oscilação de neutrinos."
        ),
        "color": (150, 200, 255),
    },

    "neutrino_muon": {
        "name": "Neutrino do Múon",
        "type": "Lépton",
        "charge": "0",
        "spin": "1/2",
        "mass": "< 1 eV/c²",
        "description": (
            "O neutrino do múon é o tipo de neutrino que é sempre produzido "
            "em associação com um múon. Foi descoberto em 1962 por Leon "
            "Lederman, Melvin Schwartz e Jack Steinberger no Laboratório "
            "Nacional de Brookhaven, nos Estados Unidos. Possui spin 1/2, "
            "carga elétrica zero e massa desconhecida, mas muito menor que "
            "1 eV/c². Interage apenas através das forças nuclear fraca e "
            "gravitacional e pode participar da oscilação de neutrinos."
        ),
        "color": (130, 180, 255),
    },

    "neutrino_tau": {
        "name": "Neutrino do Tau",
        "type": "Lépton",
        "charge": "0",
        "spin": "1/2",
        "mass": "< 1 eV/c²",
        "description": (
            "O neutrino do tau é o tipo de neutrino que é sempre produzido "
            "em associação com um tau. Foi descoberto em 2000 pela "
            "colaboração experimental DONUT, sendo o último lépton a ser "
            "descoberto. Possui spin 1/2, carga elétrica zero e massa "
            "desconhecida, mas muito menor que 1 eV/c². Interage apenas "
            "através das forças nuclear fraca e gravitacional e pode se "
            "converter nos outros tipos de neutrinos durante sua propagação."
        ),
        "color": (180, 150, 255),
    },

    "quark_up": {
        "name": "Quark Up",
        "type": "Quark",
        "charge": "+2/3",
        "spin": "1/2",
        "mass": "2,0 MeV/c²",
        "description": (
            "O quark Up foi um dos três quarks propostos independentemente "
            "em 1964 por Murray Gell-Mann e George Zweig como constituinte "
            "elementar dos hádrons. O próton contém dois quarks Up e um "
            "quark Down, enquanto o nêutron contém dois quarks Down e um "
            "Up. Foi diretamente observado em experimentos de espalhamento "
            "inelástico profundo no Acelerador Linear de Stanford, em 1968. "
            "Possui spin 1/2, carga +2/3 e massa de cerca de 2,0 MeV/c². "
            "Quarks isolados nunca são observados, pois permanecem "
            "confinados no interior dos hádrons."
        ),
        "color": (255, 0, 255),
    },

    "quark_down": {
        "name": "Quark Down",
        "type": "Quark",
        "charge": "-1/3",
        "spin": "1/2",
        "mass": "4,7 MeV/c²",
        "description": (
            "O quark Down foi um dos três quarks propostos independentemente "
            "em 1964 por Murray Gell-Mann e George Zweig como constituinte "
            "elementar dos hádrons. O próton contém dois quarks Up e um "
            "quark Down, enquanto o nêutron contém dois quarks Down e um "
            "Up. Foi diretamente observado em experimentos de espalhamento "
            "inelástico profundo no Acelerador Linear de Stanford, em 1968. "
            "Possui spin 1/2, carga -1/3 e massa de cerca de 4,7 MeV/c². "
            "Quarks isolados nunca são observados, pois permanecem "
            "confinados no interior dos hádrons."
        ),
        "color": (255, 255, 0),
    },

    "quark_charm": {
        "name": "Quark Charm",
        "type": "Quark",
        "charge": "+2/3",
        "spin": "1/2",
        "mass": "1,27 GeV/c²",
        "description": (
            "O quark Charm, ou Charme, é um quark de segunda geração, assim "
            "como o Strange. Sua existência foi postulada por Sheldon "
            "Glashow, John Iliopoulos e Luciano Maiani em 1970 para resolver "
            "problemas na teoria da força nuclear fraca. Foi descoberto em "
            "1974, independentemente no Laboratório Nacional de Brookhaven "
            "e no Acelerador Linear de Stanford, como constituinte do méson "
            "J/Psi. Possui spin 1/2, carga +2/3 e massa de cerca de "
            "1,27 GeV/c². Interage pelas quatro forças fundamentais, "
            "especialmente pela força nuclear forte."
        ),
        "color": (255, 100, 255),
    },

    "quark_strange": {
        "name": "Quark Strange",
        "type": "Quark",
        "charge": "-1/3",
        "spin": "1/2",
        "mass": "95 MeV/c²",
        "description": (
            "O quark Strange, ou Estranho, faz parte da segunda geração de "
            "quarks junto com o Charm. Foi um dos três quarks propostos "
            "independentemente em 1964 por Murray Gell-Mann e George Zweig. "
            "Alguns hádrons apresentavam uma vida média muito maior que a "
            "esperada, fenômeno associado à propriedade chamada estranheza. "
            "O quark Strange possui spin 1/2, carga -1/3 e massa de cerca "
            "de 95 MeV/c². Interage pelas quatro forças fundamentais, "
            "especialmente pela força nuclear forte."
        ),
        "color": (255, 180, 0),
    },

    "quark_bottom": {
        "name": "Quark Bottom",
        "type": "Quark",
        "charge": "-1/3",
        "spin": "1/2",
        "mass": "4,65 GeV/c²",
        "description": (
            "O quark Bottom foi o primeiro quark descoberto da terceira "
            "geração. Sua existência foi postulada em 1973 por Makoto "
            "Kobayashi e Toshihide Maskawa como parte do mecanismo necessário "
            "para explicar a violação da simetria CP. Foi descoberto em 1977 "
            "pelo experimento E288 no Fermilab, como constituinte do méson "
            "Upsilon. Possui spin 1/2, carga -1/3 e massa de cerca de "
            "4,65 GeV/c². Interage pelas quatro forças fundamentais, "
            "especialmente pela força nuclear forte."
        ),
        "color": (180, 100, 50),
    },

    "quark_top": {
        "name": "Quark Top",
        "type": "Quark",
        "charge": "+2/3",
        "spin": "1/2",
        "mass": "172,76 GeV/c²",
        "description": (
            "O quark Top pertence à terceira geração, juntamente com o "
            "Bottom, e foi o último quark a ser descoberto, em 1995, no "
            "acelerador Tevatron do Fermilab. Sua existência era esperada "
            "desde a descoberta do Bottom, devido à organização dos quarks "
            "em gerações. Possui spin 1/2, carga +2/3 e massa de cerca de "
            "172,76 GeV/c². Como os outros quarks, interage pelas quatro "
            "forças fundamentais, especialmente pela força nuclear forte. "
            "Decai rapidamente, antes de formar um hádron."
        ),
        "color": (255, 80, 80),
    },

    "foton": {
        "name": "Fóton",
        "type": "Bóson",
        "charge": "0",
        "spin": "1",
        "mass": "0",
        "description": (
            "O fóton é a partícula mediadora da força eletromagnética, "
            "responsável pela atração e repulsão elétrica e magnética entre "
            "partículas com carga. Os fótons também são responsáveis por "
            "todo o espectro da radiação eletromagnética, incluindo ondas "
            "de rádio, infravermelho, luz visível, ultravioleta, raios X e "
            "raios gama. A ideia de descrever a luz como partícula foi "
            "desenvolvida por Planck, Einstein, Compton e outros no início "
            "do século XX. Fótons são partículas estáveis, possuem spin 1 "
            "e massa zero."
        ),
        "color": (255, 215, 0),
    },

    "boson_w": {
        "name": "Bóson W",
        "type": "Bóson",
        "charge": "+1 / -1",
        "spin": "1",
        "mass": "80,4 GeV/c²",
        "description": (
            "O bóson W é um dos mediadores da força nuclear fraca, juntamente "
            "com o bóson Z. Foi teorizado em 1968 por Sheldon Glashow, Abdus "
            "Salam e Steven Weinberg como parte da teoria eletrofraca e foi "
            "descoberto nos experimentos UA1 e UA2 no CERN, em 1983. A "
            "interação mediada pelo bóson W pode alterar o sabor das "
            "partículas, transformando quarks de carga +2/3 em quarks de "
            "carga -1/3 e léptons carregados em seus neutrinos associados. "
            "Possui carga elétrica +1 ou -1, spin 1 e massa de 80,4 GeV/c²."
        ),
        "color": (100, 255, 100),
    },

    "boson_z": {
        "name": "Bóson Z",
        "type": "Bóson",
        "charge": "0",
        "spin": "1",
        "mass": "91,2 GeV/c²",
        "description": (
            "O bóson Z é um dos mediadores da força nuclear fraca, juntamente "
            "com o bóson W. Foi teorizado em 1968 por Sheldon Glashow, Abdus "
            "Salam e Steven Weinberg como parte da teoria eletrofraca e sua "
            "descoberta ocorreu nos experimentos UA1 e UA2 no CERN, em 1983. "
            "Sua interação é semelhante à do fóton, porém possui alcance "
            "curto e também atua entre neutrinos. Possui carga elétrica "
            "zero, spin 1 e massa de 91,2 GeV/c²."
        ),
        "color": (100, 150, 255),
    },

    "gluon": {
        "name": "Glúon",
        "type": "Bóson",
        "charge": "0",
        "spin": "1",
        "mass": "0",
        "description": (
            "O glúon pertence à família dos bósons e é a partícula "
            "fundamental mediadora da força nuclear forte, responsável por "
            "manter os quarks unidos dentro dos prótons e nêutrons e também "
            "por manter prótons e nêutrons juntos no núcleo atômico. Sua "
            "existência foi confirmada experimentalmente em 1979 no "
            "acelerador PETRA, na Alemanha. Possui spin 1 e carga de cor, "
            "com três tipos: vermelho, verde e azul, além das anti-cores. "
            "Não existe isoladamente em condições normais devido ao "
            "confinamento de cor."
        ),
        "color": (0, 255, 0),
    },

    "graviton": {
        "name": "Gráviton",
        "type": "Bóson",
        "charge": "0",
        "spin": "2",
        "mass": "0",
        "description": (
            "O gráviton é uma partícula elementar hipotética que, em teorias "
            "de gravidade quântica, atuaria como mediadora da força "
            "gravitacional. Sua existência foi postulada para tentar "
            "adequar a relatividade geral de Einstein à mecânica quântica, "
            "mas ainda não foi detectado experimentalmente. As teorias "
            "preveem que possua spin 2, não tenha carga elétrica nem massa "
            "de repouso e tenha alcance infinito. Sua detecção direta é "
            "considerada um grande desafio devido à interação extremamente "
            "fraca com a matéria."
        ),
        "color": (180, 180, 180),
    },

    "higgs": {
        "name": "Bóson de Higgs",
        "type": "Bóson",
        "charge": "0",
        "spin": "0",
        "mass": "125 GeV/c²",
        "description": (
            "O bóson de Higgs é uma partícula fundamental que pertence à "
            "família dos bósons escalares e é a excitação quântica do campo "
            "de Higgs, mecanismo responsável por conferir massa a outras "
            "partículas elementares, como elétrons e quarks. Foi proposto "
            "teoricamente em 1964 por Peter Higgs, François Englert e outros "
            "físicos. Sua descoberta foi anunciada em 4 de julho de 2012 "
            "pelos experimentos ATLAS e CMS no Grande Colisor de Hádrons "
            "(LHC) do CERN. Possui spin 0, não tem carga elétrica e massa "
            "de aproximadamente 125 GeV/c². É muito instável e decai quase "
            "instantaneamente."
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
