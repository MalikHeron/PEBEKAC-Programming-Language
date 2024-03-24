import { ChatMessage } from '@models/ChatMessage';
import { useState, useRef, useEffect } from 'react';
import '@styles/ChatPage.scss';
import ReactMarkdown from 'react-markdown';
import { Timestamp } from 'firebase/firestore';
import { Link } from 'react-router-dom'
import useSpeechToText from '@services/SpeechToText';
import profileImg from "@assets/images/profile-gray.png";
import profileImgWhite from "@assets/images/profile-white.png";
import { ChatService } from '@services/ChatService';

function ChatPage() {
   const [userInput, setUserInput] = useState('');
   const [messages, setMessages] = useState<ChatMessage[]>([]);
   const [isLoading, setIsLoading] = useState(false);
   const textAreaRef = useRef<HTMLTextAreaElement>(null);
   const chatContainerRef = useRef<HTMLDivElement>(null);
   const [clearIndex, setClearIndex] = useState(false);
   const characterCount = `${userInput.length}/150`;
   const { isListening, setIsListening } = useSpeechToText(setUserInput);
   const [tooltipTexts, setTooltipTexts] = useState<string[]>([]);
   const [suggestions, setSuggestions] = useState<string[]>([]);
   const [speechToTextSupported, setSpeechToTextSupported] = useState(true);
   const [suggestionsLoaded, setSuggestionsLoaded] = useState(true);

   const copyToClipboard = (message: string, index: number) => {
      navigator.clipboard.writeText(message);
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
      setSuggestionsLoaded(false);

      try {
         // Send message to backend here
         let response = '';
         await new Promise<void>((resolve) => {
            new ChatService().getResponse(trimmedInput).then((botResponse) => {
               response = botResponse;
               //const botMessage = { author: 'bot', text: response, timestamp: new Timestamp(seconds, milliseconds) };
               //updatedMessages = [...newMessages, botMessage];
               resolve();
            });
         });

         if (response === '') {
            throw new Error('Error occurred while streaming');
         }
      } catch (error) {
         console.error(error);
         now = Date.now(); // Get the current time in milliseconds
         seconds = Math.floor(now / 1000); // Convert to seconds
         milliseconds = now % 1000; // Get the remaining milliseconds

         const errorMessage = { author: 'bot', text: "Sorry, I'm unable to provide a response at this time. Please try again later.", timestamp: new Timestamp(seconds, milliseconds) };
         setMessages([...newMessages, errorMessage]);
         setIsLoading(false);
      } finally {
         setSuggestionsLoaded(true);
      }
   };

   textAreaRef.current?.addEventListener('keypress', function (e) {
      const maxLength = 150;

      if (textAreaRef.current) {
         if (textAreaRef.current.value.length > maxLength) {
            e.preventDefault();
         }
      }
   });

   textAreaRef.current?.addEventListener('paste', function (e) {
      const maxLength = 150;

      if (e.clipboardData && textAreaRef.current) {
         const pastedText = e.clipboardData.getData('text');
         if (pastedText.length + textAreaRef.current.value.length > maxLength) {
            e.preventDefault();
            const textToPaste = pastedText.slice(0, maxLength - textAreaRef.current.value.length);
            textAreaRef.current.value += textToPaste;
            textAreaRef.current.focus();
         }
      }
   });

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
         textAreaRef.current.style.height = `${scrollHeight > 100 ? 100 : scrollHeight}px`;
         chatContainerRef.current.style.height = `${scrollHeight > 80 ? '85%' : '90%'}`;
      }
   }, [userInput]);

   useEffect(() => {
      // Scroll to the bottom of the chat container whenever the messages array changes
      if (chatContainerRef.current) {
         chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
      }
   }, [messages, suggestions]);

   return (
      <div className="ChatPage">
         <div className="backdrop"></div>
         {/* sidebar */}
         <div className="sidebar">
            <div className="sidebar-content">
               {/* chat history */}
               <div className="chat-history">
                  <div className="header">
                     <h6>File Explorer</h6>
                     <button type="button" className="close-btn">
                        <i className='bi-chevron-left'></i>
                     </button>
                  </div>
                  <hr className="divider" />
               </div>

               {/*profile*/}
               <div className="profile">
                  <div className="profile-card">
                     <Link className="profile-info" to="/profile">
                        <img className='profile-picture' src={profileImgWhite} alt="" />
                     </Link>
                     <div className='actions'>
                        <button className="logout-button">
                           <i className='bi-power'></i>
                           <span className="tooltip">Logout</span>
                        </button>
                     </div>
                  </div>
               </div>
            </div>
         </div>

         {/* chat pane */}
         <div className="chat-pane">
            <div ref={chatContainerRef} className="conversation-container card">
               <div className="mobile-toggles">
                  {/* sidebar open button for mobile*/}
                  <button className="sidebar-open-btn">
                     <i className='bi-layout-sidebar-inset'></i>
                  </button>
                  {/* feedback button for mobile*/}
                  <button className="feedback-btn-mobile" type="button" data-bs-toggle="modal" data-bs-target="#feedbackModal">
                     <i className='bi-chat'></i>
                  </button>
               </div>

               {/* Display the messages */}
               {messages.map((message, index) => (
                  <div key={index} className={`message-container`}>
                     <div className='message-header'>
                        <div className='user-avatar'>
                           {message.author === 'user' ?
                              <img className='icon' src={profileImg} alt="" /> :
                              <img className='icon' src='icon.png' alt="" />
                           }
                        </div>
                        <div className='message-author' style={{ color: message.author === 'user' ? 'white' : 'var(--sophie-blue)' }}>{message.author === 'user' ? 'You' : 'Sophie'}</div>
                     </div>
                     <div className={`message-card ${message.author === 'user' ? 'user' : 'other'}`}>
                        <ReactMarkdown className="message-text">
                           {message.text}
                        </ReactMarkdown>
                        {message.author !== 'user' ?
                           <div className="actions">
                              <div id="copy" className="copy-message" onClick={() => copyToClipboard(message.text, index)}>
                                 <i className='bi-copy'></i>
                                 <span className="tooltip">{tooltipTexts[index]}</span>
                              </div>
                           </div>
                           : null
                        }
                     </div>
                  </div>
               ))}

               {/* Display the suggestions */}
               <div className="suggestions-list">
                  {suggestions.map((suggestion, index) => (
                     <div key={index} className="suggestion" onClick={() => setUserInput(suggestion)}>
                        {suggestion}
                     </div>
                  ))}
               </div>

               {/* loading indicator */}
               {isLoading && (
                  <div className="loading-message">
                     <div className='message-header'>
                        <div className='user-avatar'>
                           <img className='icon' src='icon.png' alt="" />
                        </div>
                        <div className='message-author' style={{ color: 'var(--sophie-blue)' }}>Sophie</div>
                     </div>
                     <div className="content">
                        <span>I'm thinking</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                        <div className="dot-pulse"></div>
                     </div>
                  </div>
               )}
            </div>

            {/* prompt container */}
            <div className="prompt-container">
               {/* new chat button */}
               <button className="new-chat-button" disabled={messages.length === 0 || isLoading || !suggestionsLoaded} onClick={() => { setMessages([]), setClearIndex(!clearIndex), setSuggestions([]) }}>
                  <i className='bi-chat-text'></i>
                  <span className="tooltip">New chat</span>
               </button>
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
                     maxLength={150}
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
                     <div className="character-count">{characterCount}</div>
                  </div>
               </div>
            </div>
         </div>
      </div>
   );
}

export default ChatPage;