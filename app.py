from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
import json

app = Flask(__name__, static_folder='static')

# Knowledge base built from the problem statement in the image.
KB = {
    "title": {
        "en": "Digitize and Showcase Monasteries of Sikkim for Tourism and Cultural Preservation",
        "hi": "सिटीके मठों का डिजिटलीकरण और प्रदर्शनी (Sikkim) - पर्यटन और सांस्कृतिक संरक्षण"
    },
    "short": {
        "en": "A project to create virtual tours, digital archives, interactive maps and audio guides for monasteries in Sikkim.",
        "hi": "यह परियोजना सिखिम के मठों के लिए वर्चुअल टूर, डिजिटल अभिलेख, इंटरैक्टिव मानचित्र और ऑडियो गाइड बनाती है।"
    },
    "features": {
        "en": [
            "Virtual Tours: 360° panoramic views of monastery interiors and surroundings.",
            "Narrated walkthroughs in multiple languages.",
            "Interactive Map: Geo-tagged monastery locations with travel routes and nearby attractions.",
            "Integration with local transport and tourism services.",
            "Digital Archives: Scanned manuscripts, murals, and historical documents.",
            "AI-powered search and categorization.",
            "Smart Audio Guide App: Location-based audio guides using Bluetooth beacons or GPS.",
            "Offline mode for remote areas.",
            "Cultural Calendar: Events, festivals, and rituals schedule."
        ],
        "hi": [
            "वर्चुअल टूर: मठ के अंदर और आसपास के 360° पैनोरमिक दृश्य।",
            "कई भाषाओं में वर्णित वॉकथ्रू।",
            "इंटरैक्टिव मैप: यात्रा मार्ग और पास के आकर्षणों के साथ जियो-टैग्ड मठ स्थान।",
            "स्थानीय परिवहन और पर्यटन सेवाओं के साथ एकीकरण।",
            "डिजिटल अभिलेख: स्कैन किए गए पांडुलिपियाँ, भित्ति चित्र और ऐतिहासिक दस्तावेज।",
            "एआई-संचालित खोज और वर्गीकरण।",
            "स्मार्ट ऑडियो गाइड ऐप: ब्लूटूथ बीकन या GPS का उपयोग करके स्थान-आधारित ऑडियो गाइड।",
            "दूरस्थ क्षेत्रों के लिए ऑफ़लाइन मोड।",
            "सांस्कृतिक कैलेंडर: कार्यक्रम, त्योहार और अनुष्ठान शेड्यूल।"
        ]
    },
    "org": {
        "en": "Government of Sikkim (Department of Higher & Technical Education)",
        "hi": "सिक्किम सरकार (उच्च एवं तकनीकी शिक्षा विभाग)"
    },
    "category": {"en": "Software", "hi": "सॉफ़्टवेयर"},
    "theme": {"en": "Travel & Tourism", "hi": "यात्रा और पर्यटन"}
}

# Simple rule-based responder using keyword matching
def generate_reply(message, lang="en"):
    msg = message.lower().strip()
    # greetings
    if any(g in msg for g in ["hello", "hi", "namaste", "hey", "हैलो", "नमस्ते"]):
        return {
            "text": {
                "en": "Hello! I can answer questions about the Sikkim Monasteries digitization project. Try: 'features', 'map', 'offline', or ask in Hindi.'",
                "hi": "नमस्ते! मैं सिक्किम मठ डिजिटलीकरण परियोजना के बारे में मदद कर सकता हूँ। कोशिश करें: 'features', 'मैप', 'ऑफलाइन', या हिंदी में पूछें।"
            }[lang]
        }

    # ask for summary/title
    if any(k in msg for k in ["project", "title", "about", "what is", "what's", "परियोजना", "यह क्या", "के बारे में"]):
        return {"text": KB["short"][lang]}

    # features
    if "feature" in msg or "features" in msg or "क्या-क्या" in msg or "फीचर" in msg or "विशेषत" in msg:
        lines = KB["features"][lang]
        return {"text": "\n".join(f"- {l}" for l in lines)}

    # interactive map
    if "map" in msg or "location" in msg or "geo" in msg or "मैप" in msg or "स्थान" in msg:
        answer = {
            "en": "The project includes an interactive map with geo-tagged monastery locations, travel routes, and nearby attractions. It can integrate with transport services.",
            "hi": "परियोजना में जियो-टैग्ड मठ स्थान, यात्रा मार्ग और पास के आकर्षणों वाला इंटरैक्टिव मैप शामिल है। यह परिवहन सेवाओं के साथ जुड़ सकता है।"
        }
        return {"text": answer[lang]}

    # audio guide / offline
    if "audio" in msg or "guide" in msg or "ऑडियो" in msg or "ऑफलाइन" in msg or "offline" in msg:
        answer = {
            "en": "Smart Audio Guide: location-based audio guides using Bluetooth beacons or GPS. Offline mode is supported for remote areas.",
            "hi": "स्मार्ट ऑडियो गाइड: ब्लूटूथ बीकन या GPS के माध्यम से स्थान-आधारित ऑडियो गाइड। दूरस्थ क्षेत्रों के लिए ऑफ़लाइन मोड समर्थन।"
        }
        return {"text": answer[lang]}

    # digital archives / manuscripts
    if "archive" in msg or "manuscript" in msg or "document" in msg or "piał" in msg or "अभिलेख" in msg or "पांडुलिप" in msg:
        answer = {
            "en": "Digital Archives: project will scan manuscripts, murals, and historical documents and include AI-powered search and categorization.",
            "hi": "डिजिटल अभिलेख: परियोजना पांडुलिपियाँ, भित्ति चित्र और ऐतिहासिक दस्तावेज़ स्कैन करेगी तथा एआई-संचालित खोज और वर्गीकरण होगा।"
        }
        return {"text": answer[lang]}

    # organization / category / theme
    if "organization" in msg or "org" in msg or "gov" in msg or "सरकार" in msg or "विभाग" in msg:
        return {"text": KB["org"][lang]}

    # fallback: try keywords from features
    for f in KB["features"][lang]:
        for word in f.lower().split():
            if word and word in msg and len(word) > 4:
                return {"text": f"{f}\n\n(From knowledge base)"}

    # final fallback
    fallback = {
        "en": "Sorry, I didn't understand that. Ask about 'features', 'map', 'audio guide', or type a question about the project.",
        "hi": "माफ़ कीजिये, मैं समझा नहीं। 'features', 'मैप', 'ऑडियो गाइड' के बारे में पूछें या परियोजना से जुड़ा कोई प्रश्न लिखें।"
    }
    return {"text": fallback[lang]}


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    lang = data.get('lang', 'en')
    reply = generate_reply(message, lang=lang)
    return jsonify({
        "reply": reply["text"]
    })


# serve the UI & static files
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
