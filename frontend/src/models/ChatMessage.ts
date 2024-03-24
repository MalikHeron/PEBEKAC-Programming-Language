import { Timestamp } from "firebase/firestore";

export interface ChatMessage {
   author: string;
   text: string;
   timestamp: Timestamp;
}