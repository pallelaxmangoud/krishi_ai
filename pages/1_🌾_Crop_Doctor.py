import streamlit as st
from PIL import Image
import requests
import base64
import io
from utils.i18n_helper import t

st.title(f"🌾 {t('crop_doctor_header')}")
st.write(t('crop_doctor_sub'))
st.write("---")

uploaded_file = st.file_uploader(t('upload_label'), type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Leaf Image", width=350)
    
    if st.button(t('analyze_button'), type="primary"):
        ai_mode = st.session_state.get("ai_mode", "Local Inference (Ollama)")
        lang_code = st.session_state.get("lang_code", "en")
        
        lang_names = {"en": "English", "te": "Telugu", "hi": "Hindi"}
        target_language = lang_names.get(lang_code, "English")
        
        system_instruction = (
            f"You are an expert plant pathologist. Analyze this leaf image. "
            f"Identify the probable disease, suggest organic treatments, and chemical options. "
            f"CRITICAL RULE: Provide your entire diagnosis report fluently in the {target_language} language only."
        )

        with st.spinner("Analyzing image... Please wait."):
            if "BYOK" in ai_mode:
                api_key = st.session_state.get("api_key", "").strip()
                provider = st.session_state.get("api_provider", "Google Gemini")
                
                if not api_key:
                    st.error("⚠️ Please enter your API Key in the sidebar configuration on the Home page!")
                else:
                    buffered = io.BytesIO()
                    image.save(buffered, format="JPEG")
                    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                    
                    if provider == "Google Gemini":
                        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                        payload = {
                            "contents": [{
                                "parts": [
                                    {"text": system_instruction},
                                    {
                                        "inlineData": {
                                            "mimeType": "image/jpeg",
                                            "data": img_base64
                                        }
                                    }
                                ]
                            }]
                        }
                        try:
                            res = requests.post(url, json=payload, timeout=120)
                            if res.status_code == 200:
                                ai_text = res.json()['candidates'][0]['content']['parts'][0]['text']
                                st.success("📋 Diagnosis Report:")
                                st.markdown(ai_text)
                            else:
                                st.error(f"Gemini API returned error code: {res.status_code}")
                        except Exception as e:
                            st.error(f"Error processing image: {str(e)}")
            else:
                st.info("💡 **Local Vision Inference:** To process images locally offline, run a vision model like `llava` using: `ollama run llava`")