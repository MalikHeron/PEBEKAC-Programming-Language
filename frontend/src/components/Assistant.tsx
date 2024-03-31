import { ChatMessage } from '@models/ChatMessage';
import { useEffect, useRef, useState } from 'react';
import '@styles/Assistant.scss';
import ReactMarkdown from 'react-markdown';
import { Timestamp } from 'firebase/firestore';
import useSpeechToText from '@services/SpeechToText';
import { ChatService } from '@services/ChatService';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { darcula } from 'react-syntax-highlighter/dist/esm/styles/prism';

function Assistant({ reset, setReset }) {
   const [userInput, setUserInput] = useState('');
   const [messages, setMessages] = useState<ChatMessage[]>([]);
   const [isLoading, setIsLoading] = useState(false);
   const textAreaRef = useRef<HTMLTextAreaElement>(null);
   const chatContainerRef = useRef<HTMLDivElement>(null);
   const { isListening, setIsListening } = useSpeechToText(setUserInput);
   const [tooltipTexts, setTooltipTexts] = useState<string[]>([]);
   const [suggestions, setSuggestions] = useState<string[]>([]);
   const [speechToTextSupported, setSpeechToTextSupported] = useState(true);

   const copyToClipboard = (message: string, index: number) => {
      if (message) {
         navigator.clipboard.writeText(message.trim())
            .then(() => {
               setTooltipTexts(prevTooltipTexts => {
                  const newTooltipTexts = [...prevTooltipTexts];
                  newTooltipTexts[index] = 'Copied!';
                  return newTooltipTexts;
               });
               setTimeout(() => {
                  setTooltipTexts(prevTooltipTexts => {
                     const newTooltipTexts = [...prevTooltipTexts];
                     newTooltipTexts[index] = 'Copy';
                     return newTooltipTexts;
                  });
               }, 3000);
            })
            .catch(err => {
               console.error('Failed to copy text: ', err);
            });
      }
   };

   const sendMessage = async () => {
      if (!userInput) return;

      setSuggestions([]);

      const trimmedInput = userInput.trim();
      let now = Date.now(); // Get the current time in milliseconds
      let seconds = Math.floor(now / 1000); // Convert to seconds
      let milliseconds = now % 1000; // Get the remaining milliseconds

      const newUserMessage = { author: 'user', text: trimmedInput, timestamp: new Timestamp(seconds, milliseconds) };
      const newMessages = [...messages, newUserMessage];
      setMessages(newMessages);
      setUserInput('');
      setIsLoading(true);

      try {
         // Send message to backend here
         new ChatService().getResponse(trimmedInput).then((botResponse) => {
            const botMessage = { author: 'bot', text: botResponse, timestamp: new Timestamp(seconds, milliseconds) };
            setMessages([...newMessages, botMessage]);
         }).catch((error) => {
            throw error;
         });
      } catch (error) {
         console.error(error);
         now = Date.now(); // Get the current time in milliseconds
         seconds = Math.floor(now / 1000); // Convert to seconds
         milliseconds = now % 1000; // Get the remaining milliseconds

         const errorMessage = { author: 'bot', text: "Sorry, I'm unable to provide a response at this time. Please try again later.", timestamp: new Timestamp(seconds, milliseconds) };
         setMessages([...newMessages, errorMessage]);
      } finally {
         setIsLoading(false);
      }
   };

   useEffect(() => {
      const SpeechRecognition =
         window.SpeechRecognition || window.webkitSpeechRecognition;
      const SpeechGrammarList =
         window.SpeechGrammarList || window.webkitSpeechGrammarList;

      if (!SpeechRecognition || !SpeechGrammarList) {
         setSpeechToTextSupported(false);
         return;
      }
   }, []);

   useEffect(() => {
      setTooltipTexts(new Array(messages.length).fill('Copy'));
   }, [messages]);

   useEffect(() => {
      // focus on textarea whenever userInput changes
      if (textAreaRef.current) {
         textAreaRef.current.focus();
         textAreaRef.current.value.length;
      }
   }, [userInput]);

   useEffect(() => {
      if (textAreaRef.current && chatContainerRef.current) {
         textAreaRef.current.style.height = 'inherit';
         const scrollHeight = textAreaRef.current.scrollHeight;
         textAreaRef.current.style.height = `${scrollHeight > 300 ? 300 : scrollHeight}px`;
         chatContainerRef.current.style.height = `${scrollHeight > 80 ? '85%' : '90%'}`;
      }
   }, [userInput]);

   useEffect(() => {
      // Scroll to the bottom of the chat container whenever the messages array changes
      if (chatContainerRef.current) {
         chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
      }
   }, [messages, suggestions]);

   useEffect(() => {
      if (reset) {
         setMessages([]);
         setReset(false);
      }
   }, [reset, setReset]);

   return (
      <div className="Assistant">
         {/* chat pane */}
         <div className="assistant-pane">
            <div ref={chatContainerRef} className="conversation-container card">
               {/* Display the messages */}
               {messages.map((message, index) => (
                  <div key={index} className={`message-container`}>
                     <div className='message-header'>
                        <div className='message-author' style={{ color: message.author === 'user' ? 'white' : 'var(--sophie-blue)' }}>{message.author === 'user' ? 'You' : 'Assistant'}</div>
                     </div>
                     <div className={`message-card ${message.author === 'user' ? 'user' : 'other'}`}>
                        <>
                           {message.text.replace('```pebekac', '```').split('```').map((part, idx) => {
                              if (idx % 2 === 0) {
                                 return <ReactMarkdown key={idx} className="message-text">{part}</ReactMarkdown>;
                              } else {
                                 return (
                                    <div key={idx}>
                                       <SyntaxHighlighter language="kotlin" style={darcula}>
                                          {part}
                                       </SyntaxHighlighter>
                                       <div className="actions">
                                          <div id="copy" className="copy-message" onClick={() => copyToClipboard(part, index)}>
                                             <i className='bi-copy'></i>
                                             <span className="tooltip">{tooltipTexts[index]}</span>
                                          </div>
                                       </div>
                                    </div>
                                 );
                              }
                           })}
                        </>
                     </div>
                  </div>
               ))}
            </div>
            {/* prompt container */}
            <div className="prompt-container">
               {/* input box */}
               <div className="input-container">
                  <textarea
                     ref={textAreaRef}
                     className="input"
                     placeholder={'Ask me anything...'}
                     value={userInput}
                     onChange={(e) => setUserInput(e.target.value)}
                     onKeyDown={(e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                           e.preventDefault();
                           if (!isLoading)
                              sendMessage();
                        }
                     }}
                     autoFocus
                     rows={1}
                  />
                  <div className="input-footer">
                     <button className="mic-button" style={{ display: speechToTextSupported ? (userInput ? 'none' : 'flex') : 'none', animation: isListening ? 'listening 1s infinite' : 'none' }} onClick={() => { setIsListening(prevState => !prevState); }}>
                        <div className="icon" style={{ animation: isListening ? 'listen 1s infinite' : 'none' }}>
                           <i className={`bi-mic${isListening ? '-fill' : ''}`}></i>
                           <span className="tooltip" style={{ transform: isListening ? 'translate(-38px, -70px)' : '' }}>{isListening ? 'Stop listening' : 'Use microphone'}</span>
                        </div>
                     </button>
                     <button className="send-button" disabled={isLoading || userInput === ''} style={{ display: speechToTextSupported ? (userInput ? 'flex' : 'none') : 'flex' }} onClick={sendMessage}>
                        <div className="icon">
                           <i className='bi-send-fill'></i>
                        </div>
                     </button>
                  </div>
               </div>
            </div>
         </div>
      </div>
   );
}

export default Assistant;