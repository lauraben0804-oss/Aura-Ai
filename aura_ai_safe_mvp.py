import os
import openai
import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import json

# ----------------------------------
# 1. API Keys
# ----------------------------------
# Your OpenAI API Key (replace with the key you sent)
openai.api_key = "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"

# Covalent API Key (replace with your Covalent key)
COVALENT_API_KEY = "ckey_123abc456def789ghi0jkl"  # Replace with your actual Covalent key

# ----------------------------------
# 2. Local Memory
# ----------------------------------
MEMORY_FILE = "aura_memory.json"
if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump([], f)

def load_memory():
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f)

# ----------------------------------
# 3. Streamlit UI
# ----------------------------------
st.title("Aura AI – Your Personal AI Companion")
st.write("Friendly AI with Nigerian flair, Pidgin vibes, memory, and NFT-ready Aura Moments!")

memory = load_memory()
if memory:
    st.write("**Previous Conversations:**")
    for entry in memory[-5:]:
        st.write(f"**You:** {entry['user']}")
        st.write(f"**Aura AI:** {entry['ai']}")
        st.write("---")

user_input = st.text_input("Talk to Aura AI:")

if st.button("Send") and user_input:
    # ----------------------------------
    # 4. Chat Completion
    # ----------------------------------
    messages = [
        {"role": "system",
         "content": "You are Aura AI, friendly, witty, supportive. Mix English with Pidgin, Nigerian vibes, Port Harcourt energy. Always be encouraging and creative."}
    ]
    for entry in memory[-3:]:
        messages.append({"role": "user", "content": entry['user']})
        messages.append({"role": "assistant", "content": entry['ai']})
    messages.append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=150
    )
    ai_reply = response['choices'][0]['message']['content']
    st.write(f"**Aura AI:** {ai_reply}")

    memory.append({"user": user_input, "ai": ai_reply})
    save_memory(memory)

    # ----------------------------------
    # 5. Generate Aura Moment NFT-ready Image
    # ----------------------------------
    st.write("Generating Aura Moment image...")
    try:
        image_response = openai.Image.create(
            prompt=f"Aura Moment inspired by: {user_input}, Nigerian culture, Port Harcourt vibes, futuristic style, vibrant colors, NFT-ready",
            n=1,
            size="512x512"
        )
        image_url = image_response['data'][0]['url']
        image = Image.open(BytesIO(requests.get(image_url).content))
        st.image(image, caption="Aura Moment NFT", use_column_width=True)
    except Exception as e:
        st.write("Error generating image:", e)

# ----------------------------------
# 6. Free Read-only Web3 Wallet Insights (Stealth Gem demo)
# ----------------------------------
wallet_address = st.text_input("Enter wallet address to check Stealth Gem / NFTs")
if wallet_address and st.button("Check Wallet"):
    st.write("Fetching wallet info (read-only)...")

    chain_id = 137  # Polygon example
    url = f"https://api.covalenthq.com/v1/{chain_id}/address/{wallet_address}/balances_v2/?key={COVALENT_API_KEY}"
    
    try:
        resp = requests.get(url)
        data = resp.json()
        tokens = data.get("data", {}).get("items", [])

        # Show first 5 tokens for demo
        if tokens:
            for token in tokens[:5]:
                balance = int(token.get("balance", 0)) / (10 ** int(token.get("contract_decimals", 0)))
                st.write(f"{token.get('contract_ticker_symbol')}: {balance}")
            
            # Simple Stealth Gem alert
            stealth = [t for t in tokens if t.get("contract_ticker_symbol") == "SGEM"]
            if stealth:
                st.success(f"Stealth Gem Balance: {int(stealth[0]['balance']) / (10 ** int(stealth[0]['contract_decimals']))} – nice hold!")
            else:
                st.info("No Stealth Gems found in this wallet.")
        else:
            st.warning("Wallet is empty or no tokens found.")

    except Exception as e:
        st.error("Error fetching wallet data: " + str(e))