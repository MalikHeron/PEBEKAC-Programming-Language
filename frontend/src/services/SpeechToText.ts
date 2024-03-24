import { useEffect, useState, useRef } from 'react';
import {
   SpeechRecognition,
   SpeechGrammarList,
   SpeechRecognitionEvent,
} from 'web-speech-cognitive-services';

declare global {
   interface Window {
      SpeechRecognition: typeof SpeechRecognition;
      webkitSpeechRecognition: typeof SpeechRecognition;
      SpeechGrammarList: typeof SpeechGrammarList;
      webkitSpeechGrammarList: typeof SpeechGrammarList;
      SpeechRecognitionEvent: typeof SpeechRecognitionEvent;
      webkitSpeechRecognitionEvent: typeof SpeechRecognitionEvent;
   }
}

function useSpeechToText(setUserInput: React.Dispatch<React.SetStateAction<string>>) {
   const [isListening, setIsListening] = useState(false);
   const recognition = useRef<SpeechRecognition | null>(null);

   useEffect(() => {
      const SpeechRecognition =
         window.SpeechRecognition || window.webkitSpeechRecognition;
      const SpeechGrammarList =
         window.SpeechGrammarList || window.webkitSpeechGrammarList;

      if (SpeechRecognition && SpeechGrammarList) {
         recognition.current = new SpeechRecognition();
         const speechRecognitionList = new SpeechGrammarList();

         recognition.current.grammars = speechRecognitionList;
         recognition.current.continuous = false;
         recognition.current.lang = "en-US";
         recognition.current.interimResults = false;
         recognition.current.maxAlternatives = 1;

         recognition.current.onresult = (event: SpeechRecognitionEvent) => {
            //console.log(`Result received: ${text}.`);
            //console.log(`Confidence: ${event.results[0][0].confidence}`);
            let text = event.results[0][0].transcript;
            if (text.length > 150) {
               text = text.substring(0, 150);
            }
            setUserInput(text);
         };

         recognition.current.onspeechend = () => {
            setIsListening(false);
         };

         recognition.current.onnomatch = () => {
            //console.log("I didn't recognize that.");
            setIsListening(false);
         };

         recognition.current.onerror = () => {
            //console.log(`Error occurred in recognition: ${event.error}`);
            setIsListening(false);
         };
      }
   }, [setUserInput]);

   useEffect(() => {
      if (isListening) {
         recognition.current?.start();
         //console.log("Ready to receive a command.");
      } else {
         recognition.current?.stop();
      }
   }, [isListening]);

   return { isListening, setIsListening };
}

export default useSpeechToText;