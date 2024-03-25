import Editor from '@monaco-editor/react';
import '@styles/Playground.scss';
import Assistant from '@components/Assistant';
import { useState } from 'react';

function Playground() {
   const defaultCode = `fun main() {
    print("Hello World!");
}`;
   const [collapse, setCollapse] = useState(false);
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

   const toggleChatPane = () => {
      const chatPane = document.querySelector('.chat-pane');
      const editorPane = document.querySelector('.editor-pane') as HTMLElement;

      if (chatPane) {
         chatPane.classList.toggle('hide');

         if (editorPane) {
            if (chatPane.classList.contains('hide')) {
               editorPane.style.width = '100%';
            } else {
               editorPane.style.width = 'calc(100% - 350px)';
            }
         }
      }
   }

   return (
      <div className="Playground">
         {/* chat pane */}
         <div className="chat-pane" >
            <div className="content">
               <div className="header">
                  <h6>Chat</h6>
                  <div className='action-buttons'>
                     <div className='new-chat-btn'>
                        <i className='bi-plus-lg'></i>
                        <span className="tooltip">New chat</span>
                     </div>
                     <div className="close-btn" onClick={() => { toggleChatPane(), setCollapse(!collapse) }}>
                        <i className='bi-chevron-left'></i>
                        <span className="tooltip">Collapse</span>
                     </div>
                  </div>
               </div>
               <hr className="divider" />
               <Assistant />
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
                  <button className='chat-btn' onClick={() => { toggleChatPane(), setCollapse(!collapse) }} style={{ visibility: collapse ? 'visible' : 'hidden' }}>
                     <div className='icon'>
                        <i className='bi-chat'></i>
                        <span className="tooltip">Open chat</span>
                     </div>
                  </button>
                  <button className='download-btn'>
                     <div className='icon'>
                        <i className='bi-download'></i>
                        <span className="tooltip">Download file</span>
                     </div>
                  </button>
                  <button className='run-btn'>
                     <div className='icon'>
                        <i className='bi-play'></i>
                        <span className="tooltip">Run code</span>
                     </div>
                  </button>
                  <button className='stop-btn' disabled={true}>
                     <div className='icon'>
                        <i className='bi-stop'></i>
                        <span className="tooltip">Stop</span>
                     </div>
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