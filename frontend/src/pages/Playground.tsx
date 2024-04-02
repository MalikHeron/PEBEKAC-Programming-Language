import Editor from '@monaco-editor/react';
import '@styles/Playground.scss';
import Assistant from '@components/Assistant';
import { useEffect, useRef, useState } from 'react';
import { Terminal } from 'xterm';
import 'xterm/css/xterm.css';

function Playground() {
   const terminalRef = useRef<HTMLDivElement>(null);
   const [terminalInstance, setTerminalInstance] = useState<Terminal | null>(null);
   const defaultCode = `# Check if two strings are the same
fun boolean stringEquals(string string1, string string2) {
    return string1 == string2;
}

// main function
fun main() {
    // call the equals function to compare the two strings
    if (stringEquals("Hello", "hello")) {
        print("The strings are equal");
    } else {
        print("The strings are not equal");
    }
}

main();`;
   const [chatActive, setChatActive] = useState(true);
   const [terminalActive, setTerminalActive] = useState(false);
   const [code, setCode] = useState(defaultCode);
   const [reset, setReset] = useState(false);
   const [running, setRunning] = useState(false);

   const handleEditorWillMount = (monaco) => {
      monaco.editor.defineTheme('myTheme', {
         base: 'vs-dark',
         inherit: true,
         rules: [],
         colors: {},
      });

      monaco.languages.register({ id: 'PEBEKAC' });

      monaco.languages.setMonarchTokensProvider('PEBEKAC', {
         keywords: [
            'fun', 'return', 'if', 'else', 'for', 'while', 'void', 'break',
            'true', 'false', 'True', 'False', 'null', 'list', 'len',
            'intArray', 'floatArray', 'stringArray', 'doubleArray',
            'int', 'float', 'double', 'string', 'boolean', 'print'
         ],
         tokenizer: {
            root: [
               // Comments
               [/\/\*/, 'comment', '@comment'],
               [/\/\/.*/, 'comment'],
               [/#.*/, 'comment'],

               // Keywords and identifiers
               [/[a-zA-Z_$][\w$]*/, {
                  cases: {
                     '@keywords': 'keyword',
                     '@default': 'identifier'
                  }
               }],

               // Numeric literals
               [/\b\d+\b/, 'number'],

               // String literals
               [/"/, { token: 'string.quote', bracket: '@open', next: '@string_double' }],
               [/'/, { token: 'string.quote', bracket: '@open', next: '@string_single' }],

               // Operators and punctuation
               [/[+\-*/=<>!]+/, 'operator'],
               [/[()[\]{}.,;]/, 'delimiter'],

               // Whitespace
               { include: '@whitespace' },
            ],
            whitespace: [
               [/\s+/, 'white']
            ],
            comment: [
               [/\*\//, 'comment', '@pop'],
               [/./, 'comment']
            ],
            string_double: [
               [/[^\\"]+/, 'string'],
               [/\\./, 'string.escape'],
               [/"/, { token: 'string.quote', bracket: '@close', next: '@pop' }]
            ],
            string_single: [
               [/[^\\']+/, 'string'],
               [/\\./, 'string.escape'],
               [/'/, { token: 'string.quote', bracket: '@close', next: '@pop' }]
            ]
         }
      });
   };

   // Function to toggle the side pane visibility
   const toggleSidePane = () => {
      const sidePane = document.querySelector('.side-pane');
      const editorPane = document.querySelector('.editor-pane') as HTMLElement;
      const editorContainer = document.querySelector('.editor-container') as HTMLElement;
      const terminalContainer = document.querySelector('.terminal-container') as HTMLElement;
      const navTabs = document.querySelector('.nav-tabs') as HTMLElement;

      if (sidePane) {
         sidePane.classList.toggle('hide');

         if (editorPane) {
            if (sidePane.classList.contains('hide')) {
               editorPane.style.width = '100%'; // Expand editor pane to full width
               editorContainer.style.borderRadius = '0px 10px 10px 0px';
               terminalContainer.style.borderRadius = '0px 0px 10px 0px';
               navTabs.style.setProperty('--bs-nav-tabs-border-radius', '0px');
            } else {
               editorPane.style.width = 'calc(100% - 450px)'; // Shrink editor pane to accommodate side pane
               editorContainer.style.borderRadius = '0px 10px 10px 10px';
               terminalContainer.style.borderRadius = '0px 10px 10px 10px';
               navTabs.style.setProperty('--bs-nav-tabs-border-radius', '');
            }
         }
      }
   }

   // Function to save the file
   const saveFile = () => {
      // Create a new anchor element
      const element = document.createElement('a');
      // Set the href attribute to the code content
      element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(code));
      // Set the download attribute to the file name
      element.setAttribute('download', 'main.pk');
      // Hide the element
      element.style.display = 'none';
      // Append the element to the document body
      document.body.appendChild(element);
      // Simulate a click event on the element
      element.click();
      // Remove the element from the document body
      document.body.removeChild(element);
   }

   // Function to handle terminal output
   const handleTerminalOutput = (line) => {
      // Check if the line contains an error message
      if (line.includes('Error:') || line.includes('Syntax error')) {
         // If so, write the line in red
         terminalInstance?.writeln(`\x1b[91m${line}\x1b[0m`);
      } else {
         // Otherwise, write the line as normal
         terminalInstance?.writeln(line);
      }
   };

   // Update the runCode function
   const runCode = async () => {
      try {
         if (!terminalActive && terminalInstance) {
            setTerminalActive(true); // Show the terminal if it's hidden
         }

         terminalInstance?.reset(); // Clear the terminal
         setRunning(true); // Set running state to true
         // Execute the code and handle user input prompts
         const condition = true;
         while (condition) {
            const response = await compileAndRunCode(code);
            const outputLines = response.split('\n');

            for (const line of outputLines) {
               handleTerminalOutput(line); // Use the new function to handle output
            }

            // Check if execution is complete or stopped
            if (response.execution_complete || stopRequested()) {
               if (terminalInstance) {
                  if (response.execution_complete) {
                     terminalInstance.writeln('Program execution complete.');
                     terminalInstance.write('$ ');
                  } else {
                     terminalInstance.writeln('Program execution stopped.');
                     terminalInstance.write('$ ');
                  }
               }
               break;  // Exit the loop
            }
         }
      } catch (error) {
         // Handle errors
         console.error('Error:', error);
      } finally {
         setRunning(false); // Set running state to false after execution
      }
   };


   // Function to request stopping the program execution
   const stopExecution = async () => {
      try {
         // Send a request to the server to stop execution
         const response = await fetch('https://pebekac.azurewebsites.net/stop_execution', { method: 'POST' });
         if (!response.ok) {
            throw new Error('Failed to stop execution.');
         }
      } catch (error) {
         console.error('Error:', error);
      }
   };

   // Function to check if the program execution should be stopped
   const stopRequested = () => {
      return !running;
   };

   // Function to compile and run code
   const compileAndRunCode = async (code) => {
      try {
         // Local Flask backend URL
         const apiUrl = 'https://pebekac.azurewebsites.net/compile_code';

         // Fetch data from the local endpoint
         const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
               'Content-Type': 'application/json',
            },
            body: JSON.stringify({ program_code: code }),
         });

         // Check if the response is successful
         if (!response.ok) {
            throw new Error('Network response was not ok');
         }

         // Parse the JSON response
         const data = await response.json();

         // Return the generated Python code from the API response
         return data.output;
      } catch (error) {
         return error;
      }
   };

   // Function to toggle the terminal visibility
   const toggleTerminal = () => {
      setTerminalActive((prevTerminalActive) => !prevTerminalActive); // Toggle terminal active state
   };

   // Function to toggle the chat visibility
   const toggleChat = () => {
      setChatActive((prevChatActive) => !prevChatActive); // Toggle chat active state
      toggleSidePane(); // Toggle side pane visibility
   };

   useEffect(() => {
      const terminal = new Terminal({
         theme: {
            background: '#1e1e1e',
            foreground: '#ffffff',
            cursor: '#ffffff'
         },
         cursorStyle: 'block',
         fontFamily: `"Fira Code", monospace`,
         fontSize: 14,
         rows: 10
      });

      if (terminalRef.current) {
         terminal.open(terminalRef.current);
         setTerminalInstance(terminal);
         terminal.write('$ ');
      }

      // Handle user input
      let commandBuffer = '';
      const handleInput = async (data) => {
         const charCode = data.charCodeAt(0);
         if (charCode === 13) { // Enter key pressed
            if (commandBuffer.trim() === 'clear' || commandBuffer.trim() === 'cls') {
               terminal.reset(); // Clear the terminal
               terminal.write('$ '); // Write prompt
            } else {
               // New line
               terminal.writeln('');
               if (commandBuffer.trim() === 'help') {
                  // Display help information
                  terminal.writeln('Available commands:');
                  terminal.writeln('clear - Clear the terminal');
                  terminal.writeln('cls   - Clear the terminal');
                  terminal.writeln('help  - Display this help information');
                  terminal.write('$ '); // Write prompt
               } else {
                  terminal.writeln(`Command not found: ${commandBuffer}`);
                  terminal.write('$ '); // Write prompt
               }
            }
            commandBuffer = ''; // Clear command buffer
         } else if (charCode === 127) { // Backspace key pressed
            if (commandBuffer.length > 0) {
               terminal.write('\b \b'); // Erase character
               commandBuffer = commandBuffer.slice(0, -1); // Remove character from buffer
            }
         } else {
            terminal.write(data); // Write character to terminal
            commandBuffer += data; // Add character to buffer
         }
      };

      // Listen for user input
      terminal.onData((data) => {
         handleInput(data);
      });

      return () => {
         terminal.dispose(); // Cleanup terminal instance on unmount
      };
      // eslint-disable-next-line react-hooks/exhaustive-deps
   }, []);

   useEffect(() => {
      const editorContainer = document.querySelector('.editor-container') as HTMLElement;
      const terminalContainer = document.querySelector('.terminal-container') as HTMLElement;

      if (terminalActive && chatActive) {
         editorContainer.style.borderRadius = '0px 10px 0px 0px';
         terminalContainer.style.borderRadius = '0px 0px 10px 10px';
      } else if (terminalActive && !chatActive) {
         editorContainer.style.borderRadius = '0px 10px 0px 0px';
         terminalContainer.style.borderRadius = '0px 0px 10px 0px';
      } else if (!terminalActive && chatActive) {
         editorContainer.style.borderRadius = '0px 10px 10px 10px';
      } else if (!terminalActive && !chatActive) {
         editorContainer.style.borderRadius = '0px 10px 10px 0px';
      }
   }, [terminalActive, chatActive]);

   // Add event listener for keyboard shortcuts
   useEffect(() => {
      const handleKeyDown = (e) => {
         // Handle keyboard shortcuts
         if (e.ctrlKey && e.key === 'e') {
            e.preventDefault(); // Prevent default browser behavior
            // Ctrl + E to run code
            runCode();
         } else if (e.ctrlKey && e.key === 's') {
            e.preventDefault(); // Prevent default browser behavior
            // Ctrl + S to save file
            saveFile();
         } else if (e.ctrlKey && e.key === 'k') {
            e.preventDefault(); // Prevent default browser behavior
            // Ctrl + K to toggle terminal visibility
            toggleTerminal();
         } else if (e.ctrlKey && e.key === 'q') {
            // Ctrl + C to toggle chat visibility
            setChatActive((prev) => !prev); // Toggle chat visibility
            toggleSidePane(); // Toggle side pane visibility
         }
      };

      // Attach event listener
      window.addEventListener('keydown', handleKeyDown);

      // Detach event listener on component unmount
      return () => {
         window.removeEventListener('keydown', handleKeyDown);
      };
      // eslint-disable-next-line react-hooks/exhaustive-deps
   }, []);

   return (
      <div className="Playground">
         {/* side pane mini */}
         <div className='side-pane-mini'>
            <div className={`chat-btn ${chatActive ? 'active' : ''}`} onClick={() => { toggleChat(); }}>
               <div className="indicator" />
               <div className='icon'>
                  <i className='bi-chat'></i>
               </div>
               <span className="tooltip-side">Chat</span>
            </div>
            <div className={`doc-btn`}>
               <div className="indicator" />
               <div className='icon'>
                  <i className='bi-journals'></i>
               </div>
               <span className="tooltip-side">Resources</span>
            </div>
         </div>
         {/* side pane */}
         <div className="side-pane">
            <div className="content">
               <div className="header">
                  <h6>Chat</h6>
                  <div className='action-buttons'>
                     <div className='reset-btn' onClick={() => setReset(true)}>
                        <i className='bi-arrow-clockwise'></i>
                        <span className="tooltip">Reset</span>
                     </div>
                  </div>
               </div>
               <hr className="divider" />
               <Assistant reset={reset} setReset={setReset} />
            </div>
         </div>
         {/* editor pane */}
         <div className="editor-pane">
            {/* editor header */}
            <div className="editor-header">
               <div className='tab-container'>
                  <ul className="nav nav-tabs">
                     <li className="nav-item">
                        <a className="nav-link active" aria-current="page">
                           main.pk
                        </a>
                     </li>
                  </ul>
               </div>
               <div className="action-container">
                  <button className='terminal-btn' onClick={toggleTerminal}>
                     <div className='icon'>
                        <i className='bi-terminal'></i>
                     </div>
                     <span className="tooltip">Terminal</span>
                  </button>
                  <button className='save-btn' onClick={saveFile}>
                     <div className='icon'>
                        <i className='bi-download'></i>
                     </div>
                     <span className="tooltip">Save file</span>
                  </button>
                  <button className='run-btn' onClick={runCode}>
                     <div className='icon'>
                        <i className='bi-play'></i>
                     </div>
                     <span className="tooltip">Run code</span>
                  </button>
                  <button className='stop-btn' style={{ display: running ? 'flex' : 'none' }} onClick={stopExecution}>
                     <div className='icon'>
                        <i className='bi-stop'></i>
                     </div>
                     <span className="tooltip">Stop</span>
                  </button>
               </div>
            </div>
            <div className='containers'>
               {/* editor */}
               <div className="editor-container">
                  <Editor
                     height="100%"
                     defaultLanguage="PEBEKAC"
                     defaultValue={defaultCode}
                     onChange={editorValue => { setCode(editorValue || '') }}
                     theme="myTheme"
                     beforeMount={handleEditorWillMount}
                     options={{
                        roundedSelection: true,
                        scrollbar: {
                           // Subtle shadow to the left & top. Defaults to true.
                           useShadows: false,
                           // Size of arrows (scrollbar buttons) in pixels. Defaults to 11.
                           arrowSize: 11,
                           // The scrollbar slider size will be increased by this number of pixels. Defaults to 0.
                           horizontalScrollbarSize: 11,
                           verticalScrollbarSize: 11,
                           // The scrollbar will be visible, even when the view does not overflow. Defaults to 'auto'.
                           vertical: 'visible',
                           horizontal: 'visible',
                           // Render vertical arrows (on the vertical scrollbar). Defaults to false.
                           verticalHasArrows: true,
                           // Render horizontal arrows (on the horizontal scrollbar). Defaults to false.
                           horizontalHasArrows: true,
                        },
                     }}
                  />
               </div>
               {/* terminal */}
               <div className='terminal-container' style={{ display: terminalActive ? 'block' : 'none' }}>
                  <h6 className='header'>
                     TERMINAL
                  </h6>
                  <div id='terminal' ref={terminalRef} />
               </div>
            </div>
         </div>
      </div>
   );
}

export default Playground;