import type { Basics } from "../types/ResumeTypes";

export const Header = ({ basics }: { basics: Basics }) => (
  <header>
    <h1>{basics.name}</h1>
    <div>
      <a href={`tel:${basics.contact.phone}`}>📞 {basics.contact.phone}</a>
      <a href={`mailto:${basics.contact.email}`}>✉️ {basics.contact.email}</a>
      <a href={basics.contact.github} target="_blank" rel="noopener noreferrer">
        🔗 GitHub
      </a>
    </div>
  </header>
);
