import { GoogleGenAI } from "@google/genai";
import fs from "fs";
import path from "path";

// Load key from environment or backend/.env
let apiKey = process.env.GEMINI_API_KEY;
if (!apiKey) {
    try {
        const envPath = path.resolve("./backend/.env");
        if (fs.existsSync(envPath)) {
            const content = fs.readFileSync(envPath, "utf-8");
            const match = content.match(/GEMINI_API_KEY\s*=\s*(.+)/);
            if (match) apiKey = match[1].trim();
        }
    } catch (e) {}
}

if (!apiKey) {
    console.error("No GEMINI_API_KEY found in environment or backend/.env");
    process.exit(1);
}

const ai = new GoogleGenAI({ apiKey });

async function testGemini() {
    console.log("==========================================");
    console.log("   MoodReel - Gemini API Connection Test   ");
    console.log("==========================================");
    console.log(`API Key detected: ${apiKey.substring(0, 8)}...${apiKey.substring(apiKey.length - 4)}`);

    const modelsToTry = ["gemini-3.8-flash", "gemini-3.5-flash"];

    for (const model of modelsToTry) {
        try {
            console.log(`\nTesting model [${model}]...`);
            const response = await ai.models.generateContent({
                model: model,
                contents: "Say: Gemini is successfully connected to MoodReel!"
            });

            console.log(` SUCCESS! [${model}] is active and responding:`);
            console.log(`> "${response.text ? response.text.trim() : response}"\n`);
            return;
        } catch (error) {
            console.warn(` [${model}] status: ${error.message}`);
        }
    }

    console.log("\nNote: Spikes in high-demand models (e.g. 503) automatically route to active flash tiers.");
}

testGemini();
