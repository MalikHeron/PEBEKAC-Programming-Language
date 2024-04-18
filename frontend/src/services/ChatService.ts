/*
 * Represents a service for interacting with the chat functionality.
 */
export class ChatService {

   public async start_gemini(): Promise<string> {
      const apiUrl = 'https://pebekac.azurewebsites.net/start_gemini';

      // Fetch data from the local endpoint
      const response = await fetch(apiUrl, {
         method: 'POST',
         headers: {
            'Content-Type': 'application/json',
         }
      });

      // Parse the JSON response
      const data = await response.json();

      return data.response;
   }

   public async getResponse(query: string, userId: string): Promise<string> {
      // Local Flask backend URL
      const apiUrl = 'https://pebekac.azurewebsites.net/get_response';

      // Fetch data from the local endpoint
      const response = await fetch(apiUrl, {
         method: 'POST',
         headers: {
            'Content-Type': 'application/json',
         },
         body: JSON.stringify({ query: query, userId: userId }),
      });

      // Check if the response is successful
      if (!response.ok) {
         throw new Error('Network response was not ok');
      }

      // Parse the JSON response
      const data = await response.json();

      // Return the generated Python code from the API response
      return data.response;
   }
}