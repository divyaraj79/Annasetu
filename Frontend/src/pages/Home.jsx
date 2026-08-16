import Hero from "../components/home/Hero";
import Stats from "../components/home/Stats";
import HowItWorks from "../components/home/HowItWorks";
import Features from "../components/home/Features";
import Campaigns from "../components/home/Campaigns";
import Testimonials from "../components/home/Testimonials";
import CTA from "../components/home/CTA";

export default function Home() {
  return (
    <>
      <Hero />
      <Stats />
      <HowItWorks />
      <Features />
      <Campaigns />
      <Testimonials />
      <CTA />
    </>
  );
}