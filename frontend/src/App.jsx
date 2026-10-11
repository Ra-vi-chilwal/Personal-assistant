import { useEffect, useState } from "react";
import ChatWidget from "./ChatWidget.jsx";
import { education, experience, profile, projects, skills, stats } from "./data.js";

function useReveal() {
  useEffect(() => {
    const io = new IntersectionObserver(
      (entries) => entries.forEach((e) => e.isIntersecting && (e.target.classList.add("in"), io.unobserve(e.target))),
      { threshold: 0.12 }
    );
    document.querySelectorAll(".reveal").forEach((el) => io.observe(el));
    return () => io.disconnect();
  }, []);
}

const NAV = [
  ["about", "About"],
  ["skills", "Skills"],
  ["experience", "Experience"],
  ["projects", "Projects"],
  ["contact", "Contact"],
];

function Section({ id, eyebrow, title, children }) {
  return (
    <section id={id} className="section">
      <div className="wrap">
        <div className="reveal">
          <p className="eyebrow">{eyebrow}</p>
          <h2>{title}</h2>
        </div>
        {children}
      </div>
    </section>
  );
}

export default function App() {
  const [chatOpen, setChatOpen] = useState(false);
  const [menu, setMenu] = useState(false);
  useReveal();

  return (
    <>
      <header className="nav">
        <div className="wrap nav-in">
          <a href="#top" className="logo-link"><span className="logo">R</span><b>Ravindar</b></a>
          <nav className={menu ? "open" : ""}>
            {NAV.map(([id, label]) => (
              <a key={id} href={`#${id}`} onClick={() => setMenu(false)}>{label}</a>
            ))}
            <button className="btn small" onClick={() => { setMenu(false); setChatOpen(true); }}>✦ Ask my AI</button>
          </nav>
          <button className="burger" onClick={() => setMenu(!menu)} aria-label="Menu">☰</button>
        </div>
      </header>

      <main id="top">
        <section className="hero">
          <div className="glow g1" /><div className="glow g2" />
          <div className="wrap hero-in">
            <p className="pill"><i className="dot" /> Open to new opportunities</p>
            <h1>
              Hi, I'm <span className="grad">{profile.name.split(" ")[0]}</span>.<br />
              {profile.role}.
            </h1>
            <p className="lead">{profile.tagline}</p>
            <div className="cta">
              <button className="btn" onClick={() => setChatOpen(true)}>✦ Chat with my AI</button>
              <a className="btn ghost" href={profile.resume} download>Download résumé</a>
              <a className="btn ghost" href="#contact">Get in touch</a>
            </div>
            <div className="stats">
              {stats.map((s) => (
                <div key={s.label} className="stat">
                  <b>{s.value}</b><span>{s.label}</span>
                </div>
              ))}
            </div>
          </div>
        </section>

        <Section id="about" eyebrow="About" title="Building products that think">
          <div className="about reveal">
            {profile.about.map((p, i) => <p key={i}>{p}</p>)}
            <p className="muted">📍 {profile.location}</p>
          </div>
        </Section>

        <Section id="skills" eyebrow="Toolbox" title="Skills & technologies">
          <div className="skills">
            {skills.map((g) => (
              <div key={g.group} className="card reveal">
                <h3>{g.group}</h3>
                <div className="tags">{g.items.map((t) => <span key={t}>{t}</span>)}</div>
              </div>
            ))}
          </div>
        </Section>

        <Section id="experience" eyebrow="Career" title="Where I've worked">
          <div className="timeline">
            {experience.map((e) => (
              <article key={e.company} className="tl-item reveal">
                <span className="tl-dot" />
                <div className="tl-head">
                  <h3>{e.title} <span className="at">@ {e.company}</span></h3>
                  <span className="period">{e.period}</span>
                </div>
                <p className="muted">{e.place}</p>
                <ul>{e.points.map((p, i) => <li key={i}>{p}</li>)}</ul>
              </article>
            ))}
          </div>
          <div className="edu card reveal">
            <h3>Education</h3>
            <p><b>{education.degree}</b>, {education.school}</p>
            <p className="muted">{education.period} · {education.note}</p>
          </div>
        </Section>

        <Section id="projects" eyebrow="Work" title="Selected projects">
          <div className="projects">
            {projects.map((p) => (
              <article key={p.title} className="card project reveal">
                <h3>{p.title}</h3>
                <p>{p.desc}</p>
                <div className="tags">{p.tags.map((t) => <span key={t}>{t}</span>)}</div>
              </article>
            ))}
          </div>
        </Section>

        <Section id="contact" eyebrow="Contact" title="Let's build something together">
          <div className="contact card reveal">
            <p>Have a project, a role or just a question? My inbox is open, or ask my AI assistant anything about my work.</p>
            <div className="cta">
              <a className="btn" href={`mailto:${profile.email}`}>{profile.email}</a>
              <a className="btn ghost" href={profile.linkedin} target="_blank" rel="noreferrer">LinkedIn</a>
              <a className="btn ghost" href={profile.github} target="_blank" rel="noreferrer">GitHub</a>
            </div>
          </div>
        </Section>
      </main>

      <footer className="footer">
        <div className="wrap">© {new Date().getFullYear()} {profile.name}. Built with React, FastAPI & RAG.</div>
      </footer>

      <ChatWidget open={chatOpen} setOpen={setChatOpen} />
    </>
  );
}
