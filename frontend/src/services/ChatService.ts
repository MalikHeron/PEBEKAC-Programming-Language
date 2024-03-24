import { GoogleGenerativeAI, HarmCategory, HarmBlockThreshold } from "@google/generative-ai";

const MODEL_NAME = "gemini-1.0-pro";

/**
 * Represents a service for interacting with the chat functionality.
 */
export class ChatService {

   public async getResponse(query: string): Promise<string> {
      const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
      const model = genAI.getGenerativeModel({ model: MODEL_NAME });

      const generationConfig = {
         temperature: 0.9,
         topK: 1,
         topP: 1,
         maxOutputTokens: 2048,
      };

      const safetySettings = [
         {
            category: HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
         },
         {
            category: HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
         },
         {
            category: HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
         },
         {
            category: HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
         },
      ];

      const parts = [
         { text: `You are a code assistant for the python programming language. You shouldn't answer any query that isn't related to python. When asked to write a program, you should only provide the raw code.\nQuery: ${query}` },
      ];

      const result = await model.generateContent({
         contents: [{ role: "user", parts }],
         generationConfig,
         safetySettings,
      });

      const response = result.response;
      console.log(response.text());
      return response.text();
   }
}