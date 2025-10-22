import type { Basics } from "../types/ResumeTypes";
import Github from "../assets/icons/github.png";
import Location from "../assets/icons/location.png";
import Phone from "../assets/icons/telephone.png";
import Mail from "../assets/icons/mail.png";

export const Header = ({ basics }: { basics: Basics }) => (
  <header>
    <h1>{basics.name}</h1>
    <div className="contact-grid">
      <a href={`tel:${basics.contact.phone}`}>
        <img src={Phone} alt="Phone" />
        {basics.contact.phone}
      </a>
      <a href={`mailto:${basics.contact.email}`}>
        <img src={Mail} alt="Email" />
        {basics.contact.email}
      </a>
      <a href={basics.contact.github} target="_blank" rel="noopener noreferrer">
        <img src={Github} alt="GitHub" />
        {basics.contact.github.replace("https://", "")}
      </a>
    </div>
  </header>
);
