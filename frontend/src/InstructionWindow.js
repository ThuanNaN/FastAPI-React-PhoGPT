import React, { useState } from "react";
import axios from "axios";
import "./styles.css";

const InstructionWindow = () => {
    const [chatHistory, setChatHistory] = useState([]);

    const handleUserMessage = async (messageText) => {
        const newUserMessage = { content: messageText, role: "user" };
        setChatHistory((chatHistory) => [...chatHistory, newUserMessage]);

        try {
            const response = await axios.post(
                "http://0.0.0.0:5000/instruction",
                {
                    input_prompt: messageText,
                }
            );
            const botResponse = { content: response.data.text, role: "assistant" };
            setChatHistory((chatHistory) => [...chatHistory, botResponse]);
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div className="chat-window">
            <MessageList chatHistory={chatHistory} />
            <MessageInput onMessageSubmit={handleUserMessage} />
        </div>
    );
};

const MessageList = ({ chatHistory }) => {
    return (
        <ul className="message-list">
            {chatHistory.map((message, index) => (
                <li key={index} className={`message ${message.role}`}>
                    {message.content.split(/\n/).map((line) => (
                        <div key={line}>{line}</div>
                    ))}
                </li>
            ))}
        </ul>
    );
};

const MessageInput = ({ onMessageSubmit }) => {
    const [inputMessage, setInputMessage] = useState("");

    const handleSubmit = () => {
        if (inputMessage !== "") {
            onMessageSubmit(inputMessage);
            setInputMessage("");
        }
    };

    return (
        <div className="message-input">
            <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Type your message..."
            />
            <button onClick={handleSubmit}>Send</button>
        </div>
    );
};

export default InstructionWindow;
