"""
Copyright Path Nirvana 2018
Converted from JavaScript to Python

The code and character mapping defined in this file can not be used
for any commercial purposes.
Permission from the author is required for all other purposes.
"""

import re

# https://en.wikipedia.org/wiki/ISO_15924
class Script:
    SI   = "Sinh"
    HI   = "Deva"
    RO   = "Latn"
    THAI = "Thai"
    LAOS = "Laoo"
    MY   = "Mymr"
    KM   = "Khmr"
    BENG = "Beng"
    GURM = "Guru"
    THAM = "Lana"
    GUJA = "Gujr"
    TELU = "Telu"
    KANN = "Knda"
    MALA = "Mlym"
    BRAH = "Brah"
    TIBT = "Tibt"
    CYRL = "Cyrl"


# Locale TLAs from ISO 639-2
PaliScriptInfo = {
    Script.SI: [
        "Sinhala", "සිංහල",
        [(0x0D80, 0x0DFF)],
        {"f": "sl_flag.png", "locale": "si", "localeName": "සිංහල"},
    ],
    Script.HI: [
        "Devanagari", "नागरी",
        [(0x0900, 0x097F)],
        {"f": "in_flag.png", "locale": "hi", "localeName": "हिन्दी"},
    ],
    Script.RO: [
        "Roman", "Roman",
        [(0x0000, 0x017F), (0x1E00, 0x1EFF)],
        {"f": "uk_flag.png", "locale": "en", "localeName": "English"},
    ],
    Script.THAI: [
        "Thai", "ไทย",
        [(0x0E00, 0x0E7F), 0xF70F, 0xF700],
        {"f": "th_flag.png", "locale": "th", "localeName": "ไทย"},
    ],
}


def get_script_for_code(char_code):
    for script, info in PaliScriptInfo.items():
        for rng in info[2]:
            if isinstance(rng, tuple):
                if rng[0] <= char_code <= rng[1]:
                    return script
            elif isinstance(rng, int):
                if char_code == rng:
                    return script
    return -1


ScriptIndex = {
    Script.SI:   0,
    Script.HI:   1,
    Script.RO:   2,
    Script.THAI: 3,
    Script.LAOS: 4,
    Script.MY:   5,
    Script.KM:   6,
    Script.BENG: 7,
    Script.GURM: 8,
    Script.THAM: 9,
    Script.GUJA: 10,
    Script.TELU: 11,
    Script.KANN: 12,
    Script.MALA: 13,
    Script.BRAH: 14,
    Script.TIBT: 15,
    Script.CYRL: 16,
}

# Each row: [SI, HI, RO, THAI, LAOS, MY, KM, BENG, GURM, THAM, GUJA, TELU, KANN, MALA, BRAH, TIBT, CYRL]
specials = [
    ['අ',  'अ',  'a',  'อ',   'ອ',   'အ',  'អ',  'অ',  'ਅ',  'ᩋ',  'અ',  'అ',  'ಅ',  'അ',  '𑀅',  'ཨ',  'а'],
    ['ආ',  'आ',  'ā',  'อา',  'ອາ',  'အာ', 'អា', 'আ',  'ਆ',  'ᩋᩣ', 'આ',  'ఆ',  'ಆ',  'ആ',  '𑀆',  'ཨཱ', 'а̄'],
    ['ඉ',  'इ',  'i',  'อิ',  'ອິ',  'ဣ',  'ឥ',  'ই',  'ਇ',  'ᩍ',  'ઇ',  'ఇ',  'ಇ',  'ഇ',  '𑀇',  'ཨི', 'и'],
    ['ඊ',  'ई',  'ī',  'อี',  'ອີ',  'ဤ',  'ឦ',  'ঈ',  'ਈ',  'ᩎ',  'ઈ',  'ఈ',  'ಈ',  'ഈ',  '𑀈',  'ཨཱི','ӣ'],
    ['උ',  'उ',  'u',  'อุ',  'ອຸ',  'ဥ',  'ឧ',  'উ',  'ਉ',  'ᩩ',  'ઉ',  'ఉ',  'ಉ',  'ഉ',  '𑀉',  'ཨུ', 'у'],
    ['ඌ',  'ऊ',  'ū',  'อู',  'ອູ',  'ဦ',  'ឩ',  'ঊ',  'ਊ',  'ᩪ',  'ઊ',  'ఊ',  'ಊ',  'ഊ',  '𑀊',  'ཨཱུ','ӯ'],
    ['එ',  'ए',  'e',  'อเ',  'ອເ',  'အေ', 'អេ', 'এ',  'ਏ',  'ᩐ',  'એ',  'ఏ',  'ಏ',  'ഏ',  '𑀏',  'ཨེ', 'е'],
    ['ඔ',  'ओ',  'o',  'อโ',  'ອໂ',  'အော','អោ', 'ও',  'ਓ',  'ᩄ',  'ઓ',  'ఓ',  'ಓ',  'ഓ',  '𑀑',  'ཨོ', 'о'],
    ['ං',  'ं',  'ṃ',  '\u0E4D','\u0ECD','\u1036','\u17C6','ং','ਂ','ᩴ', 'ં',  'ం',  'ಂ',  'ം',  '𑀁',  '\u0F7E','м'],
    ['ඃ',  'ः',  'ḥ',  'ะ',   '\u0EBB','\u1038','\u17C7','ঃ','ਃ','ᩡ', 'ઃ',  'ః',  'ಃ',  'ഃ',  '𑀂',  '\u0F7F','х'],
    ['්',  '्',  '',   '\u0E3A','\u0EBA','\u1039','\u17D2','্','੍','᪙', '્',  '్',  '್',  '്',  '𑁆',  '\u0F84',''],
]

consos = [
    ['ක',  'क',  'k',   'ก',   'ກ',   'က',  'ក',  'ক',  'ਕ',  'ᨠ',  'ક',  'క',  'ಕ',  'ക',  '𑀓',  'ཀ',  'к'],
    ['ඛ',  'ख',  'kh',  'ข',   'ຂ',   'ခ',  'ខ',  'খ',  'ਖ',  'ᨡ',  'ખ',  'ఖ',  'ಖ',  'ഖ',  '𑀔',  'ཁ',  'кх'],
    ['ග',  'ग',  'g',   'ค',   'ຄ',   'ဂ',  'គ',  'গ',  'ਗ',  'ᨣ',  'ગ',  'గ',  'ಗ',  'ഗ',  '𑀕',  'ག',  'г'],
    ['ඝ',  'घ',  'gh',  'ฆ',   'ຆ',   'ဃ',  'ឃ',  'ঘ',  'ਘ',  'ᨤ',  'ઘ',  'ఘ',  'ಘ',  'ഘ',  '𑀖',  'གྷ', 'гх'],
    ['ඞ',  'ङ',  'ṅ',   'ง',   'ງ',   'င',  'ង',  'ঙ',  'ਙ',  'ᨦ',  'ઙ',  'ఙ',  'ಙ',  'ങ',  '𑀗',  'ང',  'нг'],
    ['ච',  'च',  'c',   'จ',   'ຈ',   'စ',  'ច',  'চ',  'ਚ',  'ᨧ',  'ચ',  'చ',  'ಚ',  'ച',  '𑀘',  'ཅ',  'ч'],
    ['ඡ',  'छ',  'ch',  'ฉ',   'ຉ',   'ဆ',  'ឆ',  'ছ',  'ਛ',  'ᨨ',  'છ',  'ఛ',  'ಛ',  'ഛ',  '𑀙',  'ཆ',  'чх'],
    ['ජ',  'ज',  'j',   'ช',   'ຊ',   'ဇ',  'ជ',  'জ',  'ਜ',  'ᨩ',  'જ',  'జ',  'ಜ',  'ജ',  '𑀚',  'ཇ',  'дж'],
    ['ඣ',  'झ',  'jh',  'ฌ',   'ຌ',   'ဈ',  'ឈ',  'ঝ',  'ਝ',  'ᨪ',  'ઝ',  'ఝ',  'ಝ',  'ഝ',  '𑀛',  'ཞ',  'джх'],
    ['ඤ',  'ञ',  'ñ',   'ญ',   'ຍ',   'ဉ',  'ញ',  'ঞ',  'ਞ',  'ᨫ',  'ઞ',  'ఞ',  'ಞ',  'ഞ',  '𑀜',  'ཉ',  'нь'],
    ['ට',  'ट',  'ṭ',   'ฏ',   'ຏ',   'ဋ',  'ដ',  'ট',  'ਟ',  'ᨭ',  'ટ',  'ట',  'ಟ',  'ട',  '𑀝',  'ཊ',  'т̣'],
    ['ඨ',  'ठ',  'ṭh',  'ฐ',   'ຐ',   'ဌ',  'ឋ',  'ঠ',  'ਠ',  'ᨮ',  'ઠ',  'ఠ',  'ಠ',  'ഠ',  '𑀞',  'ཋ',  'т̣х'],
    ['ඩ',  'ड',  'ḍ',   'ด',   'ດ',   'ဍ',  'ឌ',  'ড',  'ਡ',  'ᨯ',  'ડ',  'డ',  'ಡ',  'ഡ',  '𑀟',  'ཌ',  'д̣'],
    ['ඪ',  'ढ',  'ḍh',  'ฒ',   'ຒ',   'ဎ',  'ឍ',  'ঢ',  'ਢ',  'ᨰ',  'ઢ',  'ఢ',  'ಢ',  'ഢ',  '𑀠',  'ཌྷ', 'д̣х'],
    ['ණ',  'ण',  'ṇ',   'ณ',   'ນ',   'ဏ',  'ណ',  'ণ',  'ਣ',  'ᨱ',  'ણ',  'ణ',  'ಣ',  'ണ',  '𑀡',  'ཎ',  'н̣'],
    ['ත',  'त',  't',   'ต',   'ຕ',   'တ',  'ត',  'ত',  'ਤ',  'ᨲ',  'ત',  'త',  'ತ',  'ത',  '𑀢',  'ཏ',  'т'],
    ['ථ',  'थ',  'th',  'ถ',   'ຖ',   'ထ',  'ថ',  'থ',  'ਥ',  'ᨳ',  'થ',  'థ',  'ಥ',  'ഥ',  '𑀣',  'ཐ',  'тх'],
    ['ද',  'द',  'd',   'ท',   'ທ',   'ဒ',  'ទ',  'দ',  'ਦ',  'ᨴ',  'દ',  'ద',  'ದ',  'ദ',  '𑀤',  'ད',  'д'],
    ['ධ',  'ध',  'dh',  'ธ',   'ຘ',   'ဓ',  'ធ',  'ধ',  'ਧ',  'ᨵ',  'ધ',  'ధ',  'ಧ',  'ധ',  '𑀥',  'དྷ', 'дх'],
    ['න',  'न',  'n',   'น',   'ນ',   'န',  'ន',  'ন',  'ਨ',  'ᨶ',  'ન',  'న',  'ನ',  'ന',  '𑀦',  'ན',  'н'],
    ['ප',  'प',  'p',   'ป',   'ປ',   'ပ',  'ប',  'প',  'ਪ',  'ᨸ',  'પ',  'ప',  'ಪ',  'പ',  '𑀧',  'པ',  'п'],
    ['ඵ',  'फ',  'ph',  'ผ',   'ຜ',   'ဖ',  'ផ',  'ফ',  'ਫ',  'ᨹ',  'ફ',  'ఫ',  'ಫ',  'ഫ',  '𑀨',  'ཕ',  'пх'],
    ['බ',  'ब',  'b',   'พ',   'ພ',   'ဗ',  'ប',  'ব',  'ਬ',  'ᨻ',  'બ',  'బ',  'ಬ',  'ബ',  '𑀩',  'བ',  'б'],
    ['භ',  'भ',  'bh',  'ภ',   'ຠ',   'ဘ',  'ភ',  'ভ',  'ਭ',  'ᨼ',  'ભ',  'భ',  'ಭ',  'ഭ',  '𑀪',  'བྷ', 'бх'],
    ['ම',  'म',  'm',   'ม',   'ມ',   'မ',  'ម',  'ম',  'ਮ',  'ᨾ',  'મ',  'మ',  'ಮ',  'മ',  '𑀫',  'མ',  'м'],
    ['ය',  'य',  'y',   'ย',   'ຢ',   'ယ',  'យ',  'য',  'ਯ',  'ᩀ',  'ય',  'య',  'ಯ',  'യ',  '𑀬',  'ཡ',  'й'],
    ['ර',  'र',  'r',   'ร',   'ຣ',   'ရ',  'រ',  'র',  'ਰ',  'ᩁ',  'ર',  'ర',  'ರ',  'ര',  '𑀭',  'ར',  'р'],
    ['ල',  'ल',  'l',   'ล',   'ລ',   'လ',  'ល',  'ল',  'ਲ',  'ᩃ',  'લ',  'ల',  'ಲ',  'ല',  '𑀮',  'ལ',  'л'],
    ['ව',  'व',  'v',   'ว',   'ວ',   'ဝ',  'វ',  'ব',  'ਵ',  'ᩅ',  'વ',  'వ',  'ವ',  'വ',  '𑀯',  'ཝ',  'в'],
    ['ස',  'स',  's',   'ส',   'ສ',   'သ',  'ស',  'স',  'ਸ',  'ᩈ',  'સ',  'స',  'ಸ',  'സ',  '𑀱',  'ས',  'с'],
    ['හ',  'ह',  'h',   'ห',   'ຫ',   'ဟ',  'ហ',  'হ',  'ਹ',  'ᩉ',  'હ',  'హ',  'ಹ',  'ഹ',  '𑀳',  'ཧ',  'х'],
    ['ළ',  'ळ',  'ḷ',   'ฬ',   'ຬ',   'ဠ',  'ឡ',  'ল়', 'ਲ਼', 'ᩃ',  'ળ',  'ళ',  'ಳ',  'ള',  '𑀴',  'ལ',  'л̣'],
]

vowels = [
    ['ා',  'ा',  'ā',  'า',   'າ',   'ာ',  'ា',  'া',  'ਾ',  'ᩣ',  'ા',  'ా',  'ಾ',  'ാ',  '𑀸',  'ཱ',  'а̄'],
    ['ි',  'ि',  'i',  '\u0E34','\u0EB4','\u102D','\u17B7','ি','ਿ','ᩥ','િ', 'ి',  'ಿ',  'ി',  '𑀺',  'ི',  'и'],
    ['ී',  'ी',  'ī',  '\u0E35','\u0EB5','\u102E','\u17B8','ী','ੀ','ᩦ','ી', 'ీ',  'ೀ',  'ീ',  '𑀻',  'ཱི', 'ӣ'],
    ['ු',  'ु',  'u',  '\u0E38','\u0EB8','\u102F','\u17BB','ু','ੁ','ᩩ','ુ', 'ు',  'ು',  'ു',  '𑀼',  'ུ',  'у'],
    ['ූ',  'ू',  'ū',  '\u0E39','\u0EB9','\u1030','\u17BC','ূ','ੂ','ᩪ','ૂ', 'ూ',  'ೂ',  'ൂ',  '𑀽',  'ཱུ', 'ӯ'],
    ['ෙ',  'े',  'e',  'เ',   'ເ',   'ေ',  '\u17C1','ে', 'ੇ',  'ᩮ', 'ે',  'ే',  'ೇ',  'േ',  '𑁂',  'ེ',  'е'],
    ['ො',  'ो',  'o',  'โ',   'ໂ',   'ော', '\u17C4','ো', 'ੋ',  'ᩰ', 'ો',  'ో',  'ೋ',  'ോ',  '𑁄',  'ོ',  'о'],
]


# ── Conversion helpers ────────────────────────────────────

def prepare_hash_maps(from_index, to_index, use_vowels=True):
    full_ar = consos + specials + (vowels if use_vowels else [])
    buckets = [{}, {}, {}]  # index = char_length - 1 (0,1,2 → len 1,2,3)

    for row in full_ar:
        if from_index >= len(row) or to_index >= len(row):
            continue
        key = row[from_index]
        val = row[to_index]
        if key:
            bucket_idx = min(len(key) - 1, 2)
            buckets[bucket_idx][key] = val

    # return sorted longest-first so longer keys match before shorter
    result = []
    for i in range(2, -1, -1):
        if buckets[i]:
            result.append((i + 1, buckets[i]))
    return result


def replace_by_maps(input_text, hash_maps):
    output = []
    b = 0
    while b < len(input_text):
        matched = False
        for length, hmap in hash_maps:
            chunk = input_text[b:b + length]
            if chunk in hmap:
                output.append(hmap[chunk])
                b += length
                matched = True
                break
        if not matched:
            output.append(input_text[b])
            b += 1
    return ''.join(output)


def convert_to(text, script):
    hm = prepare_hash_maps(ScriptIndex[Script.SI], ScriptIndex[script])
    return replace_by_maps(text, hm)


def convert_from(text, script):
    hm = prepare_hash_maps(ScriptIndex[script], ScriptIndex[Script.SI])
    return replace_by_maps(text, hm)


# ── Script-specific transforms ────────────────────────────

def insert_a(text, script=None):
    a = 'а' if script == Script.CYRL else 'a'
    text = re.sub(fr'([ක-ෆ])([^\u0DCF-\u0DDF\u0DCA{a}])', fr'\1{a}\2', text)
    text = re.sub(fr'([ක-ෆ])$', fr'\1{a}', text)
    return text


IV_TO_DV = {
    'අ': '', 'ආ': 'ා', 'ඉ': 'ි', 'ඊ': 'ී',
    'උ': 'ු', 'ඌ': 'ූ', 'එ': 'ෙ', 'ඔ': 'ො',
}


# def remove_a(text, _script=None):
#     text = re.sub(r'([ක-ෆ])([^අආඉඊඋඌඑඔ\u0DCA])', r'\1\u0DCA\2', text)
#     text = re.sub(r'([ක-ෆ])$', r'\1\u0DCA', text)

#     def repl(m):
#         return m.group(1) + IV_TO_DV[m.group(2)]

#     text = re.sub(r'([ක-ෆ])([අආඉඊඋඌඑඔ])', repl, text)
#     return text
def remove_a(text, _script=None):

    # Add hal kirima (්) after consonants
    text = re.sub(
        r'([ක-ෆ])([^අආඉඊඋඌඑඔ්])',
        r'\1' + '්' + r'\2',
        text
    )

    # Add hal kirima at end
    text = re.sub(
        r'([ක-ෆ])$',
        r'\1' + '්',
        text
    )

    # Replace independent vowels with dependent vowels
    def repl(m):
        return m.group(1) + IV_TO_DV[m.group(2)]

    text = re.sub(
        r'([ක-ෆ])([අආඉඊඋඌඑඔ])',
        repl,
        text
    )

    return text

def fix_m_above(text, script=None):
    return text.replace('ṁ', 'ං')


def beautify_sinh(text, _script=None, _rend_type=''):
    return re.sub(r'\u0DCA([\u0DBA\u0DBB])', r'\u0DCA\u200D\1', text)


def un_beautify_sinh(text):
    text = text.replace('ඒ', 'එ').replace('ඕ', 'ඔ')
    return text.replace('ේ', 'ෙ').replace('ෝ', 'ො')


def beautify_common(text, _script=None, rend_type=''):
    if rend_type == 'cen':
        text = text.replace('॥', '')
    elif rend_type.startswith('ga'):
        text = text.replace('।', ';').replace('॥', '.')
    text = text.replace('॰…', '…').replace('॰', '·')
    text = re.sub(r'[।॥]', '.', text)
    text = re.sub(r'\s([\s,!;\?.])', r'\1', text)
    return text


def cleanup_zwj(text):
    return re.sub(r'[\u200C\u200D]', '', text)


# ── Dispatch tables ───────────────────────────────────────

convert_to_func = {
    Script.RO:   [insert_a, convert_to],
    Script.CYRL: [insert_a, convert_to],
}

convert_from_func = {
    Script.RO:   [convert_from, fix_m_above, remove_a],
    Script.CYRL: [convert_from, remove_a],
}

beautify_func = {
    Script.SI: [beautify_sinh, beautify_common],
    Script.RO: [beautify_common],
}

un_beautify_func = {
    Script.SI: [cleanup_zwj, un_beautify_sinh],
    Script.HI: [cleanup_zwj],
}


# ── TextProcessor ─────────────────────────────────────────

class TextProcessor:

    @staticmethod
    def basic_convert_from_sinh(input_text, script):
        text = input_text
        for func in convert_to_func.get(script, [convert_to]):
            text = func(text, script)
        return text

    @staticmethod
    def basic_convert_to_sinh(input_text, script):

        text = input_text
        
        # Fix Roman uppercase input
        if script == Script.RO:
            text = text.lower()

        for func in convert_from_func.get(script, [convert_from]):
            text = func(text, script)

        return text

    @staticmethod
    def beautify(input_text, script, rend_type=''):
        text = input_text
        for func in beautify_func.get(script, []):
            text = func(text, script, rend_type)
        return text

    @staticmethod
    def convert_from_sinh(input_text, script):
        text = TextProcessor.basic_convert_from_sinh(input_text, script)
        return TextProcessor.beautify(text, script)

    @staticmethod
    def convert_to_sinh(input_text, script):
        text = input_text
        for func in un_beautify_func.get(script, []):
            try:
                text = func(text, script)
            except TypeError:
                text = func(text)
        return TextProcessor.basic_convert_to_sinh(text, script)

    @staticmethod
    def convert_any_to_sinh(input_text):
        mixed_text = cleanup_zwj(input_text) + ' '
        cur_script = -1
        run = ''
        output = ''
        for ch in mixed_text:
            new_script = get_script_for_code(ord(ch))
            if new_script != cur_script:
                output += TextProcessor.convert_to_sinh(run, cur_script)
                cur_script = new_script
                run = ch
            else:
                run += ch
        return output


# ── Script metadata for the API ───────────────────────────

SCRIPT_LIST = [
    {"key": Script.SI,   "name": "Sinhala",    "native": "සිංහල",     "iso": "Sinh"},
    {"key": Script.HI,   "name": "Devanagari", "native": "नागरी",     "iso": "Deva"},
    {"key": Script.RO,   "name": "Roman",      "native": "Roman",      "iso": "Latn"},
    {"key": Script.THAI, "name": "Thai",        "native": "ไทย",        "iso": "Thai"},
    {"key": Script.LAOS, "name": "Lao",         "native": "ລາວ",        "iso": "Laoo"},
    {"key": Script.MY,   "name": "Myanmar",     "native": "မြန်မာ",    "iso": "Mymr"},
    {"key": Script.KM,   "name": "Khmer",       "native": "ខ្មែរ",     "iso": "Khmr"},
    {"key": Script.BENG, "name": "Bengali",     "native": "বাংলা",     "iso": "Beng"},
    {"key": Script.GURM, "name": "Gurmukhi",    "native": "ਗੁਰਮੁਖੀ", "iso": "Guru"},
    {"key": Script.TELU, "name": "Telugu",      "native": "తెలుగు",    "iso": "Telu"},
    {"key": Script.KANN, "name": "Kannada",     "native": "ಕನ್ನಡ",    "iso": "Knda"},
    {"key": Script.MALA, "name": "Malayalam",   "native": "മലയാളം",   "iso": "Mlym"},
    {"key": Script.TIBT, "name": "Tibetan",     "native": "བོད་སྐད།",  "iso": "Tibt"},
    {"key": Script.CYRL, "name": "Cyrillic",    "native": "Кириллица", "iso": "Cyrl"},
]


if __name__ == "__main__":
    sinh_text = "කරුණා"
    print("Sinhala:", sinh_text)
    for s in SCRIPT_LIST:
        key = s["key"]
        if key == Script.SI:
            continue
        result = TextProcessor.convert_from_sinh(sinh_text, key)
        print(f"  {s['name']:15} {result}")