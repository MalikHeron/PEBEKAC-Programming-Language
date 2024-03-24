import { Conversation } from "@models/Conversation";
import { getAuth } from "firebase/auth";
import { doc, collection, addDoc, getDocs, updateDoc, deleteDoc, getFirestore, DocumentData, DocumentReference } from "firebase/firestore";

/**
 * Represents a service for interacting with the database.
 */
export class DatabaseService {
   private auth = getAuth();
   private db = getFirestore();

   /**
    * Retrieves the conversations for the current user from the database.
    * @returns {Promise<Conversation[]>} - A Promise that resolves to an array of Conversation objects.
    */
   public async getConversations(): Promise<Conversation[]> {
      const currentUser = this.auth.currentUser;
      let conversations: Conversation[] = [];

      if (currentUser) {
         const conversationRef = collection(this.db, `users/${currentUser.uid}/conversations`);
         const snapshot = await getDocs(conversationRef);
         // Sort the data by time before mapping it to Conversation objects
         const sortedDocs = snapshot.docs.sort((a, b) => b.data().time.seconds - a.data().time.seconds);
         conversations = sortedDocs.map(doc => {
            const data = doc.data();
            // set conversation data to local storage
            localStorage.setItem(`${data.id}`, JSON.stringify(data));
            // return conversation object
            return {
               id: data.id,
               name: data.name,
               time: data.time,
               messages: data.messages
            } as Conversation;
         });
      }

      return conversations;
   }

   /**
    * Adds a conversation to the database.
    * 
    * @param conversation - The conversation object to be added.
    * @returns A promise that resolves to a string indicating the success of the operation.
    * @throws An error if there was an issue adding the conversation.
    */
   async addConversation(conversation: Conversation): Promise<string> {
      try {
         const currentUser = this.auth.currentUser;
         let conversationDoc: DocumentReference<DocumentData> | undefined;

         if (currentUser) {
            const conversationRef = collection(this.db, `users/${currentUser.uid}/conversations`);
            // Add the conversation object directly
            conversationDoc = await addDoc(conversationRef, conversation);
            // Update the 'id' field of the conversation object
            await updateDoc(conversationDoc, { id: conversationDoc.id });
         }
         return conversationDoc?.id || '';
      } catch (error) {
         console.error('Error adding conversation:', error);
         throw error;
      }
   }

   /**
    * Updates a conversation in the database.
    * 
    * @param conversationId - The ID of the conversation to be updated.
    * @param conversation - The updated conversation object.
    * @returns A promise that resolves to a string indicating the success of the operation.
    * @throws An error if there was an issue updating the conversation.
    */
   async updateConversation(conversationId: string, conversation: Conversation): Promise<string> {
      try {
         const currentUser = this.auth.currentUser;

         if (currentUser) {
            const conversationRef = doc(this.db, `users/${currentUser.uid}/conversations/${conversationId}`);
            (conversation.name !== '') ? await updateDoc(conversationRef, { name: conversation.name, messages: conversation.messages, time: conversation.time }) :
               await updateDoc(conversationRef, { messages: conversation.messages, time: conversation.time });
         }
         return 'success';
      } catch (error) {
         console.error('Error updating conversation:', error);
         throw error;
      }
   }

   /**
    * Deletes a conversation from the database.
    * 
    * @param conversationId - The ID of the conversation to delete.
    * @returns A promise that resolves to a string indicating the success of the operation.
    * @throws If there is an error deleting the conversation.
    */
   async deleteConversation(conversationId: string): Promise<string> {
      try {
         const currentUser = this.auth.currentUser;

         if (currentUser) {
            const conversationRef = doc(this.db, `users/${currentUser.uid}/conversations/${conversationId}`);
            await deleteDoc(conversationRef);
         }
         return 'success';
      } catch (error) {
         console.error('Error deleting conversation:', error);
         throw error;
      }
   }

   /**
    * Adds a log to the database.
    * @param {Object} data - The log data to be added.
    * @returns {Promise} A promise that resolves when the log is successfully added.
    * @throws {Error} If there is an error adding the log.
    */
   async addLog(data: object): Promise<string> {
      try {
         const logRef = collection(this.db, 'logs');
         await addDoc(logRef, data);
         return 'success';
      } catch (error) {
         console.error("Error adding log:", error);
         throw error;
      }
   }
}