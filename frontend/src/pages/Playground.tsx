import Editor from '@monaco-editor/react';
import '@styles/Playground.scss';
import Assistant from '@components/Assistant';
import { /*useEffect,*/ useState } from 'react';
//import { Terminal } from 'xterm';
import 'xterm/css/xterm.css';

function Playground() {
   const defaultCode = `fun main() {
    print("Hello World!");
}`;
   const [collapse, setCollapse] = useState(false);
   //const [output, setOutput] = useState('');
   const handleEditorWillMount = (monaco) => {
      monaco.editor.defineTheme('myTheme', {
         base: 'vs-dark',
         inherit: true,
         rules: [
            { token: 'comment', foreground: 'ffa500', fontStyle: 'italic' },
            { token: 'keyword', foreground: '00ff00' },
         ],
         colors: {},
      });
   };

   const toggleSidePane = () => {
      const sidePane = document.querySelector('.side-pane');
      const editorPane = document.querySelector('.editor-pane') as HTMLElement;

      if (sidePane) {
         sidePane.classList.toggle('hide');

         if (editorPane) {
            if (sidePane.classList.contains('hide')) {
               editorPane.style.width = '100%';
            } else {
               editorPane.style.width = 'calc(100% - 350px)';
            }
         }
      }
   }

   /*useEffect(() => {
      const terminal = new Terminal();
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
   };*/

   return (
      <div className="Playground">
         {/* chat pane */}
         <div className="side-pane" >
            <div className="content">
               <div className="header">
                  <h6>Chat</h6>
                  <div className='action-buttons'>
                     <div className='new-chat-btn'>
                        <i className='bi-plus-lg'></i>
                        <span className="tooltip">New chat</span>
                     </div>
                     <div className="close-btn" onClick={() => { toggleSidePane(), setCollapse(!collapse) }}>
                        <i className='bi-chevron-left'></i>
                        <span className="tooltip">Collapse</span>
                     </div>
                  </div>
               </div>
               <hr className="divider" />
               <Assistant />
               {/*<div id="terminal" className='terminal'></div>*/}
            </div>
         </div>
         {/* chat pane mini button */}
         <div className='side-pane-mini' style={{ display: collapse ? 'flex' : 'none' }}>
            <button className='chat-btn' onClick={() => { toggleSidePane(), setCollapse(!collapse) }}>
               <div className='icon'>
                  <i className='bi-chat'></i>
               </div>
               <span className="tooltip-side">Open chat</span>
            </button>
            <button className='terminal-btn' onClick={() => { toggleSidePane(), setCollapse(!collapse) }}>
               <div className='icon'>
                  <i className='bi-terminal'></i>
               </div>
               <span className="tooltip-side">Open terminal</span>
            </button>
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
                  <button className='download-btn'>
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
                  <button className='stop-btn' disabled={false}>
                     <div className='icon'>
                        <i className='bi-stop'></i>
                     </div>
                     <span className="tooltip">Stop</span>
                  </button>
               </div>
            </div>

            <Editor
               className='editor-container'
               height="100%"
               defaultLanguage="kotlin"
               defaultValue={defaultCode}
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
      </div>
   );
}

export default Playground;