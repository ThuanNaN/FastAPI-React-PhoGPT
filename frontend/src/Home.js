// Home.js
import React from "react";
import Button from "react-bootstrap/Button";
import Container from "react-bootstrap/Container";

const Home = () => {
    return (
        <Container>
            <div className="d-grid gap-2 p-3">
                <Button href="/instruction" size="lg" variant="outline-primary">
                    Instruction
                </Button>
                <Button href="/chat" size="lg" variant="outline-success">
                    Chat
                </Button>
            </div>
        </Container>
    );
};

export default Home;
