import '@styles/components/ChatWelcome.scss'
import sophie from '@assets/logos/sophie_full_blush.png'
interface ChatWelcomeProps {
    prompts: string[],
    onPromptClick: (prompt: string) => void
}

function ChatWelcome({ prompts, onPromptClick }: ChatWelcomeProps) {

    return (
        <div className='ChatWelcome'>
        <img className='icon' src={sophie} alt="" />
        <h3>How can I assist you?</h3>
        <br />
        {prompts.length !== 0 &&
            <p className='subtitle'>Here are some example prompts:</p>}

        <div className="prompt-list">
        {prompts.map((prompt, index) =>
                <div
                    key={index}
            className="prompt"
            onClick={() => onPromptClick(prompt)}
    data-aos="fade-up" data-aos-delay={index * 200}
        >
        <p>{prompt}</p>
        </div>
)}
    </div>
    </div>
)
}

    export default ChatWelcome