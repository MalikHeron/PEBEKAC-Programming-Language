import Editor from '@monaco-editor/react';
import '@styles/Playground.scss';
import Assistant from '@components/Assistant';
import { useEffect, useState } from 'react';
import { Terminal } from 'xterm';
import 'xterm/css/xterm.css';

function Playground() {
   const defaultCode = `fun main() {
    print("Hello World!");
}`;
   const [chatActive, setChatActive] = useState(true);
   const [terminalActive, setTerminalActive] = useState(false);
   const [code, setCode] = useState(defaultCode);
   const [output, setOutput] = useState('');
   const [reset, setReset] = useState(false);
   
   const handleEditorWillMount = (monaco) => {
      monaco.editor.defineTheme('myTheme', {
         base: 'vs-dark',
         inherit: true,
         rules: [
            //{ token: 'comment', foreground: 'ffa500', fontStyle: 'italic' },
            //{ token: 'keyword', foreground: '00ff00' },
         ],
         colors: {},
      });
   };

   // Function to toggle the side pane visibility
   const toggleSidePane = () => {
      const sidePane = document.querySelector('.side-pane');
      const editorPane = document.querySelector('.editor-pane') as HTMLElement;

      if (sidePane) {
         sidePane.classList.toggle('hide');

         if (editorPane) {
            if (sidePane.classList.contains('hide')) {
               editorPane.style.width = '100%'; // Expand editor pane to full width
            } else {
               editorPane.style.width = 'calc(100% - 450px)'; // Shrink editor pane to accommodate side pane
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
      });
      terminal.open(document.getElementById('terminal') as HTMLElement);
      terminal.write('$ ');

      // Handle user input
      let commandBuffer = '';
      const handleInput = async (data) => {
         const charCode = data.charCodeAt(0);
         if (charCode === 13) { // Enter key pressed
            terminal.writeln(''); // New line
            if (commandBuffer.trim() === '') {
               terminal.write('$ '); // Write prompt
            } else if (commandBuffer.trim() === 'clear') {
               terminal.reset(); // Clear the terminal
               terminal.write('$ '); // Write prompt
            } else if (commandBuffer.trim() === 'run') {
               // Simulate compiling and running code
               const response = await compileAndRunCode(defaultCode);
               setOutput(response);
               terminal.writeln(response); // Display output
               terminal.write('$ '); // Write prompt
            } else {
               terminal.writeln(`Command not found: ${commandBuffer}`);
               terminal.write('$ '); // Write prompt
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
   }, []);

   // Simulate compiling and running code (Replace with actual API calls)
   const compileAndRunCode = async (code) => {
      // Here you would send the code to your compiler API
      // and receive the response containing the output
      // For demonstration purposes, let's just return a static output
      return 'Hello from simulated compilation and execution!';
   };

   return (
      <div className="Playground">
         {/* side pane mini */}
         <div className='side-pane-mini' style={{
            marginRight: chatActive ? '' : '1.5em',
            borderRadius: chatActive ? '0px' : '',
            borderRight: chatActive ? 'none' : ''
         }}>
            <div
               className={`chat-btn ${chatActive ? 'active' : ''}`}
               onClick={() => {
                  setChatActive(!chatActive);
                  toggleSidePane();
               }}
            >
               <div className="indicator" />
               <div className='icon'>
                  <i className='bi-chat'></i>
               </div>
               <span className="tooltip-side">Chat</span>
            </div>
         </div>
         {/* side pane */}
         <div className="side-pane">
            <div className="content">
               <div className="header">
                  {chatActive &&
                     <>
                        <h6>Chat</h6>
                        <div className='action-buttons'>
                           <div className='reset-btn' onClick={() => setReset(true)}>
                              <i className='bi-arrow-clockwise'></i>
                              <span className="tooltip">Reset</span>
                           </div>
                        </div>
                     </>
                  }
               </div>
               <hr className="divider" />
               {chatActive && <Assistant reset={reset} setReset={setReset} />}
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
                  <button
                     className={`terminal-btn ${terminalActive ? 'active' : ''}`}
                     onClick={() => {
                        const terminalContainer = document.querySelector('.terminal-container') as HTMLElement;
                        setTerminalActive(!terminalActive); // Toggle terminal active state
                        if (!terminalActive) {
                           terminalContainer.style.display = 'block'; // Show terminal
                        } else {
                           terminalContainer.style.display = 'none'; // Hide terminal
                        }
                     }}
                  >
                     <div className='icon'>
                        <i className='bi-terminal'></i>
                     </div>
                     <span className="tooltip">Terminal</span>
                  </button>
                  <button className='download-btn' onClick={saveFile}>
                     <div className='icon'>
                        <i className='bi-download'></i>
                     </div>
                     <span className="tooltip">Download file</span>
                  </button>
                  <button className='run-btn'>
                     <div className='icon'>
                        <i className='bi-play'></i>
                     </div>
                     <span className="tooltip">Run code</span>
                  </button>
                  <button className='stop-btn' disabled={true}>
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
                     defaultLanguage="kotlin"
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
               {/* output */}
               <div className='terminal-container'>
                  <h6 className='header'>
                     TERMINAL
                  </h6>
                  <div id='terminal' />
               </div>
            </div>
         </div>
      </div>
   );
}

export default Playground;