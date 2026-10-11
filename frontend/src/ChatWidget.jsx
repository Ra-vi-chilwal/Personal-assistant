import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import { chat } from "./api.js";
import { suggestions } from "./data.js";

const INTRO = {
  role: "assistant",
  content: "Hi! I'm Ravindar's AI assistant. Ask me anything about his experience, projects or skills.",
};

export default function ChatWidget({ open, setOpen }) {
  const [messages, setMessages] = useState([INTRO]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const endRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, busy, open]);

  useEffect(() => {
    if (open) inputRef.current?.focus();
  }, [open]);

  const send = async (text) => {
    const q = (text ?? input).trim();
    if (!q || busy) return;
    const history = messages.filter((m) => m !== INTRO && !m.error).map(({ role, content }) => ({ role, content }));
    setInput("");
    setMessages((m) => [...m, { role: "user", content: q }]);
    setBusy(true);
    try {
      const answer = await chat(q, history);
      setMessages((m) => [...m, { role: "assistant", content: answer }]);
    } catch (err) {
      setMessages((m) => [...m, { role: "assistant", content: err.message, error: true }]);
    } finally {
      setBusy(false);
    }
  };

  const onKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  };

  return (
    <>
      <button className={"fab" + (open ? " hide" : "")} onClick={() => setOpen(true)} aria-label="Open AI chat">
        <span className="fab-spark">✦</span>
        <span>Ask my AI</span>
      </button>

      <section className={"chat" + (open ? " open" : "")} aria-hidden={!open}>
        <header className="chat-head">
          <div className="chat-title">
            <span className="chat-avatar">✦</span>
            <div>
              <b>Ravindar's AI</b>
              <small><i className="dot" /> Answers from his resume</small>
            </div>
          </div>
          <button onClick={() => setOpen(false)} aria-label="Close chat">✕</button>
        </header>

        <div className="chat-body">
          {messages.map((m, i) => (
            <div key={i} className={"cmsg " + m.role}>
              <div className={"cbubble" + (m.error ? " err" : "")}>
                {m.role === "assistant" ? <ReactMarkdown>{m.content}</ReactMarkdown> : m.content}
              </div>
            </div>
          ))}
          {messages.length === 1 && (
            <div className="chips">
              {suggestions.map((s) => (
                <button key={s} onClick={() => send(s)}>{s}</button>
              ))}
            </div>
          )}
          {busy && (
            <div className="cmsg assistant">
              <div className="cbubble typing"><i /><i /><i /></div>
            </div>
          )}
          <div ref={endRef} />
        </div>

        <div className="chat-input">
          <input
            ref={inputRef}
            value={input}
            maxLength={500}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={onKey}
            placeholder="Ask about Ravindar…"
          />
          <button onClick={() => send()} disabled={!input.trim() || busy} aria-label="Send">↑</button>
        </div>
      </section>
    </>
  );
}
