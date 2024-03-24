import { DatabaseService } from "@services/DatabaseService";
import { Conversation } from '@models/Conversation';
import { useState, useEffect, useRef } from 'react';
import React from "react";
import { ChatMessage } from "@models/ChatMessage";
import { DateFormatter } from "@helpers/DateFormatter";

interface ConversationCardProps {
   onChatClick: (messages: ChatMessage[]) => void
   suggestions: (suggestions: string[]) => void
   isActive: (active: boolean) => void
   setUpdate: (update: boolean) => void
   conversationID: (id: string) => void
   toggleSidebar: () => void
   clearNewConversation: (clear: boolean) => void
   messages: ChatMessage[]
   loading: boolean
   newConversation: boolean
   update: boolean
   clearActiveIndex: boolean
}

function TabCard({ onChatClick, suggestions, isActive, setUpdate, conversationID, toggleSidebar, clearNewConversation, messages, loading, newConversation, update, clearActiveIndex }: ConversationCardProps) {
   const [conversations, setConversations] = useState<Conversation[]>([]);
   const [activeIndex, setActiveIndex] = useState('');
   const [editIndex, setEditIndex] = useState('');
   const [description, setDescription] = useState('');
   const [editMode, setEditMode] = useState(false);
   const [isNewConversation, setIsNewConversation] = useState(false);
   const inputRef = useRef<{ [key: string]: React.RefObject<HTMLInputElement> }>({});

   const dbService = new DatabaseService();

   const getConversations = async () => {
      try {
         //const response = await dbService.getConversations();
         //setConversations(response);
         //console.log('Retrieved conversations')
      } catch (e) {
         console.log(e);
      }
   };

   const deleteConversation = async (conversationId: string) => {
      try {
         await dbService.deleteConversation(conversationId);
         getConversations();
      } catch (e) {
         console.log(e);
      }
   };

   const editConversation = async (conversationId: string) => {
      try {
         const conversation = conversations.find(conversation => conversation.id === conversationId);
         if (conversation) {
            conversation.name = description;
            await dbService.updateConversation(conversationId, conversation);
            setEditMode(!editMode);
         }
      } catch (e) {
         console.log(e);
      }
   };

   useEffect(() => {
      if (newConversation) {
         setActiveIndex(conversations[0].id);
         setIsNewConversation(true);
         clearNewConversation(false);
      }
      // eslint-disable-next-line react-hooks/exhaustive-deps
   }, [conversations]);

   useEffect(() => {
      if (update) {
         //console.log('Updating conversations');
         getConversations();
         setUpdate(false);
      }
      // eslint-disable-next-line react-hooks/exhaustive-deps
   }, [update]);

   useEffect(() => {
      setActiveIndex('');
   }, [clearActiveIndex]);

   useEffect(() => {
      if (isNewConversation) {
         setTimeout(() => setIsNewConversation(false), 2000);
      }
   }, [isNewConversation]);

   useEffect(() => {
      if (editMode && editIndex && inputRef.current[editIndex]) {
         inputRef.current[editIndex].current?.focus();
      }
   }, [editMode, editIndex]);

   return (
      <div className="list">
         {conversations.length === 0 && <h6 className="text-secondary text-center w-100 mt-2">No tabs yet</h6>}
         {conversations.map((conversation) => {
            if (!inputRef.current[conversation.id]) {
               inputRef.current[conversation.id] = React.createRef();
            }
            return (
               <React.Fragment key={conversation.id}>
                  <div className={`chat-item ${(editMode && editIndex === conversation.id) ? 'edit-mode' : ''} ${activeIndex === conversation.id ? 'active' : ''}`}>
                     <div className="indicator" />
                     <div className="input-group">
                        <input
                           ref={inputRef.current[conversation.id]}
                           type={'text'}
                           className='form-control'
                           aria-describedby="basic-addon2"
                           value={editMode && editIndex === conversation.id ? description : conversation.name}
                           onChange={(e) => setDescription(e.target.value)}
                           autoFocus
                           required
                        />
                     </div>
                     <div className="description" onClick={() => { loading ? '' : activeIndex === conversation.id ? '' : (onChatClick(conversation.messages), isActive(true), suggestions([]), setActiveIndex(conversation.id)) }}>
                        <h6 className={`name ${isNewConversation && activeIndex === conversation.id ? 'typing-effect' : ''}`}>{conversation.name}</h6>
                     </div>
                     <div className="controls">
                        <button className="confirm icon-button" type="button" aria-label="Confirm" onClick={() => editConversation(conversation.id)}>
                           <i className="bi-check"></i>
                        </button>
                        <button className="cancel icon-button" type="button" aria-label="Cancel" onClick={() => setEditMode(!editMode)}>
                           <i className="bi-x"></i>
                        </button>
                     </div>
                  </div>
                  <hr className="divider" />
                  <div className="modal fade delete-modal" id={`deleteModal-${conversation.id}`} tabIndex={-1} aria-labelledby="deleteLabel" aria-hidden="true" key={`modal-${conversation.id}`}>
                     <div className="modal-dialog modal-dialog-centered">
                        <div className="modal-content">
                           <div className="modal-header">
                              <h1 className="modal-title fs-5" id="staticBackdropLabel">Delete chat?</h1>
                           </div>
                           <div className="modal-body">
                              <h6>This will delete <span style={{ fontWeight: 'bold' }}>{conversation.name}</span>.</h6>
                           </div>
                           <div className="button-group">
                              <button type="button" className="btn btn-secondary cancel-button" data-bs-dismiss="modal">Cancel</button>
                              <button type="button" className="btn btn-primary delete-button" data-bs-dismiss="modal" onClick={() => { (conversation.messages === messages) ? onChatClick([]) : activeIndex == conversation.id ? (onChatClick([]), suggestions([]), conversationID('')) : '', deleteConversation(conversation.id) }}>
                                 Delete
                              </button>
                           </div>
                        </div>
                     </div>
                  </div>
               </React.Fragment>
            );
         })}
      </div>
   )
}

export default TabCard;