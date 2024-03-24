import { useState, useRef, useEffect } from 'react';
import Editor from '@monaco-editor/react';
import '@styles/Playground.scss';

function Playground() {
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

   return (
      <div className="Playground">
         <div className="backdrop"></div>
         {/* sidebar */}
         <div className="sidebar">
            <div className="sidebar-content">
               {/* file explorer */}
               <div className="file-explorer card">
                  <div className="header">
                     <h6>File Explorer</h6>
                     <button type="button" className="close-btn">
                        <i className='bi-chevron-left'></i>
                     </button>
                  </div>
                  <hr className="divider" />
               </div>
            </div>
         </div>

         {/* editor pane */}
         <div className="editor-pane">
            <div className='tab-container'>
               <ul className="nav nav-tabs">
                  <li className="nav-item">
                     <a className="nav-link active" aria-current="page" href="#">
                        hello_word.pk
                        <i className='bi-x ms-3'></i>
                     </a>
                  </li>
                  <li className="nav-item">
                     <a className="nav-link">Untitled</a>
                  </li>
                  <a className="new-tab">
                     <i className='bi-plus'></i>
                  </a>
               </ul>
            </div>

            <Editor
               className='editor-container'
               height="85vh"
               defaultLanguage="kotlin"
               defaultValue="// some comment"
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