# from flask import Flask, render_template, request, jsonify
# from pali_script import TextProcessor, SCRIPT_LIST

# app = Flask(__name__)


# # Home Page
# @app.route("/", methods=["GET"])
# def home():
#     return render_template("index.html", scripts=SCRIPT_LIST)


# # Convert API
# @app.route("/convert", methods=["POST"])
# def convert():

#     data = request.get_json()

#     if not data:
#         return jsonify({
#             "success": False,
#             "error": "No JSON data received"
#         })

#     text = data.get("text", "")
#     from_script = data.get("from_script")
#     to_script = data.get("to_script")

#     try:

#         # Sinhala → Other
#         if from_script == "Sinh":
#             result = TextProcessor.convert_from_sinh(
#                 text,
#                 to_script
#             )

#         # Other → Sinhala
#         elif to_script == "Sinh":
#             result = TextProcessor.convert_to_sinh(
#                 text,
#                 from_script
#             )

#         # Other → Other
#         else:
#             sinh = TextProcessor.convert_to_sinh(
#                 text,
#                 from_script
#             )

#             result = TextProcessor.convert_from_sinh(
#                 sinh,
#                 to_script
#             )

#         return jsonify({
#             "success": True,
#             "result": result
#         })

#     except Exception as e:

#         return jsonify({
#             "success": False,
#             "error": str(e)
#         })

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)

from flask import Flask, render_template, request, jsonify
from devanagari_brahmi import TextProcessor

app = Flask(__name__)


SCRIPT_LIST = [
    {"key": "Deva", "name": "Devanagari"},
    {"key": "Brah", "name": "Brahmi"}
]


@app.route("/")
def home():
    return render_template(
        "index.html",
        scripts=SCRIPT_LIST
    )


@app.route("/convert", methods=["POST"])
def convert():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "No data received"
        })

    text = data.get("text", "")
    from_script = data.get("from_script")
    to_script = data.get("to_script")

    try:

        # Devanagari → Brahmi
        if from_script == "Deva" and to_script == "Brah":

            result = TextProcessor.devanagari_to_brahmi(text)

        # Brahmi → Devanagari
        elif from_script == "Brah" and to_script == "Deva":

            result = TextProcessor.brahmi_to_devanagari(text)

        else:

            result = text

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

# if __name__ == "__main__":
#     app.run(debug=True)