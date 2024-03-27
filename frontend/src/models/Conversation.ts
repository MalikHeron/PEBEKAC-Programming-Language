import { Timestamp } from "firebase/firestore";
import { ChatMessage } from "./ChatMessage";

export interface Conversation {
   id: string;
   name: string;
   time: Timestamp;
   messages: ChatMessage[];
}