# devanagari_brahmi.py

class Script:
    HI = "Deva"   # Devanagari
    BRAH = "Brah" # Brahmi


ScriptIndex = {
    Script.HI: 0,
    Script.BRAH: 1,
}

# [Devanagari, Brahmi]
chars = [
    ['अ', '𑀅'],
    ['आ', '𑀆'],
    ['इ', '𑀇'],
    ['ई', '𑀈'],
    ['उ', '𑀉'],
    ['ऊ', '𑀊'],
    ['ए', '𑀏'],
    ['ओ', '𑀑'],

    ['क', '𑀓'],
    ['ख', '𑀔'],
    ['ग', '𑀕'],
    ['घ', '𑀖'],
    ['ङ', '𑀗'],

    ['च', '𑀘'],
    ['छ', '𑀙'],
    ['ज', '𑀚'],
    ['झ', '𑀛'],
    ['ञ', '𑀜'],

    ['ट', '𑀝'],
    ['ठ', '𑀞'],
    ['ड', '𑀟'],
    ['ढ', '𑀠'],
    ['ण', '𑀡'],

    ['त', '𑀢'],
    ['थ', '𑀣'],
    ['द', '𑀤'],
    ['ध', '𑀥'],
    ['न', '𑀦'],

    ['प', '𑀧'],
    ['फ', '𑀨'],
    ['ब', '𑀩'],
    ['भ', '𑀪'],
    ['म', '𑀫'],

    ['य', '𑀬'],
    ['र', '𑀭'],
    ['ल', '𑀮'],
    ['व', '𑀯'],

    ['श', '𑀰'],
    ['ष', '𑀱'],
    ['स', '𑀲'],
    # ['स', '𑀲𑀁']
    ['ह', '𑀳'],

    ['ळ', '𑀴'],

    ['ं', '𑀁'],
    ['ः', '𑀂'],
    ['्', '𑁆'],

    ['ा', '𑀸'],
    ['ि', '𑀺'],
    ['ी', '𑀻'],
    ['ु', '𑀼'],
    ['ू', '𑀽'],
    ['े', '𑁂'],
    ['ो', '𑁄'],
]


def prepare_hash_map(from_index, to_index):
    mapping = {}
    for row in chars:
        mapping[row[from_index]] = row[to_index]
    return mapping


def replace_text(text, mapping):
    result = ""
    for ch in text:
        result += mapping.get(ch, ch)
    return result

def devanagari_preprocess(text):
    specials = {
        "श्री": "𑀰𑁆𑀭𑀻",
        "क्ष": "𑀓𑁆𑀱",
        "त्र": "𑀢𑁆𑀭",
        "ज्ञ": "𑀚𑁆𑀜",
    }

    for k, v in specials.items():
        text = text.replace(k, v)

    return text

def brahmi_preprocess(text):
    specials = {
        "𑀰𑁆𑀭𑀻": "श्री",
        "𑀓𑁆𑀱": "क्ष",
        "𑀢𑁆𑀭": "त्र",
        "𑀚𑁆𑀜": "ज्ञ",
    }

    for k, v in specials.items():
        text = text.replace(k, v)

    return text

class TextProcessor:

    @staticmethod
    def devanagari_to_brahmi(text):

        text = devanagari_preprocess(text)

        mapping = prepare_hash_map(
            ScriptIndex[Script.HI],
            ScriptIndex[Script.BRAH]
        )

        return replace_text(text, mapping)

    @staticmethod
    def brahmi_to_devanagari(text):

        text = brahmi_preprocess(text)

        mapping = prepare_hash_map(
            ScriptIndex[Script.BRAH],
            ScriptIndex[Script.HI]
        )

        return replace_text(text, mapping)


if __name__ == "__main__":

    dev = "करुणा"
    brah = TextProcessor.devanagari_to_brahmi(dev)

    print("Devanagari :", dev)
    print("Brahmi     :", brah)

    print("Back to Devanagari :")
    print(TextProcessor.brahmi_to_devanagari(brah))