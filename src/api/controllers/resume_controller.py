from flask.views import MethodView
from flask import request, jsonify
import os, json, re, fitz, docx, yaml
from werkzeug.utils import secure_filename
from src.constants import infoConstant as constant
from src.utils.loggerUtils import CustomJSONFormatter as logger

# Load config
with open("config.yaml") as f:
    config = yaml.safe_load(f)

UPLOAD_FOLDER = config["app"]["upload_folder"]

class ResumeController(MethodView):

    def extract_info(self, file_path):
        text = ""
        if file_path.endswith(".pdf"):
            with fitz.open(file_path) as doc:
                for page in doc:
                    text += page.get_text()
        elif file_path.endswith(".docx"):
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + ' '

        # Extract name safely
                # Extract name more accurately
        name = "N/A"
        name_match = re.search(r"(?:Name|Full Name)[:\- ]+([^\n\r]+)", text, re.IGNORECASE)
        if name_match:
            name = name_match.group(1).strip()
        else:
            for line in text.splitlines():
                line = line.strip()
                if (
                    len(line.split()) >= 2 and
                    all(word[0].isupper() for word in line.split() if word.isalpha()) and
                    not any(loc in line.lower() for loc in ["india", "gujarat", "mumbai", "delhi", "bangalore", "pune", "ahmedabad"])
                ):
                    name = line
                    break


        # Extract email
        email_match = re.search(r"[\w\.-]+@[\w\.-]+", text)
        email = email_match.group(0) if email_match else "N/A"

        # Extract phone
        phone_match = re.search(r"(\+?\d{1,2}\s?)?(\(?\d{3}\)?[\s.-]?)?\d{3}[\s.-]?\d{4}", text)
        phone = phone_match.group(0) if phone_match else "N/A"

        return {
            'name': name,
            'email': email,
            'phone': phone,
            'text': text
        }

    def score_resume(self, text):
        try:
            with open("requirements.json") as f:
                req = json.load(f)
        except:
            return 0.0, "FAIL"

        required_keywords = req.get("requirements", [])
        threshold = req.get("threshold", 6)
        text_lower = text.lower()
        matched = sum(1 for k in required_keywords if k.lower() in text_lower)
        content_score = round((matched / len(required_keywords)) * 10, 1) if required_keywords else 0.0

        structure_score = 0
        for section in ['skills', 'education', 'experience']:
            if section in text_lower:
                structure_score += 1
        if 300 <= len(text_lower.split()) <= 1000:
            structure_score += 1
        if '•' in text_lower:
            structure_score += 1

        final_structure_score = round((structure_score / 6) * 10, 1)
        final_score = round(0.7 * content_score + 0.3 * final_structure_score, 1)
        status = "PASS" if final_score >= threshold else "FAIL"
        return final_score, status

    def uploadResume(self, data):
        try:
            if "resume" not in request.files:
                return jsonify({"error": "No file uploaded"}), 400
            file = request.files["resume"]
            filename = secure_filename(file.filename)
            path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(path)

            info = self.extract_info(path)
            score, status = self.score_resume(info['text'])
            info.pop('text')
            info['score'] = score
            info['status'] = status

            with open("candidates.json", "r+") as f:
                try:
                    records = json.load(f)
                except:
                    records = []
                records.append(info)
                f.seek(0)
                json.dump(records, f, indent=2)

            return jsonify({"message": "Resume processed", "status": status, "score": score})
        except Exception as e:
            logger.CreateLog("ERROR", constant.UPLOAD_FAILED, 500, 112, str(e))
            return jsonify({"error": "Internal Server Error"}), 500
