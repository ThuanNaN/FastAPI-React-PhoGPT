import "./App.css";
import Home from "./Home";
import ChatWindow from "./ChatWindow";
import InstructionWindow from "./InstructionWindow";
import Header from "./Header";
import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={[<Header />, <Home/>]}/>
            </Routes>
            <Routes>
                <Route path="/chat" element={[<Header />, <ChatWindow />]} />
            </Routes>
            <Routes>
                <Route
                    path="/instruction"
                    element={[<Header />, <InstructionWindow />]}
                />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
