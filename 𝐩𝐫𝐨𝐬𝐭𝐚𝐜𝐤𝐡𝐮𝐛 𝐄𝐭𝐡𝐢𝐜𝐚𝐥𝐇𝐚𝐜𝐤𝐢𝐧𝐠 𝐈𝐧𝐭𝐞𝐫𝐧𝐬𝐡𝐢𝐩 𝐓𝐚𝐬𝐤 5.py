# ================================================================
#        🛡️ CRYPTOVAULT - URL SECURITY ANALYZER
#                    TASK 5 - PROSTACKHUB
# ================================================================

from flask import Flask, request, render_template_string
from urllib.parse import urlparse
import ipaddress
import re

app = Flask(__name__)

# ================================================================
#                     HTML + CSS DESIGN
# ================================================================

HTML = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>CryptoVault | URL Security Analyzer</title>

    <style>

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: Arial, Helvetica, sans-serif;
        }

        body {
            min-height: 100vh;
            background:
                radial-gradient(circle at top left, #172554, transparent 35%),
                radial-gradient(circle at bottom right, #312e81, transparent 35%),
                #050816;
            color: white;
            padding: 30px 15px;
        }

        .container {
            max-width: 950px;
            margin: auto;
        }

        .header {
            text-align: center;
            padding: 25px;
            margin-bottom: 25px;
        }

        .logo {
            font-size: 55px;
            margin-bottom: 10px;
        }

        .title {
            font-size: 38px;
            font-weight: bold;
            background: linear-gradient(90deg, #60a5fa, #c084fc);
            -webkit-background-clip: text;
            color: transparent;
        }

        .subtitle {
            color: #b8c1d9;
            margin-top: 10px;
            font-size: 16px;
        }

        .card {
            background: rgba(15, 23, 42, 0.88);
            border: 1px solid rgba(148, 163, 184, 0.25);
            border-radius: 22px;
            padding: 30px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.4);
            margin-bottom: 25px;
        }

        label {
            display: block;
            margin-bottom: 10px;
            font-weight: bold;
            color: #e2e8f0;
        }

        .url-box {
            display: flex;
            gap: 10px;
        }

        input {
            flex: 1;
            padding: 16px;
            border-radius: 12px;
            border: 1px solid #475569;
            background: #0f172a;
            color: white;
            outline: none;
            font-size: 15px;
        }

        input:focus {
            border-color: #60a5fa;
            box-shadow: 0 0 12px rgba(96,165,250,.25);
        }

        button {
            padding: 15px 25px;
            border: none;
            border-radius: 12px;
            background: linear-gradient(135deg, #2563eb, #7c3aed);
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: .3s;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(99,102,241,.35);
        }

        .score-card {
            text-align: center;
            padding: 25px;
            border-radius: 18px;
            background: rgba(30,41,59,.8);
            margin-bottom: 20px;
        }

        .score {
            font-size: 65px;
            font-weight: bold;
        }

        .safe {
            color: #22c55e;
        }

        .medium {
            color: #facc15;
        }

        .danger {
            color: #ef4444;
        }

        .status {
            font-size: 20px;
            font-weight: bold;
            margin-top: 5px;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-top: 20px;
        }

        .result {
            padding: 18px;
            border-radius: 14px;
            background: #111827;
            border: 1px solid #334155;
        }

        .result-title {
            color: #94a3b8;
            font-size: 13px;
            margin-bottom: 7px;
        }

        .result-value {
            font-weight: bold;
            font-size: 17px;
        }

        .recommendations {
            margin-top: 20px;
            padding: 20px;
            border-radius: 15px;
            background: rgba(30,41,59,.75);
        }

        .recommendations h3 {
            color: #60a5fa;
            margin-bottom: 12px;
        }

        .recommendations li {
            margin: 9px 0;
            color: #dbeafe;
            list-style: none;
        }

        .recommendations li::before {
            content: "⚠ ";
            color: #facc15;
        }

        .footer {
            text-align: center;
            color: #64748b;
            padding: 20px;
            font-size: 13px;
        }

        .error {
            background: rgba(127,29,29,.3);
            color: #fca5a5;
            padding: 15px;
            border-radius: 12px;
            margin-top: 15px;
        }

        @media(max-width: 650px) {

            .title {
                font-size: 28px;
            }

            .url-box {
                flex-direction: column;
            }

            .grid {
                grid-template-columns: 1fr;
            }

            button {
                width: 100%;
            }
        }

    </style>

</head>

<body>

<div class="container">

    <div class="header">

        <div class="logo">🛡️</div>

        <div class="title">
            CRYPTOVAULT
        </div>

        <div class="subtitle">
            Smart URL Security & Risk Analyzer
        </div>

    </div>


    <div class="card">

        <form method="POST">

            <label>
                🔗 Enter a URL to analyze
            </label>

            <div class="url-box">

                <input
                    type="text"
                    name="url"
                    placeholder="https://example.com"
                    value="{{ url }}"
                    required
                >

                <button type="submit">
                    🔍 Analyze URL
                </button>

            </div>

        </form>

        {% if error %}

            <div class="error">
                ❌ {{ error }}
            </div>

        {% endif %}

    </div>


    {% if result %}

    <div class="card">

        <div class="score-card">

            <div class="score {{ result.color }}">
                {{ result.score }}/100
            </div>

            <div class="status">
                {{ result.status }}
            </div>

        </div>


        <h2>🔎 Security Analysis</h2>


        <div class="grid">

            <div class="result">

                <div class="result-title">
                    HTTPS Protection
                </div>

                <div class="result-value">
                    {{ result.https }}
                </div>

            </div>


            <div class="result">

                <div class="result-title">
                    IP Address Detected
                </div>

                <div class="result-value">
                    {{ result.ip }}
                </div>

            </div>


            <div class="result">

                <div class="result-title">
                    Suspicious Characters
                </div>

                <div class="result-value">
                    {{ result.suspicious }}
                </div>

            </div>


            <div class="result">

                <div class="result-title">
                    URL Length
                </div>

                <div class="result-value">
                    {{ result.length }} characters
                </div>

            </div>


            <div class="result">

                <div class="result-title">
                    Domain
                </div>

                <div class="result-value">
                    {{ result.domain }}
                </div>

            </div>


            <div class="result">

                <div class="result-title">
                    URL Scheme
                </div>

                <div class="result-value">
                    {{ result.scheme }}
                </div>

            </div>

        </div>


        <div class="recommendations">

            <h3>💡 Security Recommendations</h3>

            <ul>

                {% for recommendation in result.recommendations %}

                    <li>{{ recommendation }}</li>

                {% endfor %}

            </ul>

        </div>

    </div>

    {% endif %}


    <div class="footer">

        🔐 CryptoVault URL Security Analyzer
        <br><br>
        MADE by Aiza Eman — Software Engineer

    </div>

</div>

</body>

</html>
"""


# ================================================================
#                    URL ANALYSIS FUNCTION
# ================================================================

def analyze_url(url):

    result = {}

    # ------------------------------------------------------------
    # Clean URL
    # ------------------------------------------------------------

    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    # ------------------------------------------------------------
    # Domain
    # ------------------------------------------------------------

    domain = parsed.hostname

    if not domain:
        raise ValueError("Invalid URL. Please enter a valid website address.")

    result["domain"] = domain
    result["scheme"] = parsed.scheme.upper()

    score = 100
    recommendations = []

    # ------------------------------------------------------------
    # HTTPS CHECK
    # ------------------------------------------------------------

    if parsed.scheme.lower() == "https":

        result["https"] = "✅ Enabled"

    else:

        result["https"] = "❌ Not Secure"
        score -= 30

        recommendations.append(
            "Use HTTPS websites whenever possible."
        )

    # ------------------------------------------------------------
    # IP ADDRESS CHECK
    # ------------------------------------------------------------

    ip_detected = False

    try:

        ipaddress.ip_address(domain)
        ip_detected = True

    except ValueError:

        ip_detected = False

    if ip_detected:

        result["ip"] = "⚠️ Yes"
        score -= 20

        recommendations.append(
            "The URL uses an IP address instead of a normal domain."
        )

    else:

        result["ip"] = "✅ No"

    # ------------------------------------------------------------
    # SUSPICIOUS CHARACTER CHECK
    # ------------------------------------------------------------

    suspicious_pattern = r"[@<>\"'`|{}\\]"

    suspicious_found = re.findall(
        suspicious_pattern,
        url
    )

    if suspicious_found:

        result["suspicious"] = (
            f"⚠️ Yes ({len(suspicious_found)} found)"
        )

        score -= min(
            20,
            len(suspicious_found) * 5
        )

        recommendations.append(
            "Review unusual characters carefully before visiting the URL."
        )

    else:

        result["suspicious"] = "✅ No"

    # ------------------------------------------------------------
    # URL LENGTH CHECK
    # ------------------------------------------------------------

    url_length = len(url)

    result["length"] = url_length

    if url_length > 200:

        score -= 15

        recommendations.append(
            "The URL is unusually long. Verify that all parameters are expected."
        )

    elif url_length > 100:

        score -= 5

        recommendations.append(
            "The URL is moderately long; review its parameters carefully."
        )

    # ------------------------------------------------------------
    # SUSPICIOUS KEYWORDS
    # ------------------------------------------------------------

    suspicious_words = [
        "login",
        "verify",
        "verification",
        "password",
        "account",
        "update",
        "secure",
        "confirm"
    ]

    found_words = []

    for word in suspicious_words:

        if word in url.lower():

            found_words.append(word)

    if len(found_words) >= 3:

        score -= 10

        recommendations.append(
            "The URL contains several security-related keywords. "
            "Verify the website through an official source."
        )

    # ------------------------------------------------------------
    # QUERY PARAMETER CHECK
    # ------------------------------------------------------------

    if parsed.query:

        if len(parsed.query) > 150:

            score -= 5

            recommendations.append(
                "The URL contains a large query string. "
                "Check its parameters before proceeding."
            )

    # ------------------------------------------------------------
    # FINAL SCORE
    # ------------------------------------------------------------

    score = max(0, min(100, score))

    if score >= 80:

        status = "🟢 LOW RISK"
        color = "safe"

        if not recommendations:

            recommendations.append(
                "No obvious warning signs were detected by this basic analyzer."
            )

    elif score >= 50:

        status = "🟡 MEDIUM RISK"
        color = "medium"

    else:

        status = "🔴 HIGH RISK"
        color = "danger"

    result["score"] = score
    result["status"] = status
    result["color"] = color
    result["recommendations"] = recommendations

    return result


# ================================================================
#                         FLASK ROUTE
# ================================================================

@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    error = ""
    url = ""

    if request.method == "POST":

        url = request.form.get("url", "").strip()

        if not url:

            error = "Please enter a URL."

        else:

            try:

                result = analyze_url(url)

            except ValueError as e:

                error = str(e)

            except Exception:

                error = "Unable to analyze this URL."

    return render_template_string(
        HTML,
        result=result,
        error=error,
        url=url
    )


# ================================================================
#                         APPLICATION
# ================================================================

if __name__ == "__main__":

    print("=" * 60)
    print("🛡️  CRYPTOVAULT - URL SECURITY ANALYZER")
    print("=" * 60)
    print("🌐 Open your browser and visit:")
    print("👉 http://127.0.0.1:5002")
    print("=" * 60)

    app.run(
        host="127.0.0.1",
        port=5002,
        debug=True
    )